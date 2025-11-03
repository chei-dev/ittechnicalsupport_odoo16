#© 2025 José Luis Ruiz Verdugo

#Todos los derechos reservados.

#Este módulo de Odoo y todo su contenido (código fuente, vistas, imágenes, documentación, etc.) son propiedad exclusiva del desarrollador.

#Queda estrictamente prohibida cualquier forma de distribución, copia, modificación, sublicencia o uso comercial sin la autorización expresa y por escrito del desarrollador.

#Para consultas o licencias, puedes contactar a (jlruizverdugo@outlook.es)




{
'name': 'Soporte Técnico',
'version': '16.0.1.0.0',
'summary': 'Gestión de tickets de soporte, contratos, servicios y satisfacción',
'category': 'Services/Helpdesk',
'author': 'José Luis Ruiz Verdugo',
'license': 'AGPL-3',
'depends': ['base', 'account','hr', 'calendar', 'product'],
'data': [
'security/ir.model.access.csv',
'views/vistas_ticket_incidencia.xml',
'views/vistas_contrato_soporte.xml',
'views/vistas_producto_servicio.xml',
'views/vistas_evaluacion.xml',
'views/vistas_cita_visita_soporte.xml',
'views/vistas_heredadas.xml',
'views/vistas_tecnico.xml',
'views/acciones.xml',
'views/vistas_menus.xml',
'views/vistas_facturacion.xml',
],
'application': True,
'installable': True,
}