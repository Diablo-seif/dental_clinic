from odoo import models, fields, api, _

class TreatmentPrescription(models.Model):
    _name = "treatment.prescription"
    _description = "Therapeutic Prescription"
    _inherit=['mail.thread','mail.activity.mixin']

    name = fields.Char(string=_("Medicine Name"))
    alternative = fields.Char(string=_("Alternative Medicine"), )
    des = fields.Char(string=_("Description") , )
    patient_id = fields.Many2one(comodel_name="patient.patient", string="Patient", required=False )
