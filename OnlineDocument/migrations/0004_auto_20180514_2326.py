# Generated by Django 2.0.5 on 2018-05-14 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineDocument', '0003_auto_20180514_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to='static/document/pdf/%Y/%M', verbose_name='PDF'),
        ),
    ]
