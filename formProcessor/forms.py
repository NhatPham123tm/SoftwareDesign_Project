from django import forms
from api.models import ReimbursementRequest

class RimburseForm(forms.Form):
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

class PayrollForm(forms.Form):
    emp_name = forms.CharField(max_length=100)
    emp_id = forms.CharField(max_length=50)
    today_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    education_level = forms.ChoiceField(choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('PostDoc', 'PostDoc'), ('Other', 'Other')])
    requested_action = forms.ChoiceField(choices=[('newHire', 'New Hire'), ('rehireTransfer', 'Rehire/Transfer'), ('payrollChange', 'Payroll Change')])

    start_date1 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date1 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    salary1 = forms.CharField(max_length=20)
    fte1 = forms.CharField(max_length=10)
    speed_type1 = forms.CharField(max_length=50)
    budget_percent1 = forms.CharField(max_length=10)
    position_title1 = forms.CharField(max_length=100)
    benefit1 = forms.ChoiceField(choices=[('eligible', 'Eligible'), ('no_eligible', 'Not Eligible'), ('insurance', 'Insurance')])
    total_salary1 = forms.CharField(max_length=20)
    pcn1 = forms.CharField(max_length=50)

    start_date2 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    end_date2 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    salary2 = forms.CharField(max_length=20)
    fte2 = forms.CharField(max_length=10)
    speed_type2 = forms.CharField(max_length=50)
    budget_percent2 = forms.CharField(max_length=10)
    position_title2 = forms.CharField(max_length=100)
    benefit2 = forms.ChoiceField(choices=[('eligible', 'Eligible'), ('no_eligible', 'Not Eligible'), ('insurance', 'Insurance')])
    total_salary2 = forms.CharField(max_length=20)
    pcn2 = forms.CharField(max_length=50)

    job_title = forms.CharField(max_length=100, required=False)
    position_number = forms.CharField(max_length=50, required=False)
    termination_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    termination_reason = forms.CharField(max_length=200, required=False)
    
    EFFECTIVE_DATE1 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    FROM_SPEED1 = forms.CharField(max_length=10)
    TO_SPEED1 = forms.CharField(max_length=10)

    EFFECTIVE_DATE2 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    FTEFROM = forms.CharField(max_length=10)
    FTETO = forms.CharField(max_length=10)

    EFFECTIVE_DATE3 = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    CURRENT_RATE = forms.CharField(max_length=20)
    NEW_RATE = forms.CharField(max_length=20)
    RE_DATE = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    FROM_SPEED2 = forms.CharField(max_length=10)
    TO_SPEED2 = forms.CharField(max_length=10)
    OTHER = forms.CharField(max_length=100)

    SIGN_DATE = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)

# Implement with database model
class ReimbursementForm(forms.ModelForm):
    class Meta:
        model = ReimbursementRequest
        exclude = ['status', 'signature_url', 'approve_date']

# Implement with database model
class ReimbursementStep1Form(forms.ModelForm):
    class Meta:
        model = ReimbursementRequest
        fields = ['employee_name', 'employee_id', 'today_date']

class ReimbursementStep2Form(forms.ModelForm):
    class Meta:
        model = ReimbursementRequest
        fields = ['reimbursement_items', 'purpose', 'meal_info']

class ReimbursementStep3Form(forms.ModelForm):
    class Meta:
        model = ReimbursementRequest
        fields = ['cost_center_1', 'amount_1', 'cost_center_2', 'amount_2', 'total_reimbursement']