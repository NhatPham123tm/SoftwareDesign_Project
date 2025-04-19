import os, time
from PIL import Image
import subprocess
from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from .forms import ReimbursementStep1Form, ReimbursementStep2Form, ReimbursementStep3Form,PayrollStep1Form, PayrollStep2Form, PayrollStep3Form, PayrollStep4Form, PayrollStep5Form, PayrollStep6Form, PayrollStep7Form, PayrollStep8Form, PayrollStep9Form, PayrollStep10Form, ChangeAddressStep1Form, ChangeAddressStep2Form, ChangeAddressStep3Form, DiplomaStep1Form, DiplomaStep2Form
from api.models import ReimbursementRequest, PayrollAssignment, ChangeOfAddress, DiplomaRequest
import re
from django.contrib.auth.decorators import login_required
from authentication.views import dashboard
from django.contrib import messages
from django.conf import settings
import datetime
import base64
from workflow.views import assign_workflow_steps, advance_to_next_workflow_step

# utility functions for latex and pdf
def escape_latex(value):
    """ Escapes LaTeX special characters in user input """
    if not isinstance(value, str):
        return value
    return value.replace('_', '\\_').replace('&', '\\&').replace('%', '\\%')

# Generate signature image from base64 data
def save_signature_image(base64_data, output_path):
    """Save base64-encoded signature to an image file, or generate blank PNG if data is missing."""

    # Create directory if it doesn't exist was causing issues with docker
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        if base64_data and base64_data.startswith("data:image"):
            format, imgstr = base64_data.split(';base64,')
            img_data = base64.b64decode(imgstr)
            with open(output_path, 'wb') as f:
                f.write(img_data)
        else:
            raise ValueError("No valid image data")
    except Exception as e:
        # Create a blank white image as fallback
        blank_img = Image.new("RGB", (300, 100), color="white")
        blank_img.save(output_path, format="PNG")


def save_signatures(form_instance):
    paths = []
    for attr, filename in [("signature_base64", "signatureUser.png"), ("signatureAdmin_base64", "signatureAdmin.png")]:
        if hasattr(form_instance, attr):
            path = os.path.join("output", filename)
            save_signature_image(getattr(form_instance, attr), path)
            paths.append(path)
    return paths

def get_pdf_paths(model_name, form_id):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    base = f"{model_name.lower()}_{form_id}_{timestamp}.pdf"
    return {
        "filled_tex": "output/filled_template.tex",
        "compiled_pdf": "output/filled_template.pdf",
        "final_pdf": os.path.join("output", base),
        "relative_url": f"output/{base}"
    }

def fill_latex_template(context, template_path, output_dir="output", tex_name="filled_template.tex"):
    with open(template_path, "r", encoding="utf-8") as file:
        tex_content = file.read()
    for key, value in context.items():
        tex_content = re.sub(r'\{\{' + key.replace('_', r'\\_') + r'\}\}', value, tex_content)
    filled_path = os.path.join(output_dir, tex_name)
    with open(filled_path, "w", encoding="utf-8") as file:
        file.write(tex_content)
    return filled_path

def generate_pdf_and_redirect(request, instance, latex_path, dashboard_redirect=True):
    sig_paths = save_signatures(instance)
    context = {field.name.upper(): escape_latex(str(getattr(instance, field.name) or '')) for field in instance._meta.fields}
    paths = get_pdf_paths(type(instance).__name__, instance.id)
    
    filled_tex_path = fill_latex_template(context, latex_path)
    
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", "output", filled_tex_path],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if os.path.exists(paths["compiled_pdf"]):
            os.rename(paths["compiled_pdf"], paths["final_pdf"])
            instance.pdf_url = paths["relative_url"]
            instance.save()
    except subprocess.CalledProcessError as e:
        print("PDF generation failed", e.stdout.decode(), e.stderr.decode())

    for path in sig_paths:
        if os.path.exists(path):
            os.remove(path)
            
    # Assign workflow steps
    assign_workflow_steps(instance)

    if dashboard_redirect:
        messages.success(request, "Form submitted successfully.")
        return redirect('dashboard')
    return None

