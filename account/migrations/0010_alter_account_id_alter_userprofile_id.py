# Generated by Django 4.2.7 on 2024-03-09 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_account_is_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]