# Generated by Django 5.1.6 on 2025-02-18 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_accs',
            name='last_login',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
