# Generated by Django 3.1 on 2024-03-08 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Category', '0003_auto_20230408_0315'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscribeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscribers', models.ManyToManyField(to='Category.Category')),
            ],
        ),
    ]
