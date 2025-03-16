import os
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from .forms import RimburseForm, PayrollForm, ReimbursementForm
from .forms import ReimbursementStep1Form, ReimbursementStep2Form, ReimbursementStep3Form
from api.models import ReimbursementRequest
import re
from django.contrib.auth.decorators import login_required
from authentication.views import dashboard
from django.contrib import messages
from django.conf import settings
import datetime

def escape_latex(value):
    """ Escapes LaTeX special characters in user input """
    if not isinstance(value, str):
        return value
    return value.replace('_', '\\_').replace('&', '\\&').replace('%', '\\%')

#for testing only
def generate_payroll_pdf(request):
    LATEX_TEMPLATE_PATH = "latexform/payroll-assignment.tex"
    OUTPUT_PDF_PATH = "output/filled_template.pdf"
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            # Extract form data
            context = {key.upper(): value for key, value in form.cleaned_data.items()}

            # Read LaTeX template
            with open(LATEX_TEMPLATE_PATH, "r") as file:
                tex_content = file.read()

            # Replace placeholders with user input
            for placeholder, value in context.items():
                tex_content = tex_content.replace(f"{{{{{placeholder}}}}}", str(value))

            # Save modified LaTeX file
            filled_tex_path = "output/filled_template.tex"
            with open(filled_tex_path, "w") as file:
                file.write(tex_content)

            # Run Makefile to generate PDF
            try:
                subprocess.run(["make", "pdf"], check=True)
            except subprocess.CalledProcessError as e:
                return HttpResponse(f"Error generating PDF: {e}", status=500)

            return FileResponse(open(OUTPUT_PDF_PATH, "rb"), content_type="application/pdf")

    else:
        form = PayrollForm()
    return render(request, 'form.html', {'form': form})
##--------------------------------------------------------------------------------------------------------
# Implement with model

def generate_reimbursement_pdf(request, reimbursement_id):
    """ Generates PDF from saved reimbursement form data """
    LATEX_TEMPLATE_PATH = "latexform/reimburse.tex"
    OUTPUT_PDF_PATH = "output/filled_template.pdf"
    NEW_PDF_NAME = f"reimbursement_{reimbursement_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    NEW_PDF_PATH = os.path.join("output/", NEW_PDF_NAME)
    PDF_URL = f"output/{NEW_PDF_NAME}" 

    reimbursement = get_object_or_404(ReimbursementRequest, id=reimbursement_id)

    # Convert model fields to a dictionary and escape LaTeX special characters
    context = {field.name.upper(): escape_latex(str(getattr(reimbursement, field.name, ''))) for field in ReimbursementRequest._meta.fields}

    # Read LaTeX template
    with open(LATEX_TEMPLATE_PATH, "r") as file:
        tex_content = file.read()

    # Ensure replace placeholders including LaTeX escaped versions
    for key, value in context.items():
        tex_content = re.sub(r'\{\{' + key.replace('_', r'\\_') + r'\}\}', value, tex_content)

    # Save modified LaTeX file
    filled_tex_path = "output/filled_template.tex"
    with open(filled_tex_path, "w") as file:
        file.write(tex_content)

    # Debugging: Print the first few lines of the LaTeX file before compiling
    with open(filled_tex_path, "r") as file:
        print("\n".join(file.readlines()[:20]))

    # Compile LaTeX to PDF
    subprocess.run(["make", "pdf"], check=True)
    
    # Ensure the file exists before renaming
    if os.path.exists(OUTPUT_PDF_PATH):
        os.rename(OUTPUT_PDF_PATH, NEW_PDF_PATH)  # Rename the file

    # Store the new PDF path in the database
    reimbursement.pdf_url = PDF_URL
    reimbursement.save()

    messages.success(request, f"Form submitted successfully!")
    return redirect(dashboard)

