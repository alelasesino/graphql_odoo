# -*- coding: utf-8 -*-
# from odoo import http


# class GraphqlOdoo(http.Controller):
#     @http.route('/graphql_odoo/graphql_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/graphql_odoo/graphql_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('graphql_odoo.listing', {
#             'root': '/graphql_odoo/graphql_odoo',
#             'objects': http.request.env['graphql_odoo.graphql_odoo'].search([]),
#         })

#     @http.route('/graphql_odoo/graphql_odoo/objects/<model("graphql_odoo.graphql_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('graphql_odoo.object', {
#             'object': obj
#         })
