# Generated by Django 5.1.6 on 2025-03-19 03:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='roles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='user_accs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password_hash', models.CharField(max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('banned', 'banned')], default='active', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_login', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('role', models.ForeignKey(default=2, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.roles')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PayrollAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_url', models.URLField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('employee_name', models.CharField(max_length=100)),
                ('employee_id', models.CharField(max_length=50)),
                ('todays_date', models.DateField()),
                ('education_level', models.CharField(choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('PostDoc', 'PostDoc')], max_length=20)),
                ('requested_action', models.CharField(choices=[('New Hire', 'New Hire'), ('Rehire/Transfer', 'Rehire/Transfer'), ('Payroll Change', 'Payroll Change')], max_length=20)),
                ('start_date1', models.DateField(blank=True, null=True)),
                ('end_date1', models.DateField(blank=True, null=True)),
                ('salary1', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fte1', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('speed_type1', models.CharField(blank=True, max_length=50, null=True)),
                ('budget_percentage1', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('position_title1', models.CharField(blank=True, max_length=100, null=True)),
                ('benefits_type1', models.CharField(blank=True, choices=[('eligible', 'Eligible'), ('no_eligible', 'Not Eligible'), ('insurance', 'Insurance')], max_length=30, null=True)),
                ('pcn1', models.CharField(blank=True, max_length=50, null=True)),
                ('start_date2', models.DateField(blank=True, null=True)),
                ('end_date2', models.DateField(blank=True, null=True)),
                ('salary2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('fte2', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('speed_type2', models.CharField(blank=True, max_length=50, null=True)),
                ('budget_percentage2', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('position_title2', models.CharField(blank=True, max_length=100, null=True)),
                ('benefits_type2', models.CharField(blank=True, choices=[('eligible', 'Eligible'), ('no_eligible', 'Not Eligible'), ('insurance', 'Insurance')], max_length=30, null=True)),
                ('salary_fte1', models.CharField(blank=True, max_length=50, null=True)),
                ('pcn2', models.CharField(blank=True, max_length=50, null=True)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('position_number', models.CharField(blank=True, max_length=50, null=True)),
                ('termination_date', models.DateField(blank=True, null=True)),
                ('termination_reason', models.TextField(blank=True, null=True)),
                ('budget_change_effective_date', models.DateField(blank=True, null=True)),
                ('from_speed_type', models.CharField(blank=True, max_length=50, null=True)),
                ('to_speed_type', models.CharField(blank=True, max_length=50, null=True)),
                ('fte_change_effective_date', models.DateField(blank=True, null=True)),
                ('from_fte', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('to_fte', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('pay_rate_change_effective_date', models.DateField(blank=True, null=True)),
                ('current_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('new_pay_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('pay_rate_change_reason', models.TextField(blank=True, null=True)),
                ('reallocation_dates', models.TextField(blank=True, null=True)),
                ('reallocation_from_position', models.CharField(blank=True, max_length=50, null=True)),
                ('reallocation_to_position', models.CharField(blank=True, max_length=50, null=True)),
                ('other_specification', models.TextField(blank=True, null=True)),
                ('signature_url', models.URLField(blank=True, null=True)),
                ('approve_date', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_detail', models.CharField(max_length=100, unique=True)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.roles')),
            ],
        ),
        migrations.CreateModel(
            name='ReimbursementRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(blank=True, max_length=100, null=True)),
                ('employee_id', models.CharField(blank=True, max_length=50, null=True)),
                ('today_date', models.DateField(blank=True, null=True)),
                ('reimbursement_items', models.TextField(blank=True, null=True)),
                ('purpose', models.TextField(blank=True, null=True)),
                ('meal_info', models.TextField(blank=True, null=True)),
                ('cost_center_1', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_1', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('cost_center_2', models.CharField(blank=True, max_length=50, null=True)),
                ('amount_2', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('total_reimbursement', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status', models.CharField(choices=[('Draft', 'Draft'), ('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Cancelled', 'Cancelled')], default='Draft', max_length=20)),
                ('signature_url', models.URLField(blank=True, null=True)),
                ('approve_date', models.DateField(blank=True, null=True)),
                ('pdf_url', models.URLField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'constraints': [models.UniqueConstraint(condition=models.Q(('status', 'Pending')), fields=('user',), name='unique_pending_reimbursement_per_user')],
            },
        ),
    ]