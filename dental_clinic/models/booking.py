from odoo import models, fields, api, _
from datetime import date, timedelta
import babel.dates
from odoo.exceptions import ValidationError

class BookingLine(models.Model):
    _name = 'booking.line'
    _description = 'booking.line'
    _inherit=['mail.thread','mail.activity.mixin']

    num = fields.Integer(string=_("N"), readonly=True)
    des = fields.Text(string=_("description"), required=False, )
    state = fields.Selection(string=_("State"), selection=[('waiting',  _('Waiting')), ('consultation',  _('Consultation')), ('done',  _('Done')), ], required=False,default="waiting" )
    cost = fields.Float(string=_("Cost"), required=False, )
    total_cost = fields.Float(string=_("Total Cost"), required=False, compute="_compute_total_cost",)
    pay = fields.Float(string=_("Pay"), required=False, )
    difference = fields.Float(string=_("Difference"), required=False, readonly=True, store=True,compute="_compute_difference",)
    patients_id = fields.Many2one(comodel_name="patient.patient", string=_("Name"), required=False, )
    person = fields.Char(string=_("Person"), store=True,related="patients_id.name",)
    booking_id = fields.Many2one(comodel_name="booking.booking", string=_("Booking"),)
    check_examination = fields.Boolean(string=_("Examination"), default=False)
    check_amount = fields.Float(string=_("Examination Cost"), compute="_compute_check_amount", store=True)
    doctor_id = fields.Many2one(comodel_name="doctor.doctor", string="Doctor", required=False, )
    @api.depends("check_examination")
    def _compute_check_amount(self):
        for rec in self:
            if rec.check_examination:
                exam = self.env['cost.examination'].search([], limit=1)
                rec.check_amount = exam.cost_of_examination if exam else 0.0
            else:
                rec.check_amount = 0.0

    @api.constrains('cost', 'pay')
    def _check_values(self):
        for rec in self:
            if rec.cost < 0:
                raise ValidationError(_("⚠️ Cost can only be a positive number."))
            if rec.pay < 0:
                raise ValidationError(_("⚠️ Pay can only be a positive number."))

    @api.model
    def create(self, vals):
        booking_date = False
        if 'booking_id' in vals:
            booking = self.env['booking.booking'].browse(vals['booking_id'])
            booking_date = booking.date
        else:
            booking_date = fields.Date.context_today(self)

        last_num = self.search([('booking_id.date', '=', booking_date)], order='num desc', limit=1).mapped('num')
        new_num = 1
        if last_num:
            new_num = last_num[0] + 1

        vals['num'] = new_num
        return super(BookingLine, self).create(vals)
    @api.depends("cost","check_amount")
    def _compute_total_cost(self):
        for rec in self:
            rec.total_cost = (rec.cost or 0.0) + (rec.check_amount or 0.0)
    @api.depends("pay", "total_cost")
    def _compute_difference(self):
        for rec in self:
            rec.difference = (rec.pay or 0.0) - (rec.total_cost or 0.0)

class Booking(models.Model):
    _name = 'booking.booking'
    _description = 'booking.booking'
    _rec_name = "name"
    _inherit=['mail.thread','mail.activity.mixin']

    name = fields.Char(string=_("Day"),     compute="_compute_name", store=True,tracking=True , )
    day  = fields.Char(string=_("Booking Day"), tracking=True ,)
    date = fields.Date(string=_("Date"), default=fields.Date.context_today,tracking=True ,)
    pay = fields.Float(string=_("Financial budget"), compute="_compute_line_totals", store=True ,tracking=True)
    booking_line_ids = fields.One2many(comodel_name="booking.line", inverse_name="booking_id", string=_("Patients"),)
    month = fields.Char(string=_("Month"), compute="_compute_month", store=True, index=True)
    difference_total = fields.Float(string="Total Difference", compute="_compute_line_totals", store=True)
    cost_total = fields.Float(string="Total Cost", compute="_compute_line_totals", store=True)
    patients_total = fields.Integer(string="Total Disclosures", compute="_compute_line_totals", store=True)

    @api.depends("booking_line_ids.cost" ,"booking_line_ids.difference" ,"booking_line_ids.pay" , "booking_line_ids.patients_id")
    def _compute_line_totals(self):
        for rec in self:
            rec.difference_total = sum(rec.booking_line_ids.mapped("difference"))
            rec.pay = sum(rec.booking_line_ids.mapped("pay"))
            rec.cost_total = sum(rec.booking_line_ids.mapped("cost"))
            rec.patients_total = len(rec.booking_line_ids)


    @api.depends("date")
    def _compute_name(self):
        for rec in self:
            if rec.date:
                dt = fields.Date.from_string(rec.date) if isinstance(rec.date, str) else rec.date
                # لغة المستخدم أو عربي
                lang = rec.env.user.lang or 'en_US'
                try:
                    day_name = babel.dates.format_date(dt, format='EEEE', locale=lang)
                except Exception:
                    day_name = dt.strftime('%A')
                # هنا بقى الـ name = "اسم اليوم - التاريخ"
                rec.name = _("%s - %s") % (day_name, rec.date)
            else:
                rec.name = ""

    @api.depends("date")
    def _compute_month(self):
        for rec in self:
            if rec.date:
                lang = rec.env.user.lang or 'en_US'
                try:
                    rec.month = babel.dates.format_date(rec.date, "MMMM yyyy", locale=lang)
                except Exception:
                    rec.month = rec.date.strftime("%B %Y")
            else:
                rec.month = ""


    @api.constrains('date')
    def _check_unique_date(self):
        for rec in self:
            if rec.date and self.search_count([('date', '=', rec.date), ('id', '!=', rec.id)]) > 0:
                raise ValidationError(_("⚠️ The date has already been registered. \n You cannot register again."))
