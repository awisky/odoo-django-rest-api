from rest_framework import viewsets

from .serializers import DocumentSerializer
from .models import Document


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('name')
    serializer_class = DocumentSerializer
