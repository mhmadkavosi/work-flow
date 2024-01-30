# Generated by Django 5.0.1 on 2024-01-27 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_requests_content_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requests',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('next', 'Next'), ('reject', 'Reject'), ('accept', 'Accept')], default='pending'),
        ),
        migrations.AlterField(
            model_name='requestshistory',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('next', 'Next'), ('reject', 'Reject'), ('accept', 'Accept')], default='pending'),
        ),
    ]