@login_required
def reimbursement_step1(request):
    """ Step 1: Employee Info - Check for unfinished form first """
    user = request.user

    # Check for an existing pending reimbursement form
    pending_reimbursement = ReimbursementRequest.objects.filter(user=user, status="Pending").first()
    if pending_reimbursement:
        messages.error(request, "You already have a pending reimbursement request!")
        return redirect('dashboard')

    # Check for an existing draft form
    draft_reimbursement = ReimbursementRequest.objects.filter(user=user, status="Draft").first()
    
    if request.method == 'POST':
        form = ReimbursementStep1Form(request.POST, instance=draft_reimbursement)
        if form.is_valid():
            reimbursement = form.save(commit=False)
            reimbursement.user = user
            reimbursement.status = "Draft"
            reimbursement.save()
            return redirect('reimbursement_step2', reimbursement_id=reimbursement.id)
    else:
        form = ReimbursementStep1Form(instance=draft_reimbursement)

    return render(request, 'reimbursement_step1.html', {'form': form, 'reimbursement': draft_reimbursement})


@login_required
def reimbursement_step2(request, reimbursement_id=None):
    """ Step 2: Expense Details - Only proceed if form exists """
    user = request.user

    # Check if the form exists
    if not reimbursement_id:
        reimbursement = ReimbursementRequest.objects.filter(user=user, status="Draft").first()
        if reimbursement:
            return redirect('reimbursement_step2', reimbursement_id=reimbursement.id)
        return redirect('reimbursement_step1')  # No draft, restart process

    reimbursement = get_object_or_404(ReimbursementRequest, id=reimbursement_id, user=user)

    if request.method == 'POST':
        form = ReimbursementStep2Form(request.POST, instance=reimbursement)
        if form.is_valid():
            form.save()
            return redirect('reimbursement_step3', reimbursement_id=reimbursement.id)
    else:
        form = ReimbursementStep2Form(instance=reimbursement)

    return render(request, 'reimbursement_step2.html', {'form': form, 'reimbursement': reimbursement})

@login_required
def reimbursement_step3(request, reimbursement_id=None):
    """ Step 3: Cost Center Details - Only proceed if form exists """
    user = request.user

    # Check if the form exists
    if not reimbursement_id:
        reimbursement = ReimbursementRequest.objects.filter(user=user, status="Draft").first()
        if reimbursement:
            return redirect('reimbursement_step3', reimbursement_id=reimbursement.id)
        return redirect('reimbursement_step1')  # No draft, restart process

    reimbursement = get_object_or_404(ReimbursementRequest, id=reimbursement_id, user=user)

    if request.method == 'POST':
        form = ReimbursementStep3Form(request.POST, instance=reimbursement)
        if form.is_valid():
            reimbursement = form.save(commit=False)
            reimbursement.status = "Pending"  # Mark as completed
            reimbursement.save()
            return redirect('generate_reimbursement_pdf', reimbursement_id=reimbursement.id)
    else:
        form = ReimbursementStep3Form(instance=reimbursement)

    return render(request, 'reimbursement_step3.html', {'form': form, 'reimbursement': reimbursement})

@login_required
def delete_reimbursement(request, reimbursement_id):
    """ Allows a user to delete their draft or pending reimbursement request """
    reimbursement = get_object_or_404(ReimbursementRequest, id=reimbursement_id, user=request.user)

    if reimbursement.status in ["Draft", "Pending"]:
        reimbursement.delete()
        messages.success(request, "Your reimbursement request has been deleted successfully.")
    else:
        messages.error(request, "You can only delete Draft or Pending forms.")

    return redirect('dashboard')

@login_required
def view_pdf(request):
    """ Opens the latest reimbursement request PDF for the logged-in user """
    
    # Get the latest reimbursement request with a PDF URL
    reimbursement = ReimbursementRequest.objects.filter(
        user=request.user,
        pdf_url__isnull=False
    ).order_by('-id').first()

    if not reimbursement or not reimbursement.pdf_url:
        return HttpResponse("No PDF available.", status=404)

    # Convert the stored URL to an absolute file path
    pdf_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(reimbursement.pdf_url))

    # Ensure the file exists
    if not os.path.exists(pdf_path):
        return HttpResponse("PDF file not found.", status=404)

    # Serve the PDF file
    return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")