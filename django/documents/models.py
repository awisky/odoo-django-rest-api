from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Document(models.Model):
    name = models.CharField(max_length=60)
    text = models.TextField(null=True, blank=True)
    file = models.FileField(blank=False, null=True)
    mimetype = models.CharField(max_length=60, null=True)
    ocr_processed = models.BooleanField(default=False)

    # res model linked to the document
    res_model = models.CharField(max_length=60, null=True)
    res_id = models.IntegerField(default=0)

    # odoo fields
    odoo_sent = models.BooleanField(default=False)
    odoo_id = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return self.name


class Odoo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    odoo_url = models.CharField(max_length=100, blank=True)
    odoo_user = models.CharField(max_length=30, blank=True)
    odoo_password = models.CharField(max_length=30, blank=True)
    odoo_database = models.CharField(max_length=30, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Odoo.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.odoo.save()

    def __str__(self):
        return self.user.__str__()
