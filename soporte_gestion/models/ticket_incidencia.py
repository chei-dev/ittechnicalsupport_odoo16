from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import datetime

class TicketIncidencia(models.Model):
    _name = 'ticket.incidencia'
    _description = 'Ticket de Incidencia'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Habilita chatter y actividades
    _order = 'name desc'  # Ordena los tickets por referencia, de mayor a menor

    # Referencia única autogenerada (secuencia)
    name = fields.Char(
        'Referencia',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: self.env['ir.sequence']
                                 .next_by_code('ticket.incidencia'),
    )
    # Cliente que reporta el ticket
    partner_id = fields.Many2one(
        'res.partner', 'Cliente',
        required=True,
        tracking=True,
        ondelete='cascade'
    )
    # Usuario que creó el ticket
    user_id = fields.Many2one(
        'res.users', 'Creador',
        default=lambda self: self.env.user,
        tracking=True
    )
    # Técnico (empleado) asignado al ticket
    technician_id = fields.Many2one(
        'hr.employee', 'Técnico asignado',
        required=True,
        tracking=True
    )
    # Eventos de calendario asociados (se sincronizan con cambios de estado)
    event_id = fields.Many2one(
        'calendar.event', 'Evento asociado',
        readonly=True
    )

    # Flujo de estados del ticket
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('assigned', 'Asignado'),
        ('in_progress', 'En Progreso'),
        ('done', 'Completado'),
        ('cancelled', 'Cancelado'),
    ],
        default='draft',
        tracking=True
    )

    # Descripción y equipo afectado
    descripcion = fields.Text('Descripción', help='Detalles del problema')
    equipo_afectado = fields.Char('Equipo Afectado', help='Dispositivo o sistema')

    # Foto y sus versiones redimensionadas
    image = fields.Image("Foto de Incidencia", max_width=1024, max_height=1024)
    image_medium = fields.Image("Imagen mediana", related="image", store=True, readonly=True)
    image_small = fields.Image("Imagen", related="image", store=True, readonly=True)

    # Fechas de inicio y finalización del trabajo, calculadas al cambiar estado
    event_start = fields.Datetime('Fecha de Inicio', readonly=True)
    event_stop = fields.Datetime('Fecha de Finalización', readonly=True)

    # Historial de acciones y notas (modelo separado)
    historial_ids = fields.One2many(
        'ticket.historial', 'incidencia_id',
        'Historial', readonly=True
    )
    # Productos o servicios vinculados al ticket
    product_ids = fields.Many2many(
        'product.product',
        'ticket_producto_rel',
        'ticket_id', 'product_id',
        'Productos/Servicios',
        tracking=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        """
        Al crear uno o varios tickets:
        - Si el estado es 'assigned', fija event_start ahora.
        - Sincroniza/crea el evento de calendario.
        - Añade una entrada inicial en el historial.
        """
        records = super().create(vals_list)
        for rec in records:
            if rec.state == 'assigned':
                rec.event_start = fields.Datetime.now()
            rec._sync_event()
            rec.create_historial_entry("Incidencia creada")
        return records

    def write(self, vals):
        """
        Al modificar campos:
        - Si cambia 'state', actualiza event_start/event_stop según corresponda.
        - Registra cada cambio de estado en el historial.
        - Sincroniza el evento de calendario tras los cambios.
        """
        res = super().write(vals)
        if 'state' in vals:
            for rec in self:
                new_state = vals['state']
                if new_state == 'assigned' and not rec.event_start:
                    rec.event_start = fields.Datetime.now()
                if new_state in ('done', 'cancelled') and not rec.event_stop:
                    rec.event_stop = fields.Datetime.now()
                rec.create_historial_entry(
                    f"Estado cambiado a {dict(self._fields['state'].selection)[new_state]}"
                )
        for rec in self:
            rec._sync_event()
        return res

    def _sync_event(self):
        """
        Crea o actualiza un evento de calendario para este ticket:
        - Si el ticket se cancela, borra el evento.
        - En otros casos, valida que el técnico tenga usuario y ajusta fecha/hora.
        """
        for rec in self:
            if rec.state == 'cancelled':
                if rec.event_id:
                    rec.event_id.unlink()
                    rec.event_id = False
                continue

            if not rec.technician_id.user_id:
                raise ValidationError("El técnico debe tener un usuario válido asignado.")

            # Determina las fechas de inicio/parada del evento
            start = rec.event_start or fields.Datetime.now()
            stop = rec.event_stop or (start + datetime.timedelta(hours=1))

            event_vals = {
                'name':        f"Visita: {rec.name}",
                'start':       start,
                'stop':        stop,
                'allday':      False,
                'user_id':     rec.technician_id.user_id.id,
                'description': (
                    f"Ticket #{rec.name} para {rec.partner_id.name}\n"
                    f"Estado: {rec.state}\n\n"
                    f"{rec.descripcion or ''}\n"
                    f"Equipo Afectado: {rec.equipo_afectado or 'No especificado'}"
                ),
            }

            if rec.event_id:
                rec.event_id.write(event_vals)
            else:
                rec.event_id = self.env['calendar.event'].create(event_vals)

    def action_start(self):
        """
        Pasa los tickets 'assigned' a 'in_progress', publica mensaje y historial.
        """
        for rec in self.filtered(lambda r: r.state == 'assigned'):
            rec.state = 'in_progress'
            rec.message_post(body="Trabajo en progreso iniciado.")
            rec.create_historial_entry("Trabajo en progreso iniciado")
        return True

    def action_done(self):
        """
        Marca tickets como 'done' si estaban en 'assigned' o 'in_progress'.
        Agrega mensaje en chatter e historial.
        """
        for rec in self.filtered(lambda r: r.state in ('assigned', 'in_progress')):
            rec.state = 'done'
            rec.message_post(body="Trabajo completado.")
            rec.create_historial_entry("Trabajo completado")
        return True

    def action_cancel(self):
        """
        Cancela el ticket, publica mensaje e historial,
        y a su vez el método de write borrará el evento.
        """
        for rec in self:
            rec.state = 'cancelled'
            rec.message_post(body="Ticket cancelado.")
            rec.create_historial_entry("Ticket cancelado")
        return True

    def action_generate_invoice(self):
        """
        Genera una factura con los productos/servicios del ticket.
        Si hay descripción, la añade como línea sin precio unitario.
        Abre el formulario de la factura creada.
        """
        self.ensure_one()
        if not self.product_ids:
            raise ValidationError("No hay productos o servicios seleccionados.")
        lines = [
            (0, 0, {
                'product_id': p.id,
                'name':       p.display_name,
                'quantity':   1,
                'price_unit': p.lst_price
            })
            for p in self.product_ids
        ]
        if self.descripcion:
            lines.append((0, 0, {
                'name': self.descripcion,
                'quantity': 1,
                'price_unit': 0.0,
                'product_id': False,
            }))
        inv = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': lines,
        })
        return {
            'name': 'Factura',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': inv.id,
            'type': 'ir.actions.act_window',
        }

    def action_set_assigned(self):
        """
        Cambia manualmente de 'draft' a 'assigned',
        publica mensaje e historial.
        """
        for rec in self.filtered(lambda r: r.state == 'draft'):
            rec.state = 'assigned'
            rec.message_post(body="Estado cambiado manualmente a 'Asignado'.")
            rec.create_historial_entry("Estado cambiado manualmente a 'Asignado'")
        return True

    @api.constrains('technician_id', 'partner_id')
    def _check_technician_not_client(self):
        """
        Impide que el técnico asignado sea el mismo usuario que el cliente.
        """
        for rec in self:
            if (
                rec.partner_id.user_id and
                rec.technician_id.user_id and
                rec.partner_id.user_id == rec.technician_id.user_id
            ):
                raise ValidationError("El técnico no puede ser el mismo que el cliente.")

    def create_historial_entry(self, notes):
        """
        Auxiliar para añadir una nota al historial del ticket.
        """
        self.env['ticket.historial'].create({
            'incidencia_id': self.id,
            'notes': notes,
        })
