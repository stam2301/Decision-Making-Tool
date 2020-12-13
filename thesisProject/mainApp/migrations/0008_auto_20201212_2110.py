# Generated by Django 3.1.2 on 2020-12-12 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0007_auto_20201206_1916'),
    ]

    operations = [
        migrations.AddField(
            model_name='method',
            name='method_type',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='method',
            name='input_file',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='method',
            name='output_file',
            field=models.JSONField(),
        ),
    ]
