from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'  # Extiende el modelo de productos estándar de Odoo

    # --- Campos nuevos --- #

    is_service = fields.Boolean(
        string='Es Servicio',
        default=False,
        help='Marcar este producto como un servicio'
    )
    # Con este booleano señalas si el producto es un servicio (en vez de un artículo físico).

    image_1920 = fields.Image(
        string="Imagen de Producto",
        max_width=1920,
        max_height=1920,
        help="Imagen principal del producto"
    )
    # Imagen de alta resolución (hasta 1920×1920px) para mostrar el producto.

    image_1024 = fields.Image(
        string="Imagen Mediana",
        related="image_1920",
        max_width=1024,
        max_height=1024,
        help="Versión mediana de la imagen"
    )
    image_256 = fields.Image(
        string="Imagen Pequeña",
        related="image_1920",
        max_width=256,
        max_height=256,
        help="Versión pequeña de la imagen"
    )
    image_128 = fields.Image(
        string="Icono",
        related="image_1920",
        max_width=128,
        max_height=128,
        help="Icono del producto"
    )
    # Creamos varias versiones redimensionadas automáticamente
    # para optimizar la carga en diferentes puntos de la interfaz.

    ticket_count = fields.Integer(
        string='Número Tickets Asociados',
        compute='_compute_ticket_count',
        help='Cantidad de tickets de incidencia que usan este producto'
    )
    # Un campo calculado que muestra cuántos tickets están vinculados a este producto.

    ticket_ids = fields.Many2many(
        'ticket.incidencia',           # Modelo destino
        'ticket_product_rel',          # Tabla intermedia
        'template_id',                 # Columna que apunta al producto
        'ticket_id',                   # Columna que apunta al ticket
        string='Tickets de Incidencia relacionados',
        readonly=True
    )
    # Relación M2M para navegar directamente desde el producto
    # hasta los tickets que lo incluyen.

    # --- Lógica de negocio --- #

    @api.depends('ticket_ids')
    def _compute_ticket_count(self):
        """
        Calcula el número de tickets asociados a cada plantilla de producto.
        Agrupa por product_id usando read_group para eficiencia.
        """
        # Leemos en bloque el conteo de incidencias por producto
        tickets = self.env['ticket.incidencia'].read_group(
            [('product_ids', 'in', self.ids)],
            ['product_ids'],
            ['product_ids']
        )
        # Construimos un mapa {producto_id: cantidad}
        count_map = {}
        for grp in tickets:
            for prod_id in grp['product_ids']:
                count_map[prod_id] = grp['__count']
        # Asignamos el conteo a cada registro
        for tmpl in self:
            tmpl.ticket_count = count_map.get(tmpl.id, 0)

    def action_view_tickets(self):
        """
        Abre la vista de lista de tickets filtrada por este producto.
        Utiliza la acción definida en el módulo de soporte.
        """
        self.ensure_one()  # Solo funciona con un único producto seleccionado
        action = self.env.ref('soporte_gestion.action_ticket_incidencia').read()[0]
        action.update({
            'domain': [('product_ids', 'in', [self.id])],
            'context': {'default_product_ids': [(4, self.id)]},
        })
        return action
