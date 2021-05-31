# Generated by Django 3.2.3 on 2021-05-23 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_auto_20210522_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='ocr_processed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='odoo_sent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]