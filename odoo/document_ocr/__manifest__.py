# © 2021 Agustin Wisky (<https://github.com/awisky>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Document OCR",
    "summary": "OCR document management.",
    "version": "14.0.1.0.0",
    "category": "Localization",
    'author': "Agustin wisky",
    'website': "https://github.com/awisky",
    "depends": [
        'documents',
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/ir_cron_data.xml',
        'data/document_data.xml',
        'views/document.xml',
        'views/ocr_connector_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
