# Generated by Django 3.2.3 on 2021-05-24 05:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('documents', '0007_rename_mime_type_document_mimetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='Odoo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('odoo_url', models.CharField(blank=True, max_length=30)),
                ('odoo_user', models.CharField(blank=True, max_length=30)),
                ('odoo_password', models.CharField(blank=True, max_length=30)),
                ('odoo_database', models.CharField(blank=True, max_length=30)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]