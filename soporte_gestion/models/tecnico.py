# models/tecnico.py

from odoo import models, fields

class Tecnico(models.Model):
    _name = 'soporte.tecnico'
    _description = 'Técnico'

    # Nombre descriptivo del técnico (puede ser alias, nombre completo, etc.)
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre visible del técnico en la interfaz'
    )

    # Enlaza este registro con un empleado de Recursos Humanos
    employee_id = fields.Many2one(
        'hr.employee',
        string='Empleado',
        required=True,
        help='Empleado asociado al técnico para datos de nómina y permisos'
    )

    # Relaciona el técnico con un usuario de Odoo (login, permisos de acceso)
    user_id = fields.Many2one(
        'res.users',
        string='Usuario Odoo',
        required=True,
        help='Cuenta de usuario que usará el técnico en Odoo'
    )

    # Lista todos los tickets de incidencia donde este técnico está asignado
    ticket_ids = fields.One2many(
        'ticket.incidencia',   # Modelo destino: incidencias de soporte
        'technician_id',       # Campo Many2one en ticket.incidencia
        string='Tickets de Incidencia',
        help='Tickets que tiene asignados este técnico'
    )


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # Añadimos al empleado la misma relación de tickets que al técnico,
    # para ver en la ficha de empleado los tickets asignados
    ticket_ids = fields.One2many(
        'ticket.incidencia',   # Modelo de incidencias
        'technician_id',       # Mismo campo Many2one que usa Tecnico
        string='Tickets asignados',
        readonly=True,
        help='Incidencias de soporte donde este empleado actúa como técnico'
    )
