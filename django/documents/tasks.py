
from celery import shared_task
from .models import Document

import easyocr
from pdf2image import convert_from_path

import logging

_logger = logging.getLogger(__name__)

reader = easyocr.Reader(lang_list=['en'])


@shared_task
def process_ocr():
    docs = Document.objects.filter(text__isnull=True)
    _logger.info('=======Process Task========')
    _logger.info('Reader: %s' % reader)
    for doc in docs:
        path = doc.file.path
        _logger.info('Doc %s:%s' % (doc.name, path))
        try:
            text = ''
            data = reader.readtext(path)
            _logger.info('Page Data %s' % data)
            for element in data:
                text += element[1]+'\n'
            if text:
                doc.text = text
                doc.save()
        except Exception:
            print('handled')
            response = "bad response"
    _logger.info('=======End Process Task========')
