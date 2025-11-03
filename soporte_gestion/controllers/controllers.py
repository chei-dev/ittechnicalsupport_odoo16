# -*- coding: utf-8 -*-
# from odoo import http


# class Support(http.Controller):
#     @http.route('/support/support', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/support/support/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('support.listing', {
#             'root': '/support/support',
#             'objects': http.request.env['support.support'].search([]),
#         })

#     @http.route('/support/support/objects/<model("support.support"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('support.object', {
#             'object': obj
#         })
