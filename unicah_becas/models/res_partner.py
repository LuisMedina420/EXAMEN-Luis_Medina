from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    beca_ids = fields.One2many(
        "unicah.beca",
        "partner_id",
        string="Solicitudes de beca",
    )
    tiene_beca_activa = fields.Boolean(
        string="Tiene beca aprobada",
        compute="_compute_tiene_beca_activa",
        store=True,
    )

    @api.depends("beca_ids.estado")
    def _compute_tiene_beca_activa(self):
        for partner in self:
            partner.tiene_beca_activa = any(
                b.estado == "aprobada" for b in partner.beca_ids
            )
