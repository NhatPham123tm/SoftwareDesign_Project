# Generated by Django 5.1.6 on 2025-03-19 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payrollassignment',
            name='education_level',
            field=models.CharField(choices=[('Undergraduate', 'Undergraduate'), ('Graduate', 'Graduate'), ('PostDoc', 'PostDoc'), ('Other', 'Other')], max_length=20),
        ),
    ]
