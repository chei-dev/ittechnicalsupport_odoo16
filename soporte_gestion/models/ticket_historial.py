from odoo import models, fields, api

class TicketHistorial(models.Model):
    _name = 'ticket.historial'
    _description = 'Historial de Incidencias'

    # Enlaza cada registro de historial con su incidencia (ticket)
    incidencia_id = fields.Many2one(
        'ticket.incidencia',
        string='Incidencia',
        required=True,
        ondelete='cascade',  # Si borras el ticket, borras también su historial
    )

    # Fecha y hora en que se guarda la entrada de historial
    date = fields.Datetime(
        string='Fecha',
        default=fields.Datetime.now,
        readonly=True,       # No editable una vez creado
    )

    # Quién creó la entrada de historial
    user_id = fields.Many2one(
        'res.users',
        string='Usuario',
        default=lambda self: self.env.user,  # Por defecto, el usuario actual
        readonly=True,
    )

    # Detalle o nota que se quiere dejar en el historial
    notes = fields.Text(
        string='Notas',
        required=True,       # Obligatorio para no tener entradas vacías
    )

    @api.model
    def create(self, vals):
        """
        Asegura que, si no se pasa explícitamente user_id,
        se utilice siempre el usuario actual como autor de la nota.
        """
        vals.setdefault('user_id', self.env.user.id)
        return super().create(vals)