# Generates a PDF from the form model using a LaTeX template and given form ID
def generate_pdf_from_form_id(request, form_id, ModelClass, latex_template_path, output_dir="output"):
    instance = get_object_or_404(ModelClass, id=form_id)
    
    new_pdf_name = f"{ModelClass.__name__.lower()}_{form_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    new_pdf_path = os.path.join(output_dir, new_pdf_name)
    output_pdf_path = os.path.join(output_dir, "filled_template.pdf")
    pdf_url = os.path.join(output_dir, new_pdf_name)

    # Prepare LaTeX-safe context from model fields
    context = {}
    for field in ModelClass._meta.fields:
        value = getattr(instance, field.name)
        
        # Convert PostgreSQL boolean values ('t'/'f') to Python Boolean
        if isinstance(value, bool):  
            value = "True" if value else "False"
        
        context[field.name.upper()] = escape_latex(str(value or ''))


    # Read and fill LaTeX template
    with open(latex_template_path, "r") as file:
        tex_content = file.read()

    for key, value in context.items():
        tex_content = re.sub(r'\{\{' + key.replace('_', r'\\_') + r'\}\}', value, tex_content)

    # Write the filled LaTeX content
    filled_tex_path = os.path.join(output_dir, "filled_template.tex")
    with open(filled_tex_path, "w") as file:
        file.write(tex_content)

    # Compile LaTeX to PDF
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_dir, filled_tex_path],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("LaTeX compilation failed:")
        print("Stdout:", e.stdout.decode())
        print("Stderr:", e.stderr.decode())

    # Rename compiled PDF if successful
    if os.path.exists(output_pdf_path):
        os.rename(output_pdf_path, new_pdf_path)

    # Save URL/path to model 
    if hasattr(instance, "pdf_url"):
        instance.pdf_url = pdf_url
        instance.save()
    
    #messages.success(request, f"PDF generated successfully.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

def handle_form_pdf_response(request, form_instance, template_name):
    if not form_instance or not form_instance.pdf_url:
        return HttpResponse("No PDF available.", status=404)

    # Save signature if available
    signature_output_path_admin = os.path.join("output", "signatureAdmin.png")
    save_signature_image(getattr(form_instance, 'signatureAdmin_base64', ''), signature_output_path_admin)
    signature_output_path_user = os.path.join("output", "signatureUser.png")
    save_signature_image(getattr(form_instance, 'signature_base64', ''), signature_output_path_user)
   
    # Generate PDF (always regenerate for consistency)
    generate_pdf_from_form_id(
        request=request,
        form_id=form_instance.id,
        ModelClass=type(form_instance),
        latex_template_path=template_name
    )

    form_instance.refresh_from_db()
    time.sleep(0.1)

    pdf_path = os.path.join(settings.MEDIA_ROOT, os.path.basename(form_instance.pdf_url))

    if os.path.exists(signature_output_path_admin):
        os.remove(signature_output_path_admin)
    if os.path.exists(signature_output_path_user):
        os.remove(signature_output_path_user)

    if not os.path.exists(pdf_path):
        return HttpResponse("PDF file not found.", status=404)

    return FileResponse(open(pdf_path, "rb"), content_type="application/pdf")

#-----------------------------------------------------------------------------------
# Reimbursement section
def generate_reimbursement_pdf(request, reimbursement_id):
    """ Generates PDF from saved reimbursement form data """
    LATEX_TEMPLATE_PATH = "latexform/reimburse.tex"
    OUTPUT_PDF_PATH = "output/filled_template.pdf"
    NEW_PDF_NAME = f"reimbursement_{reimbursement_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    NEW_PDF_PATH = os.path.join("output/", NEW_PDF_NAME)
    PDF_URL = f"output/{NEW_PDF_NAME}" 
    
    reimbursement = get_object_or_404(ReimbursementRequest, id=reimbursement_id)

    # Save signature image if available
    signature_output_path_user = os.path.join("output", "signatureUser.png")
    signature_output_path_admin = os.path.join("output", "signatureAdmin.png")
    save_signature_image(reimbursement.signature_base64, signature_output_path_user)
    save_signature_image(reimbursement.signatureAdmin_base64, signature_output_path_admin)

    # Convert model fields to a dictionary and escape LaTeX special characters
    context = {field.name.upper(): escape_latex(str(getattr(reimbursement, field.name) or '')) for field in ReimbursementRequest._meta.fields}

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
    try:
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", "output", "output/filled_template.tex"],
            check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        print("Warning: pdflatex returned a non-zero exit status")
        print("Stdout:", e.stdout.decode())
        print("Stderr:", e.stderr.decode())
    
    # Ensure the file exists before renaming
    if os.path.exists(OUTPUT_PDF_PATH):
        os.rename(OUTPUT_PDF_PATH, NEW_PDF_PATH)  # Rename the file

    # Store the new PDF path in the database
    reimbursement.pdf_url = PDF_URL
    reimbursement.save()

    # Delete signature png
    if os.path.exists(signature_output_path_user):
        os.remove(signature_output_path_user)
    if os.path.exists(signature_output_path_admin):
        os.remove(signature_output_path_admin)

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

