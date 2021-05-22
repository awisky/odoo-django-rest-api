# serializers.py
from rest_framework import serializers

from .models import Document

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('name', 'alias')