# Generated by Django 2.2.28 on 2023-08-04 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_form', '0007_alter_property_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]