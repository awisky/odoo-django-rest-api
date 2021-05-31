# © 2021 Agustin Wisky (<https://github.com/awisky>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class DocumentFolder(models.Model):
    _inherit = 'documents.folder'

    ocr_sync = fields.Boolean()
