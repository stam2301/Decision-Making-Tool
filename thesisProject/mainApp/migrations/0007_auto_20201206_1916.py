# Generated by Django 3.1.2 on 2020-12-06 17:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_auto_20201201_0454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='input_file',
            field=models.FileField(upload_to='inputs', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['json'])]),
        ),
        migrations.AlterField(
            model_name='method',
            name='output_file',
            field=models.FileField(upload_to='outputs'),
        ),
    ]
