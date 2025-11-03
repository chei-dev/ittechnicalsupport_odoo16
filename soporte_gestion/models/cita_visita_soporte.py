from odoo import models, fields, api, _
from odoo.exceptions import UserError

class CitaVisitaSoporte(models.Model):
    _name = 'cita.visita.soporte'
    _description = 'Cita de Visita de Soporte'
    # Habilitamos hilos de conversación y tareas del buzón de entrada
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Relacionamos la cita con una incidencia (ticket de soporte)
    incidencia_id = fields.Many2one(
        'ticket.incidencia',
        string='Incidencia',
        required=True,          # Obligatorio
        ondelete='cascade',     # Si borras la incidencia, borra la cita
        tracking=True           # Seguimiento en chatter
    )
    # Asignamos un técnico responsable de la visita
    technician_id = fields.Many2one(
        'res.users',
        string='Técnico',
        required=True,
        tracking=True
    )
    # Fecha y hora de la cita
    date = fields.Datetime(
        string='Fecha y Hora',
        required=True,
        default=fields.Datetime.now,  # Por defecto, ahora
        tracking=True
    )
    # Estados por los que pasa la cita
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('scheduled', 'Programada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada'),
    ],
        string='Estado',
        default='draft',
        tracking=True
    )
    # Detalle libre de la visita
    description = fields.Text(string='Descripción')
    # Enlace al evento de calendario creado
    event_id = fields.Many2one(
        'calendar.event',
        string='Evento Calendario',
        readonly=True,
        copy=False
    )

    def action_schedule(self):
        """Programa la cita y crea o actualiza el evento de calendario."""
        for rec in self:
            # Solo citas en borrador
            if rec.state != 'draft':
                continue

            # Validamos que la incidencia tenga cliente asignado
            if not rec.incidencia_id.partner_id:
                raise UserError(_("La incidencia debe tener un cliente asignado."))

            # No permitimos fechas pasadas
            if rec.date < fields.Datetime.now():
                raise UserError(_("La fecha de la cita no puede ser en el pasado."))

            # Preparamos los valores para el evento
            event_vals = {
                'name': _('Visita Soporte: %s') % rec.incidencia_id.name,
                'start': rec.date,
                'stop': rec.date,  # Para duración, ajustar stop > start
                'user_id': rec.technician_id.id,
                'partner_ids': [(4, rec.incidencia_id.partner_id.id)],
                'description': rec.description,
            }

            if rec.event_id:
                # Si ya existe evento, solo lo actualizamos si algo cambió
                has_changes = any(
                    event_vals[k] != getattr(rec.event_id, k)
                    for k in event_vals
                )
                if has_changes:
                    rec.event_id.write(event_vals)
            else:
                # Creamos un nuevo evento y lo vinculamos
                event = self.env['calendar.event'].create(event_vals)
                rec.event_id = event.id

            # Marcamos como programada
            rec.state = 'scheduled'

    def action_done(self):
        """Marcar la cita como realizada."""
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        """Cancelar cita y eliminar evento asociado."""
        for rec in self:
            # Si hay evento en calendario, lo borramos
            if rec.event_id:
                rec.event_id.unlink()
                rec.event_id = False
            rec.state = 'cancelled'

    @api.model
    def create(self, vals):
        # Llamada al método original: aquí podrías agregar notificaciones automáticas
        rec = super().create(vals)
        return rec
