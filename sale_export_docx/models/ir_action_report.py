# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class IrActionReport(models.Model):
    _inherit = "ir.actions.report"

    report_type = fields.Selection(selection_add=[("docx", "DOCX")])

    @api.model
    def render_docx(self, docids, data):
        report_model_name = "report.%s" % self.report_name
        report_model = self.env.get(report_model_name)
        if report_model is None:
            raise UserError(_("%s model was not found" % report_model_name))
        return report_model.with_context(active_model=self.model).create_docx_report(  # noqa
            docids, data
        )

    @api.model
    def _get_report_from_name(self, report_name):
        res = super(IrActionReport, self)._get_report_from_name(report_name)
        if res:
            return res
        report_obj = self.env["ir.actions.report"]
        qwebtypes = ["docx"]
        conditions = [
            ("report_type", "in", qwebtypes),
            ("report_name", "=", report_name),
        ]
        context = self.env["res.users"].context_get()
        return report_obj.with_context(context).search(conditions, limit=1)
