from django import forms

class PDFForm(forms.Form):
    name = forms.CharField(max_length=100)
    empl_id = forms.CharField(max_length=50)
    reimbursement_items = forms.CharField(widget=forms.Textarea)
    purpose = forms.CharField(widget=forms.Textarea)
    meal_info = forms.CharField(widget=forms.Textarea, required=False)
    cost_center_1 = forms.CharField(max_length=50)
    amount_1 = forms.CharField(max_length=20)
    cost_center_2 = forms.CharField(max_length=50, required=False)
    amount_2 = forms.CharField(max_length=20, required=False)
    total_reimbursement = forms.CharField(max_length=20)
