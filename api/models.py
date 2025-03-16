from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class roles(models.Model):
    role_name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.role_name

class user_accs(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('active', 'active'),
        ('inactive', 'inactive'),
        ('banned', 'banned'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)  # Store hashed passwords
    role = models.ForeignKey(roles, on_delete=models.SET_DEFAULT, default=2)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.CharField(max_length=255, unique=False, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    # Required fields for Django Authentication
    last_login = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)  # Needed for Django authentication
    is_staff = models.BooleanField(default=False)  # Needed for Django admin access
    USERNAME_FIELD = 'email'  # Email will be used as the unique identifier
    REQUIRED_FIELDS = ['name']  # Required fields for createsuperuser
    def __str__(self):
        return self.name
    
    def set_password(self, raw_password):
        """ Set the password by hashing it """
        self.password_hash = make_password(raw_password)

    def save(self, *args, **kwargs):
        # Ensure password is hashed before saving
        if not self.password_hash.startswith('pbkdf2_sha256$'):  
            self.password_hash = make_password(self.password_hash)
        super().save(*args, **kwargs)

class permission(models.Model):
    role = models.ForeignKey(roles, on_delete=models.CASCADE)
    permission_detail = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.role.role_name} - {self.permission_detail}"


class PayrollAssignment(models.Model):
    EDUCATION_LEVEL_CHOICES = [
        ('Undergraduate', 'Undergraduate'),
        ('Graduate', 'Graduate'),
        ('PostDoc', 'PostDoc'),
    ]
    REQUESTED_ACTION_CHOICES = [
        ('New Hire', 'New Hire'),
        ('Rehire/Transfer', 'Rehire/Transfer'),
        ('Payroll Change', 'Payroll Change'),
    ]
    FORM_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(user_accs, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=50)
    todays_date = models.DateField()
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES)
    requested_action = models.CharField(max_length=20, choices=REQUESTED_ACTION_CHOICES)

    job_title = models.CharField(max_length=100, blank=True, null=True)
    position_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Termination 
    termination_date = models.DateField(blank=True, null=True)
    termination_reason = models.TextField(blank=True, null=True)
    
    # Budget change 
    budget_change_effective_date = models.DateField(blank=True, null=True)
    from_speed_type = models.CharField(max_length=50, blank=True, null=True)
    to_speed_type = models.CharField(max_length=50, blank=True, null=True)
    
    # FTE change 
    fte_change_effective_date = models.DateField(blank=True, null=True)
    from_fte = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    to_fte = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Pay rate change 
    pay_rate_change_effective_date = models.DateField(blank=True, null=True)
    current_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    new_pay_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    pay_rate_change_reason = models.TextField(blank=True, null=True)
    
    # Reallocation 
    reallocation_dates = models.TextField(blank=True, null=True)
    reallocation_from_position = models.CharField(max_length=50, blank=True, null=True)
    reallocation_to_position = models.CharField(max_length=50, blank=True, null=True)
    
    # Other payroll change
    other_specification = models.TextField(blank=True, null=True)

    # Verification
    status = models.CharField(max_length=20, choices=FORM_STATUS, default='Pending')
    signature_url = models.URLField(blank=True, null=True)
    approve_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.id} ({self.employee_name})"


class PositionInformation(models.Model):
    BENEFITS_TYPE_CHOICES = [
        ('Benefits Eligible', 'Benefits Eligible'),
        ('NonBenefits Eligible', 'NonBenefits Eligible'),
        ('Insurance Only', 'Insurance Only'),
    ]
    SALARY_UNIT_CHOICES = [
        ('Monthly', 'Monthly'),
        ('Hourly', 'Hourly'),
    ]
    
    payroll_assignment = models.ForeignKey(
        PayrollAssignment, on_delete=models.CASCADE, related_name='positions'
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    salary_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    salary_unit = models.CharField(max_length=20, choices=SALARY_UNIT_CHOICES, blank=True, null=True)
    fte = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    speed_type = models.CharField(max_length=50, blank=True, null=True)
    budget_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    position_title = models.CharField(max_length=100, blank=True, null=True)
    benefits_type = models.CharField(max_length=30, choices=BENEFITS_TYPE_CHOICES, blank=True, null=True)
    pcn = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"Position for {self.payroll_assignment.id} {self.payroll_assignment.employee_name}"

class ReimbursementRequest(models.Model):
    FORM_STATUS = [
        ('Draft', 'Draft'),
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(user_accs, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    today_date = models.DateField(blank=True, null=True)
    reimbursement_items = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    meal_info = models.TextField(blank=True, null=True)
    
    # Cost Center Information
    cost_center_1 = models.CharField(max_length=50, blank=True, null=True)
    amount_1 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cost_center_2 = models.CharField(max_length=50, blank=True, null=True)
    amount_2 = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    total_reimbursement = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Approval Process
    status = models.CharField(max_length=20, choices=FORM_STATUS, default='Draft')
    signature_url = models.URLField(blank=True, null=True)
    approve_date = models.DateField(blank=True, null=True)
    pdf_url = models.URLField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'], condition=models.Q(status="Pending"),
                name='unique_pending_reimbursement_per_user'
            )
        ]

    def __str__(self):
        return f"Reimbursement {self.id} - {self.status}"

    def clean(self):
        """ Ensure only one 'Pending' form per user """
        if self.status == "Pending":
            existing_pending = ReimbursementRequest.objects.filter(user=self.user, status="Pending").exclude(id=self.id)
            if existing_pending.exists():
                raise ValidationError("You can only have one pending reimbursement request at a time.")

    def save(self, *args, **kwargs):
        self.clean()  # Enforce constraint before saving
        super().save(*args, **kwargs)