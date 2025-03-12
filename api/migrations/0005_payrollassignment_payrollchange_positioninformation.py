# Generated by Django 5.1.6 on 2025-03-12 06:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_user_accs_address_alter_user_accs_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=100)),
                ('employee_id', models.CharField(max_length=50)),
                ('todays_date', models.DateField()),
                ('education_level', models.CharField(choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('PostDoc', 'PostDoc')], max_length=20)),
                ('requested_action', models.CharField(choices=[('New Hire', 'New Hire'), ('Rehire/Transfer', 'Rehire/Transfer'), ('Payroll Change', 'Payroll Change')], max_length=20)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('signature_url', models.URLField(blank=True, null=True)),
                ('approve_date', models.DateField(blank=True, null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PayrollChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('payroll_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payroll_changes', to='api.payrollassignment')),
            ],
        ),
        migrations.CreateModel(
            name='PositionInformation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('salary_value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('salary_unit', models.CharField(blank=True, choices=[('Monthly', 'Monthly'), ('Hourly', 'Hourly')], max_length=20, null=True)),
                ('fte', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('speed_type', models.CharField(blank=True, max_length=50, null=True)),
                ('budget_percentage', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('position_title', models.CharField(blank=True, max_length=100, null=True)),
                ('benefits_type', models.CharField(blank=True, choices=[('Benefits Eligible', 'Benefits Eligible'), ('NonBenefits Eligible', 'NonBenefits Eligible'), ('Insurance Only', 'Insurance Only')], max_length=30, null=True)),
                ('pcn', models.CharField(blank=True, max_length=50, null=True)),
                ('payroll_assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='api.payrollassignment')),
            ],
        ),
    ]
