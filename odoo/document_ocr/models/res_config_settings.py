# © 2021 Agustin Wisky (<https://github.com/awisky>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from ast import literal_eval
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ocr_connector_id = fields.Many2one('ocr.connector')

    @api.model
    def get_values(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        res = super(ResConfigSettings, self).get_values()
        ocr_connector_id = literal_eval(ICPSudo.get_param(
            'kranz_ocr.ocr_connector_id',
            default='False'))
        res.update(
            ocr_connector_id=ocr_connector_id,
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        ICPSudo.set_param("kranz_ocr.ocr_connector_id",
                          self.ocr_connector_id.id)
