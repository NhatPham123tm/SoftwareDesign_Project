# Generated by Django 5.1.6 on 2025-03-19 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payrollassignment',
            name='is_terminated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='payrollassignment',
            name='benefits_type1',
            field=models.CharField(blank=True, choices=[('Eligible', 'Eligible'), ('Not Eligible', 'Not Eligible'), ('Insurance', 'Insurance')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='payrollassignment',
            name='benefits_type2',
            field=models.CharField(blank=True, choices=[('Eligible', 'Eligible'), ('Not Eligible', 'Not Eligible'), ('Insurance', 'Insurance')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='payrollassignment',
            name='education_level',
            field=models.CharField(choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('PostDoc', 'PostDoc'), ('Other', 'Other')], max_length=20),
        ),
    ]
