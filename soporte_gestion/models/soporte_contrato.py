from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class SoporteContrato(models.Model):
    _name = 'soporte.contrato'
    _description = 'Contrato de Suscripción de Soporte IT'
    # Habilitamos el chatter y las actividades automáticas
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # Usamos el campo 'name' como etiqueta principal
    _rec_name = 'name'

    # Referencia única autogenerada
    name = fields.Char(
        string='Referencia',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence']
                               .next_by_code('soporte.contrato')
    )
    # Cliente asociado al contrato
    partner_id = fields.Many2one(
        'res.partner',
        string='Cliente',
        required=True,
        tracking=True
    )
    # Periodicidad de la suscripción
    periodo = fields.Selection([
        ('mensual', 'Mensual'),
        ('trimestral', 'Trimestral'),
        ('anual', 'Anual'),
    ],
        string='Periodicidad',
        required=True,
        tracking=True
    )
    # Fecha de inicio y fin de la vigencia
    start_date = fields.Date(
        string='Fecha de Inicio',
        required=True,
        tracking=True
    )
    end_date = fields.Date(
        string='Fecha de Fin',
        required=True,
        tracking=True
    )
    # Duración en días, se calcula automáticamente
    duration_days = fields.Integer(
        string='Duración (días)',
        compute='_compute_duration',
        store=True
    )
    # Importe de la suscripción en la moneda de la compañía
    amount = fields.Monetary(
        string='Importe (€)',
        required=True,
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Moneda',
        default=lambda self: self.env.company.currency_id
    )
    # Estados por los que pasa el contrato
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('open', 'Activo'),
        ('expired', 'Expirado'),
        ('cancel', 'Cancelado'),
    ],
        string='Estado',
        default='draft',
        tracking=True
    )
    # Permite inactivar el contrato sin borrarlo
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Permite inactivar la suscripción sin borrarla.'
    )

    # Asegura que cada referencia sea única en base de datos
    _sql_constraints = [
        ('name_unique', 'unique(name)', 'La referencia debe ser única.')
    ]

    @api.onchange('periodo')
    def _onchange_periodo(self):
        """
        Ajusta automáticamente el importe según la periodicidad:
        - Mensual: 100 €
        - Trimestral: 250 €
        - Anual: 1000 €
        """
        if self.periodo:
            mapping = {'mensual': 100.0, 'trimestral': 250.0, 'anual': 1000.0}
            self.amount = mapping.get(self.periodo, 0.0)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        """
        Valida que:
        1) La fecha de inicio no sea posterior a la de fin.
        2) La fecha de fin no esté en el pasado.
        """
        for rec in self:
            if rec.start_date > rec.end_date:
                raise ValidationError(_('La fecha de inicio debe ser anterior a la fecha de fin.'))
            if rec.end_date < date.today():
                raise ValidationError(_('La fecha de fin no puede estar en el pasado.'))

    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        """
        Calcula y almacena la duración del contrato en días
        (incluye ambos extremos).
        """
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.duration_days = (rec.end_date - rec.start_date).days + 1
            else:
                rec.duration_days = 0

    def action_confirm(self):
        """
        Al confirmar el contrato:
        - Cambia el estado a 'Activo'.
        - Reactiva el contrato.
        - Crea una actividad recordatoria 30 días antes del fin para renovar.
        """
        for rec in self:
            rec.state = 'open'
            rec.active = True
            if rec.end_date:
                reminder = rec.end_date - timedelta(days=30)
                self.env['mail.activity'].create({
                    'res_model_id': self.env['ir.model']._get_id('soporte.contrato'),
                    'res_id': rec.id,
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('Renovar contrato %s') % rec.name,
                    'date_deadline': reminder,
                    'user_id': self.env.user.id,
                })

    def action_cancel(self):
        """
        Cancela el contrato:
        - Estado a 'Cancelado'.
        - Lo inactiva sin eliminarlo.
        """
        self.write({'state': 'cancel', 'active': False})

    @api.model
    def _cron_expirar_contratos(self):
        """
        Tarea programada (cron) que:
        - Busca contratos activos cuyo fin ya pasó.
        - Marca su estado como 'Expirado' e inactiva el registro.
        """
        hoy = date.today()
        expirar = self.search([('state', '=', 'open'), ('end_date', '<', hoy)])
        expirar.write({'state': 'expired', 'active': False})
