# Generated by Django 4.2.1 on 2023-05-13 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_remove_seller_username_seller_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='username',
            field=models.CharField(default=3, max_length=150),
            preserve_default=False,
        ),
    ]
