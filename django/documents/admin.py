from django.contrib import admin
from .models import Document, Odoo

admin.site.register(Odoo)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["name", "text", "file", "mimetype",
                    "ocr_processed", "odoo_sent", "created_by",
                    "res_model", "res_id"]
    search_fields = ["name", "text", "file", "mimetype",
                     "ocr_processed", "odoo_sent", "created_by",
                     "res_model", "res_id"]
