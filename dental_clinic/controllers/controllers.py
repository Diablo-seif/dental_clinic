# -*- coding: utf-8 -*-
# from odoo import http


# class DentalClinic(http.Controller):
#     @http.route('/dental_clinic/dental_clinic', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dental_clinic/dental_clinic/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dental_clinic.listing', {
#             'root': '/dental_clinic/dental_clinic',
#             'objects': http.request.env['dental_clinic.dental_clinic'].search([]),
#         })

#     @http.route('/dental_clinic/dental_clinic/objects/<model("dental_clinic.dental_clinic"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dental_clinic.object', {
#             'object': obj
#         })

