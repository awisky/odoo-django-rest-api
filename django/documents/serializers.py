# serializers.py
from rest_framework import serializers

from .models import Document

import logging

_logger = logging.getLogger(__name__)


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'text', 'file',
                  'ocr_processed', 'odoo_sent', 'odoo_id', 'mimetype',
                  'created_by')
        extra_kwargs = {'created_by': {
            'default': serializers.CurrentUserDefault()}}
