# © 2021 Agustin Wisky (<https://github.com/awisky>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import requests
from requests import Session
from requests.auth import HTTPBasicAuth
from odoo import fields, models, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class OCRConnector(models.Model):
    """
    OCR connector 
    """
    _name = 'ocr.connector'
    _description = "OCR connector"

    name = fields.Char(
        help="A user-defined name for the OCR connector", required=True)
    service_url = fields.Char(required=True)
    user = fields.Char(required=True)
    token = fields.Char(required=True)

    def sendDocument(self, document):
        """
        This operation sends the document to OCR to be processed
        """

        headers = {'Authorization': 'Token '+self.token}

        files = {
            'file': (document.name, document.attachment_id.raw,
                     document.attachment_id.mimetype)}

        data = {'name': document.name, 'file': files, 'mimetype':
                document.attachment_id.mimetype, 'odoo_id': document.id}

        response = requests.post(
            self.service_url, headers=headers, files=files, data=data)
        _logger.debug(response)
        return response
