# Generated by Django 4.2.4 on 2023-08-15 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property_form', '0011_alter_property_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=100)),
                ('payment_status', models.CharField(max_length=50)),
                ('amount_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property_form.property')),
            ],
        ),
    ]