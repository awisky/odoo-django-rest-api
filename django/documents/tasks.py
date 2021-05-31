
from celery import shared_task
from .models import Document, Odoo, OcrElement
from django.contrib.gis.geos import Polygon

import easyocr
from pdf2image import convert_from_path
import xmlrpc.client
import logging

_logger = logging.getLogger(__name__)


@shared_task
def process_ocr():
    docs = Document.objects.filter(ocr_processed=False)
    _logger.info('=======Process OCR Task========')
    buffer_image = '/code/rest/mediafiles/buffer.jpg'
    for doc in docs:
        path = doc.file.path
        text = ''
        reader = easyocr.Reader(lang_list=['pt'])
        if doc.file:
            if doc.mimetype == 'application/pdf':
                pages = convert_from_path(path, 500)
                _logger.info('Doc %s:%s pages:%s' %
                             (doc.name, path, len(pages)))
                for page in pages:
                    page.save(buffer_image, 'JPEG')
                    data = reader.readtext(buffer_image)
                    for element in data:
                        text += element[1]+' '
                        linear = element[0]
                        linear.append(linear[0])
                        _logger.info('linear? %s' % str(linear))
                        linear = tuple([tuple(x) for x in linear])
                        _logger.info('linear? %s' % str(linear))
                        polygon = Polygon(linear)
                        e = OcrElement(
                            text=element[1], document=doc, rectangle=polygon)
                        e.save()
            elif doc.mimetype in ['image/jpeg', 'image/png']:
                data = reader.readtext(path)
                for element in data:
                    text += element[1]+' '
                    linear = element[0]
                    linear.append(linear[0])
                    _logger.info('linear? %s' % str(linear))
                    linear = tuple([tuple(x) for x in linear])
                    _logger.info('linear? %s' % str(linear))
                    polygon = Polygon(linear)
                    e = OcrElement(
                        text=element[1], document=doc, rectangle=polygon)
                    e.save()
        if text:
            doc.text = text
        doc.ocr_processed = True
        doc.save()
    _logger.info('=======End Process OCR Task========')


@shared_task
def process_odoo():
    docs = Document.objects.filter(ocr_processed=True,
                                   odoo_sent=True, odoo_id__gt=0)
    _logger.info('=======Process Odoo Learn Task========')
    for doc in docs:

        profile = Odoo.objects.filter(user=doc.created_by)
        profile = profile and profile[0]
        if profile:
            url = profile.odoo_url
            db = profile.odoo_database
            user = profile.odoo_user
            password = profile.odoo_password
            _logger.info('=======Profile> %s %s %s %s' %
                         (url, db, user, password))
            common = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url))
            # if (url and db and user and password):
            #     continue
            uid = common.authenticate(db, user, password, {})
            _logger.info('=======logged in %s' % uid)
            models = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url))
            models.execute_kw(db, uid, password, 'documents.document', 'write', [[doc.odoo_id], {
                'ocr_text': doc.text or ''
            }])
            doc.odoo_sent = True
            doc.save()
    _logger.info('=======End Odoo Learn Process Task========')


@shared_task
def process_odoo_learn():
    docs = Document.objects.filter(ocr_processed=True,
                                   odoo_sent=True, odoo_id__gt=0)
    _logger.info('=======Process Odoo Task========')
    for doc in docs:

        profile = Odoo.objects.filter(user=doc.created_by)
        profile = profile and profile[0]
        if profile:
            url = profile.odoo_url
            db = profile.odoo_database
            user = profile.odoo_user
            password = profile.odoo_password
            _logger.info('=======Profile> %s %s %s %s' %
                         (url, db, user, password))
            common = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/common'.format(url))
            # if (url and db and user and password):
            #     continue
            uid = common.authenticate(db, user, password, {})
            models = xmlrpc.client.ServerProxy(
                '{}/xmlrpc/2/object'.format(url))
            result = models.execute_kw(db, uid, password,
                                       'documents.document', 'search_read',
                                       [[['id', '=', doc.odoo_id]]],
                                       {'fields': ['name', 'partner_id', 'res_model', 'res_id'], 'limit': 1})
            if result:
                res_model = result[0]['res_model']
                res_id = result[0]['res_id']
                doc.res_model = res_model
                doc.res_id = res_id
                doc.save()
                res = models.execute_kw(db, uid, password,
                                        res_model, 'search_read',
                                        [[['id', '=', res_id]]],
                                        {'fields': ['partner_id'], 'limit': 1})
                _logger.info('learning partner of this document %s' % res)

    _logger.info('=======End Odoo Process Task========')


@shared_task
def process_doc_check():
    docs = Document.objects.filter(ocr_processed=True,
                                   odoo_id__gt=0)
    _logger.info('=======Process Doc Check========')
    labels = ['Segurança']
    for doc in docs:

        elements = OcrElement.objects.filter(document=doc)
        for element in elements:
            if element.text in labels:
                _logger.info('Label found %s:%s' %
                             (element.text, element.rectangle))

    _logger.info('=======End Doc Check Task========')
