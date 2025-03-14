import os
import subprocess
from django.shortcuts import render
from django.http import FileResponse, HttpResponse
from .forms import RimburseForm, PayrollForm
# For testing need improvement
def generate_reimburse_pdf(request):
    LATEX_TEMPLATE_PATH = "latexform/reimburse.tex"
    OUTPUT_PDF_PATH = "output/filled_template.pdf"
    if request.method == 'POST':
        form = RimburseForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            empl_id = form.cleaned_data['empl_id']
            reimbursement_items = form.cleaned_data['reimbursement_items']
            purpose = form.cleaned_data['purpose']
            meal_info = form.cleaned_data['meal_info']
            cost_center_1 = form.cleaned_data['cost_center_1']
            amount_1 = form.cleaned_data['amount_1']
            cost_center_2 = form.cleaned_data['cost_center_2']
            amount_2 = form.cleaned_data['amount_2']
            total_reimbursement = form.cleaned_data['total_reimbursement']

            # Read LaTeX template
            with open(LATEX_TEMPLATE_PATH, "r") as file:
                tex_content = file.read()

            # Replace placeholders with user input
            tex_content = tex_content.replace("{{NAME}}", name)
            tex_content = tex_content.replace("{{EMPL_ID}}", empl_id)
            tex_content = tex_content.replace("{{REIMBURSEMENT_ITEMS}}", reimbursement_items)
            tex_content = tex_content.replace("{{PURPOSE}}", purpose)
            tex_content = tex_content.replace("{{MEAL_INFO}}", meal_info)
            tex_content = tex_content.replace("{{COST_CENTER_1}}", cost_center_1)
            tex_content = tex_content.replace("{{AMOUNT_1}}", amount_1)
            tex_content = tex_content.replace("{{COST_CENTER_2}}", cost_center_2)
            tex_content = tex_content.replace("{{AMOUNT_2}}", amount_2)
            tex_content = tex_content.replace("{{TOTAL_REIMBURSEMENT}}", total_reimbursement)

            # Save modified LaTeX file
            filled_tex_path = "output/filled_template.tex"
            with open(filled_tex_path, "w") as file:
                file.write(tex_content)

            # Run Makefile to generate PDF
            try:
                subprocess.run(["make", "pdf"], check=True)
            except subprocess.CalledProcessError as e:
                return HttpResponse(f"Error generating PDF: {e}", status=500)

            # Serve PDF as response
            return FileResponse(open(OUTPUT_PDF_PATH, "rb"), content_type="application/pdf")

    else:
        form = RimburseForm()
    return render(request, 'form.html', {'form': form})

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