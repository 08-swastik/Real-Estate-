# Generated by Django 4.2.1 on 2023-05-12 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_seller_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seller',
            name='user',
        ),
        migrations.AddField(
            model_name='seller',
            name='username',
            field=models.CharField(default=3, max_length=150, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='seller',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
