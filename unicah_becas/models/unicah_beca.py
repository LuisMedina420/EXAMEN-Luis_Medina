from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

TIPOS_BECA = [
    ("excelencia", "Excelencia Académica"),
    ("deportiva", "Deportiva / Cultural"),
    ("socioeconomica", "Apoyo Socioeconómico"),
]


class UnicahBeca(models.Model):
    _name = "unicah.beca"
    _description = "Solicitud de beca estudiantil UNICAH"

    name = fields.Char(string="Código de solicitud", required=True)
    partner_id = fields.Many2one(
        "res.partner",
        string="Estudiante",
        required=True,
        domain="[('tipo_cliente', '=', 'estudiante')]",
    )
    numero_cuenta = fields.Char(
        related="partner_id.numero_cuenta",
        string="Número de cuenta",
        readonly=True,
    )
    carrera = fields.Char(
        related="partner_id.carrera",
        string="Carrera",
        readonly=True,
    )
    periodo = fields.Char(string="Período académico", required=True, default="2026-I")
    tipo_beca = fields.Selection(
        TIPOS_BECA,
        string="Tipo de beca",
        required=True,
        default="excelencia",
    )
    indice_academico = fields.Float(string="Índice académico (%)", required=True, default=90.0)
    costo_mensualidad = fields.Float(string="Mensualidad base (L.)", required=True, default=4500.0)
    porcentaje_beca = fields.Float(
        string="Beca otorgada (%)",
        compute="_compute_montos_beca",
        store=True,
    )
    monto_descuento = fields.Float(
        string="Ahorro mensual (L.)",
        compute="_compute_montos_beca",
        store=True,
    )
    pago_neto = fields.Float(
        string="Cuota neta a pagar (L.)",
        compute="_compute_montos_beca",
        store=True,
    )
    estado = fields.Selection(
        [
            ("borrador", "En revisión"),
            ("aprobada", "Aprobada"),
            ("rechazada", "Rechazada"),
        ],
        string="Estado",
        default="borrador",
        required=True,
    )

    @api.depends("tipo_beca", "indice_academico", "costo_mensualidad")
    def _compute_montos_beca(self):
        for beca in self:
            if beca.tipo_beca == "excelencia":
                if beca.indice_academico >= 95:
                    porcentaje = 50.0
                elif beca.indice_academico >= 90:
                    porcentaje = 35.0
                elif beca.indice_academico >= 85:
                    porcentaje = 25.0
                else:
                    porcentaje = 0.0
            elif beca.tipo_beca == "deportiva":
                porcentaje = 20.0 if beca.indice_academico >= 75 else 0.0
            else:
                porcentaje = 30.0 if beca.indice_academico >= 70 else 0.0

            beca.porcentaje_beca = porcentaje
            beca.monto_descuento = beca.costo_mensualidad * (porcentaje / 100.0)
            beca.pago_neto = beca.costo_mensualidad - beca.monto_descuento

    @api.constrains("indice_academico", "tipo_beca", "costo_mensualidad")
    def _check_requisitos_beca(self):
        for beca in self:
            if beca.indice_academico <= 0 or beca.indice_academico > 100:
                raise ValidationError(
                    "El índice académico debe estar entre 1 % y 100 %."
                )
            if beca.costo_mensualidad <= 0:
                raise ValidationError(
                    "La mensualidad base debe ser mayor que cero."
                )
            if beca.tipo_beca == "excelencia" and beca.indice_academico < 85:
                raise ValidationError(
                    "Para optar a la Beca de Excelencia Académica, el estudiante debe tener "
                    "un índice académico mínimo de 85 %."
                )
            if beca.tipo_beca == "deportiva" and beca.indice_academico < 75:
                raise ValidationError(
                    "Para optar a la Beca Deportiva / Cultural, el índice mínimo es de 75 %."
                )

    def action_aprobar(self):
        for beca in self:
            duplicada = self.search([
                ("id", "!=", beca.id),
                ("partner_id", "=", beca.partner_id.id),
                ("periodo", "=", beca.periodo),
                ("estado", "=", "aprobada"),
            ], limit=1)
            if duplicada:
                raise UserError(
                    f"El estudiante {beca.partner_id.name} ya tiene una beca aprobada "
                    f"({duplicada.name}) en el período {beca.periodo}."
                )
            beca.estado = "aprobada"

    def action_rechazar(self):
        for beca in self:
            beca.estado = "rechazada"
