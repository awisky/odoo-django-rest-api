from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=60)
    text = models.TextField(null=True)
    file = models.FileField(blank=False, null=True)

    def __str__(self):
        return self.name

    def ocr(self):
        self.text
