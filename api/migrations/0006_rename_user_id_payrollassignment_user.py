# Generated by Django 5.1.6 on 2025-03-12 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_payrollassignment_payrollchange_positioninformation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payrollassignment',
            old_name='user_id',
            new_name='user',
        ),
    ]
