# © 2021 Agustin Wisky (<https://github.com/awisky>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, _, fields, api
from ast import literal_eval
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class DocumentsDocument(models.Model):
    _inherit = 'documents.document'

    ocr_sent = fields.Boolean()
    ocr_text = fields.Text()

    def _get_default_connector(self):
        """
        Returns the default configured OCR Connector
        """
        ICPSudo = self.env['ir.config_parameter'].sudo()
        connector_id = literal_eval(ICPSudo.get_param(
            'document_ocr.ocr_connector_id', default='False'
        ))
        ocr_connector = None
        if connector_id:
            ocr_connector = self.env['ocr.connector'].browse(connector_id)
        return ocr_connector

    def action_set_to_send(self):
        """
        This action reset the document ocr fields
        """
        for doc in self:
            doc.ocr_sent = False
            doc.ocr_text = ''

    def action_send(self):
        """
        This action sends the document
        """
        self.ensure_one()
        ocr_connector = self._get_default_connector()
        if ocr_connector:
            response = ocr_connector.sendDocument(self)
            if response:
                self.ocr_sent = True
        else:
            raise ValidationError(_(
                "You must define a default OCR connector "
                "to execute this action "
            ))

    @api.model
    def _send_to_ocr(self):
        """
        This method is called from the cron job.
        """
        documents = self.search([
            ('ocr_sent', '=', False),
            ('mimetype', 'in', ('application/pdf', 'image/jpeg', 'image/png')),
            ('folder_id.ocr_sync', '=', True)
        ])
        _logger.info("OCR Status Check documents (%s)" % len(documents))
        if documents:
            for document in documents:
                document.action_send()
