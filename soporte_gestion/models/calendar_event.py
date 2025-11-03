
from odoo import models, fields

class CalendarEvent(models.Model):
    # Extendemos el modelo de eventos de calendario de Odoo
    _inherit = 'calendar.event'

    # Añadimos un campo Many2one para vincular cada evento con una cita o visita de soporte
    cita_visita_id = fields.Many2one(
        comodel_name='cita.visita',       # Modelo al que enlaza: nuestras citas/visitas de soporte
        string='Cita / Visita',           # Etiqueta que verá el usuario en la interfaz
        help='Enlace a la cita o visita de soporte relacionada'  
        # Texto de ayuda que aclara la función del campo
    )
