# models/account_move.py

from odoo import models, fields

class AccountMove(models.Model):
    # Indicamos que extendemos (heredamos) la funcionalidad del modelo 'account.move'
    _inherit = 'account.move'

    # Añadimos un nuevo campo para vincular el asiento contable con un ticket de soporte
    ticket_id = fields.Many2one(
        comodel_name='ticket.incidencia',       # Modelo al que apunta: nuestro ticket de incidencia
        string='Ticket de Incidencia',          # Etiqueta legible en la interfaz
        help='Ticket de soporte asociado a este asiento contable'  
        # Texto de ayuda que explica qué representa este campo
    )
