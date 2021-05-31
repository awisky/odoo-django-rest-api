from django.contrib import admin
from .models import Document, Odoo, OcrElement

admin.site.register(Odoo)


class OCRElementInline(admin.TabularInline):
    model = OcrElement
    extra = 0
    fields = ["text", "rectangle"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["name", "text", "file", "mimetype",
                    "ocr_processed", "odoo_sent", "created_by",
                    "res_model", "res_id"]
    search_fields = ["name", "text", "file", "mimetype",
                     "ocr_processed", "odoo_sent", "created_by",
                     "res_model", "res_id"]
    inlines = [
        OCRElementInline]
