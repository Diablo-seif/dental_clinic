from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError

class Patient(models.Model):
    _name = 'patient.patient'
    _description = 'patient.patient'
    _rec_name = "name"
    _inherit=['mail.thread','mail.activity.mixin']

    name = fields.Char(string=_("Name"), required=True, tracking=True)
    phone = fields.Char(string=_("Number"),tracking=True,)
    age = fields.Integer(string=_("Age"), compute="_compute_age", store=True, readonly=True ,  tracking=True)
    date_birth = fields.Date(string=_('Birth Date'), tracking=True)
    job_id = fields.Many2one(comodel_name="job.job", string=_("Job"), required=False, tracking=True)
    medical_history_ids = fields.Many2many("medical.history", "patient_medical_rel", "patient_id", "medical_history_id", string=_("Medical History"), tracking=True)
    general_diagnosis_id = fields.Many2one(comodel_name="general.diagnosis",string=_("General Diagnosis"),  tracking=True)
    teeth_ids = fields.One2many(comodel_name="teeth.teeth", inverse_name="patient_id", string=_("Teeth"), required=False,  tracking=True)
    booking_line_ids = fields.One2many(comodel_name="booking.line", inverse_name="patients_id", string=_("Booking"),  tracking=True)
    difference = fields.Float(compute='_compute_difference', store=True, tracking=True)
    treatment_prescription_ids = fields.One2many(comodel_name="treatment.prescription", inverse_name="patient_id", string=_("Treatment Prescription"), required=False, )
    blood_type = fields.Selection(string="Blood type", selection=[ ('a+', 'A+') , ('ab+', 'AB+'),('a-', 'A-') , ('ab-', 'AB-'),('b+', 'B+') ,   ('o+', 'O+'),('b-', 'B-') ,   ('o-', 'O-'),   ]   )

    state = fields.Selection(string=_("State"), selection=[('examination', _('Examination')),('follow_up', _('Follow-up')),('done', _('Done'))], required=False, default='examination', tracking=True)
    user_id = fields.Many2one('res.users', string="System User", readonly=True)

    @api.depends('booking_line_ids.difference')
    def _compute_difference(self):
        for rec in self:
            rec.difference = sum(rec.booking_line_ids.mapped('difference'))

    def change_state (self) :
        if  not self.state :
                        self.state = "examination"
        elif self.state == "examination":
                        self.state = "follow_up"
        elif self.state == "follow_up":
                        self.state = "done"

    def back_state (self) :
        if self.state == "follow_up":
                            self.state = "examination"
        elif self.state == "done":
                        self.state = "follow_up"



    @api.depends('date_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_birth:
                rec.age = (date.today() - rec.date_birth).days // 365
            else:
                rec.age = 0

    @api.constrains ('date_birth')
    def _check_date_birth(self):
        for rec in self :
            if rec.date_birth and rec.date_birth > date.today():
                raise ValidationError(_("⚠️ Birth date must be in the past."))

