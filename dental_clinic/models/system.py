from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class GeneralDiagnosis (models.Model):
    _name = 'general.diagnosis'
    _description = 'general.diagnosis'
    name = fields.Char(string=_("Name"), required=False, )
    patient_ids= fields.One2many(comodel_name="patient.patient", inverse_name="general_diagnosis_id", string=_("General Diagnosis"), required=False, )

class MedicalHistory (models.Model):
    _name = 'medical.history'
    _description = 'medical.history'
    name = fields.Char(string=_("Name"), required=False, )
    patient_ids = fields.Many2many("patient.patient", "patient_medical_rel", "medical_history_id", "patient_id", string=_("Patients"),)

class Job (models.Model):
    _name = 'job.job'
    _description = 'job.job'
    name = fields.Char(string=_("Name"), required=False, )
    patient_ids = fields.One2many(comodel_name="patient.patient", inverse_name="job_id", string=_("Patient"), required=False, )

class CostExamination(models.Model):
    _name = 'cost.examination'
    _description = 'cost.examination'
    _rec_name = "cost_of_examination"

    cost_of_examination = fields.Float(string=_("Cost Of Examination"),  required=False)

class DentalTeeth(models.Model):
    _name = 'teeth.teeth'
    _description = 'teeth.teeth'

    teeth_code = fields.Many2one('tooth.tooth', string=_("Tooth Code"),)
    teeth_title = fields.Char(string=_("Tooth Name"), related="teeth_code.title", readonly=True)
    des = fields.Text(string=_("Problem"),)
    patient_id = fields.Many2one('patient.patient', string=_("Patient"),)

    @api.constrains ('teeth_code')
    def _check_name(self):
        for rec in self :
            if rec.teeth_code.name > 32 :
                raise ValidationError(_("⚠️ Teeth Code should be positive number and smaller than 33."))
            elif rec.teeth_code.name < 1:
                raise ValidationError(_("⚠️ Teeth Code should be positive number and smaller than 33."))

class DentalTooth(models.Model):
    _name = 'tooth.tooth'
    _description = 'tooth.tooth'
    _rec_name = "name"
    name = fields.Integer(string=_("Tooth Code"), required=True)
    title = fields.Char(string=_("Tooth Title"), required=True, default=_("Unknown"))

    @api.constrains ('name')
    def _check_name(self):
        for rec in self :
            if  rec.name > 32:
                raise ValidationError(_("⚠️ Tooth Code should be positive number and smaller than 33."))
            elif  rec.name < 1:
                raise ValidationError(_("⚠️ Tooth Code should be positive number and smaller than 33."))


class Doctor(models.Model):
    _name = 'doctor.doctor'
    _description = 'doctor.doctor'
    _rec_name = "name"
    name = fields.Char(string=_("Name"), required=True)

