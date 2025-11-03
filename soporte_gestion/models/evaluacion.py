# models/evaluacion_satisfaccion.py

from odoo import models, fields

class Evaluacion(models.Model):
    _name = 'evaluacion'
    _description = 'Evaluación de Satisfacción'

    # Enlaza esta evaluación con el ticket de incidencia al que responde
    incidencia_id = fields.Many2one(
        'ticket.incidencia',
        string='Incidencia',
        help='Ticket de soporte al que corresponde esta evaluación'
    )

    # Permite al usuario elegir una nota del 1 al 5, con etiquetas claras
    rating = fields.Selection([
        ('1', 'Muy mala'),
        ('2', 'Mala'),
        ('3', 'Regular'),
        ('4', 'Buena'),
        ('5', 'Muy buena'),
    ],
        string='Calificación',
        help='Puntuación de la satisfacción del cliente'
    )

    # Campo libre para que el cliente deje comentarios adicionales
    comments = fields.Text(
        string='Comentarios',
        help='Observaciones o sugerencias del cliente sobre el servicio'
    )