#-------------------------------------------------------------
## payroll section
@login_required
def payroll_step1(request):
    """ Step 1: Employee Info - Prevent multiple pending forms """
    user = request.user

    # Check for an existing pending or draft payroll request
    pending_payroll = PayrollAssignment.objects.filter(user=user, status="Pending").first()
    if pending_payroll:
        messages.error(request, "You already have a pending payroll request!")
        return redirect('dashboard')

    draft_payroll = PayrollAssignment.objects.filter(user=user, status="Draft").first()

    if request.method == 'POST':
        form = PayrollStep1Form(request.POST, instance=draft_payroll)
        if form.is_valid():
            payroll = form.save(commit=False)
            payroll.user = user
            payroll.status = "Draft"
            payroll.save()

            # Check the requested_action and redirect accordingly
            if payroll.requested_action == 'New Hire' or payroll.requested_action == 'Rehire/Transfer':
                return redirect('payroll_step7', payroll_id=payroll.id)
            else:
                return redirect('payroll_step2', payroll_id=payroll.id)

    else:
        form = PayrollStep1Form(instance=draft_payroll)

    return render(request, 'payroll_step1.html', {'form': form, 'payroll': draft_payroll})


@login_required
def payroll_step2(request, payroll_id):
    """ Step 2: Job Information """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep2Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step3', payroll_id=payroll.id)
    else:
        form = PayrollStep2Form(instance=payroll)

    return render(request, 'payroll_step2.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step3(request, payroll_id):
    """ Step 3: Budget Change Details """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep3Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step4', payroll_id=payroll.id)
    else:
        form = PayrollStep3Form(instance=payroll)

    return render(request, 'payroll_step3.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step4(request, payroll_id):
    """ Step 4: FTE Change Details """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep4Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step5', payroll_id=payroll.id)
    else:
        form = PayrollStep4Form(instance=payroll)

    return render(request, 'payroll_step4.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step5(request, payroll_id):
    """ Step 5: Pay Rate Change Details """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep5Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step6', payroll_id=payroll.id)
    else:
        form = PayrollStep5Form(instance=payroll)

    return render(request, 'payroll_step5.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step6(request, payroll_id):
    """ Step 6: Reallocation & Other Changes """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep6Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step9', payroll_id=payroll.id)
    else:
        form = PayrollStep6Form(instance=payroll)

    return render(request, 'payroll_step6.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step7(request, payroll_id):
    """ Step 7: First Position Information """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep7Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step8', payroll_id=payroll.id)
    else:
        form = PayrollStep7Form(instance=payroll)

    return render(request, 'payroll_step7.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step8(request, payroll_id):
    """ Step 8: First Position Details """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep8Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()

            return redirect('payroll_review', payroll_id=payroll.id)  

    else:
        form = PayrollStep8Form(instance=payroll)

    return render(request, 'payroll_step8.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step9(request, payroll_id):
    """ Step 9: Second Position (Only for Rehire/Transfer) """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep9Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_step10', payroll_id=payroll.id)
    else:
        form = PayrollStep9Form(instance=payroll)

    return render(request, 'payroll_step9.html', {'form': form, 'payroll': payroll})


@login_required
def payroll_step10(request, payroll_id):
    """ Step 10: Second Position Details (Only for Rehire/Transfer) """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if request.method == 'POST':
        form = PayrollStep10Form(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_review', payroll_id=payroll.id)
    else:
        form = PayrollStep10Form(instance=payroll)

    return render(request, 'payroll_step10.html', {'form': form, 'payroll': payroll})

@login_required
def payroll_review(request, payroll_id):
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)
    return generate_pdf_and_redirect(request, payroll, "latexform/payroll-assignment.tex")
   
@login_required
def delete_payroll(request, payroll_id):
    """ Allows a user to delete their draft or pending payroll request """
    payroll = get_object_or_404(PayrollAssignment, id=payroll_id, user=request.user)

    if payroll.status in ["Draft", "Pending"]:
        payroll.delete()
        messages.success(request, "Your payroll request has been deleted successfully.")
    else:
        messages.error(request, "You can only delete Draft or Pending payroll forms.")

    return redirect('dashboard')

#--------------------------------------------------------------------------------
# Change address section

@login_required
def change_address_step1(request):
    """ Step 1: Personal Info """
    user = request.user

    # Check if user already has a pending form
    pending_form = ChangeOfAddress.objects.filter(user=user, status="Pending").first()
    if pending_form:
        messages.error(request, "You already have a pending change of address request.")
        return redirect('dashboard')

    # Get draft if exists
    draft_form = ChangeOfAddress.objects.filter(user=user, status="Draft").first()

    if request.method == 'POST':
        form = ChangeAddressStep1Form(request.POST, instance=draft_form)
        if form.is_valid():
            change_form = form.save(commit=False)
            change_form.user = user
            change_form.status = "Draft"
            change_form.save()
            return redirect('change_address_step2', form_id=change_form.id)
    else:
        form = ChangeAddressStep1Form(instance=draft_form)

    return render(request, 'change_address_step1.html', {'form': form})


@login_required
def change_address_step2(request, form_id=None):
    """ Step 2: Address Info """
    user = request.user

    # Find draft or redirect back
    if not form_id:
        draft = ChangeOfAddress.objects.filter(user=user, status="Draft").first()
        if draft:
            return redirect('change_address_step2', form_id=draft.id)
        return redirect('change_address_step1')

    change_form = get_object_or_404(ChangeOfAddress, id=form_id, user=user)

    if request.method == 'POST':
        form = ChangeAddressStep2Form(request.POST, instance=change_form)
        if form.is_valid():
            form.save()
            return redirect('change_address_step3', form_id=change_form.id)
    else:
        form = ChangeAddressStep2Form(instance=change_form)

    return render(request, 'change_address_step2.html', {'form': form})


@login_required
def change_address_step3(request, form_id=None):
    """ Step 3: Signature & Submission """
    user = request.user

    # Find draft or redirect back
    if not form_id:
        draft = ChangeOfAddress.objects.filter(user=user, status="Draft").first()
        if draft:
            return redirect('change_address_step3', form_id=draft.id)
        return redirect('change_address_step1')

    change_form = get_object_or_404(ChangeOfAddress, id=form_id, user=user)

    if request.method == 'POST':
        form = ChangeAddressStep3Form(request.POST, instance=change_form)
        if form.is_valid():
            submitted_form = form.save(commit=False)
            submitted_form.status = "Pending"
            submitted_form.save()
            return redirect('generate_change_address_pdf', form_id=submitted_form.id)
    else:
        form = ChangeAddressStep3Form(instance=change_form)

    return render(request, 'change_address_step3.html', {'form': form})

@login_required
def delete_address(request, form_id):
    """ Allows a user to delete their draft or pending address change request """
    address_form = get_object_or_404(ChangeOfAddress, id=form_id, user=request.user)

    if address_form.status in ["Draft", "Pending"]:
        address_form.delete()
        messages.success(request, "Your change of address request has been deleted successfully.")
    else:
        messages.error(request, "You can only delete Draft or Pending forms.")

    return redirect('dashboard')

@login_required
def generate_change_address_pdf(request, form_id):
    address = get_object_or_404(ChangeOfAddress, id=form_id, user=request.user)
    return generate_pdf_and_redirect(request, address, "latexform/change_address.tex")

#-------------------------------------------------------------------------
# Diploma request form

@login_required
def diploma_step1(request):
    """ Step 1: Personal Info & Contact """
    user = request.user

    pending_diploma = DiplomaRequest.objects.filter(user=user, status="Pending").first()
    if pending_diploma:
        messages.error(request, "You already have a pending diploma request.")
        return redirect('dashboard')

    draft = DiplomaRequest.objects.filter(user=user, status="Draft").first()

    if request.method == 'POST':
        form = DiplomaStep1Form(request.POST, instance=draft)
        if form.is_valid():
            diploma = form.save(commit=False)
            diploma.user = user
            diploma.status = "Draft"
            diploma.save()
            return redirect('diploma_step2', diploma_id=diploma.id)
    else:
        form = DiplomaStep1Form(instance=draft)

    return render(request, 'diploma_step1.html', {'form': form})

@login_required
def diploma_step2(request, diploma_id=None):
    """ Step 2: Address & Signature """
    user = request.user

    if not diploma_id:
        draft = DiplomaRequest.objects.filter(user=user, status="Draft").first()
        if draft:
            return redirect('diploma_step2', diploma_id=draft.id)
        return redirect('diploma_step1')

    diploma = get_object_or_404(DiplomaRequest, id=diploma_id, user=user)

    if request.method == 'POST':
        form = DiplomaStep2Form(request.POST, instance=diploma)
        if form.is_valid():
            completed = form.save(commit=False)
            completed.status = "Pending"
            completed.save()
            return redirect('generate_diploma_pdf', diploma_id=completed.id)
    else:
        form = DiplomaStep2Form(instance=diploma)

    return render(request, 'diploma_step2.html', {'form': form})

@login_required
def delete_diploma(request, form_id):
    """ Allows a user to delete their draft or pending diploma request """
    diploma_form = get_object_or_404(DiplomaRequest, id=form_id, user=request.user)

    if diploma_form.status in ["Draft", "Pending"]:
        diploma_form.delete()
        messages.success(request, "Your diploma request has been deleted successfully.")
    else:
        messages.error(request, "You can only delete Draft or Pending forms.")

    return redirect('dashboard')

@login_required
def generate_diploma_pdf(request, diploma_id):
    diploma = get_object_or_404(DiplomaRequest, id=diploma_id, user=request.user)
    return generate_pdf_and_redirect(request, diploma, "latexform/diploma.tex")

#-------------------------------------------------------------------
# View PDF functions

# Opens the latest payroll request PDF for the logged-in user 
@login_required
def view_payroll_pdf(request):
    payroll = PayrollAssignment.objects.filter(user=request.user, pdf_url__isnull=False).order_by('-id').first()
    return handle_form_pdf_response(request, payroll, "latexform/payroll-assignment.tex")

# Open latest payroll form base on user
@login_required
def view_payroll_pdf2(request, user_id):    
    # Get the latest payroll request with a generated PDF URL
    payroll = PayrollAssignment.objects.filter(id=user_id, pdf_url__isnull=False).order_by('-id').first()
    return handle_form_pdf_response(request, payroll, "latexform/payroll-assignment.tex")

# Get the latest reimbursement request for logged in user
@login_required
def view_reimbursement_pdf(request):
    reimbursement = ReimbursementRequest.objects.filter(
        user=request.user,
        pdf_url__isnull=False
    ).order_by('-id').first()
    return handle_form_pdf_response(request, reimbursement, "latexform/reimburse.tex")

# Open latest form base on user
@login_required
def view_reimbursement_pdf2(request, user_id):
    # Get the latest reimbursement for the specified user
    reimbursement = ReimbursementRequest.objects.filter(id=user_id, pdf_url__isnull=False).order_by('-id').first()
    return handle_form_pdf_response(request, reimbursement, "latexform/reimburse.tex")

# Open specific form base on id
@login_required
def view_payroll_pdf3(request, form_id):
    # Retrieve the payroll form using its specific form ID (and ensure pdf_url is set)
    payroll = get_object_or_404(PayrollAssignment, id=form_id, pdf_url__isnull=False)
    return handle_form_pdf_response(request, payroll, "latexform/payroll-assignment.tex")

# Open specific form base on id
@login_required
def view_reimbursement_pdf3(request, form_id):
    # Retrieve the reimbursement form using its specific form ID (and ensure pdf_url is set)
    reimbursement = get_object_or_404(ReimbursementRequest, id=form_id, pdf_url__isnull=False)
    return handle_form_pdf_response(request, reimbursement, "latexform/reimburse.tex")

# Opens the latest diploma request PDF for the logged-in user
@login_required
def view_diploma_pdf(request):
    diploma = DiplomaRequest.objects.filter(
        user=request.user,
        pdf_url__isnull=False
    ).order_by('-id').first()
    return handle_form_pdf_response(request, diploma, "latexform/diploma.tex")
    
# Open diploma form using its specific form ID 
@login_required
def view_diploma_pdf3(request, form_id):
    diploma = get_object_or_404(DiplomaRequest, id=form_id, pdf_url__isnull=False)
    return handle_form_pdf_response(request, diploma, "latexform/diploma.tex")

#  Opens the latest change of address PDF for the logged-in user
@login_required
def view_change_address_pdf(request):
    address = ChangeOfAddress.objects.filter(
        user=request.user,
        pdf_url__isnull=False
    ).order_by('-id').first()

    return handle_form_pdf_response(request, address, "latexform/change_address.tex")

# Open change of address form using its specific form ID
@login_required
def view_change_address_pdf3(request, form_id):
    address = get_object_or_404(ChangeOfAddress, id=form_id, pdf_url__isnull=False)
    return handle_form_pdf_response(request, address, "latexform/change_address.tex")
 