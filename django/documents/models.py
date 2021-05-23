from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=60)
    text = models.TextField(null=True, blank=True)
    file = models.FileField(blank=False, null=True)
    mimetype = models.CharField(max_length=60, null=True)
    ocr_processed = models.BooleanField(default=False)

    # odoo fields
    odoo_sent = models.BooleanField(default=False)
    odoo_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def ocr(self):
        self.text
