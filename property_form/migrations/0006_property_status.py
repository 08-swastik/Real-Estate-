# Generated by Django 4.2 on 2023-07-29 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property_form', '0005_property_is_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('sold', 'Sold')], default='available', max_length=20),
        ),
    ]