# Generated by Django 2.2.28 on 2023-08-05 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20230804_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='registration_date',
        ),
        migrations.RemoveField(
            model_name='seller',
            name='registration_date',
        ),
    ]