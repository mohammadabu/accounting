import logging

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

_logger = logging.getLogger(__name__)


class AttendanceWizard(models.TransientModel):
    _name = 'attendance.wizard'
    _description = 'Attendance Wizard'

    @api.model
    def _get_all_device_ids(self):
        all_devices = self.env['attendance.device'].search([('state', '=', 'confirmed')])
        if all_devices:
            return all_devices.ids
        else:
            return []

    device_ids = fields.Many2many('attendance.device', string='Devices', default=_get_all_device_ids, domain=[('state', '=', 'confirmed')])
    fix_attendance_valid_before_synch = fields.Boolean(string='Fix Attendance Valid', help="If checked, Odoo will recompute all attendance data for their valid"
                                                     " before synchronizing with HR Attendance (upon you hit the 'Synchronize Attendance' button)")

    def download_attendance_manually(self):
        # TODO: remove me after 12.0
        self.action_download_attendance()

    def action_download_attendance(self):
        if not self.device_ids:
            raise UserError(_('You must select at least one device to continue!'))
        self.device_ids.action_attendance_download()

    def cron_download_device_attendance(self):
        devices = self.env['attendance.device'].search([('state', '=', 'confirmed')])
        devices.action_attendance_download()

    def cron_sync_attendance(self):
        self.with_context(synch_ignore_constraints=True).sync_attendance()

    def sync_attendance(self):
        """
        This method will synchronize all downloaded attendance data with Odoo attendance data.
        It do not download attendance data from the devices.
        """
        if self.fix_attendance_valid_before_synch:
            self.action_fix_user_attendance_valid()

        synch_ignore_constraints = self.env.context.get('synch_ignore_constraints', False)

        error_msg = {}
        HrAttendance = self.env['hr.attendance'].with_context(synch_ignore_constraints=synch_ignore_constraints)
        
        unsync_data = self.env['user.attendance'].search([
            ('hr_attendance_id', '=', False),
            ('valid', '=', True),
            ('employee_id', '!=', False)], order='timestamp ASC')

        last_employee_attendance = {}
        for attendance_activity in self.env['attendance.activity'].search([]):
            if attendance_activity.id not in last_employee_attendance.keys():
                last_employee_attendance[attendance_activity.id] = {}
            unsync_user_attendances = unsync_data.filtered(lambda uatt: uatt.activity_id == attendance_activity).sorted('timestamp')
            for uatt in unsync_user_attendances:
                employee = uatt.user_id.employee_id
                if employee.id not in last_employee_attendance[attendance_activity.id].keys():
                    last_employee_attendance[attendance_activity.id][employee.id] = False

                if uatt.type == 'checkout':
                    # find last attendance
                    last_employee_attendance[attendance_activity.id][employee.id] = HrAttendance.search(
                        [('employee_id', '=', employee.id),
                         ('activity_id', 'in', (attendance_activity.id, False)),
                         ('check_in', '<=', uatt.timestamp)], limit=1, order='check_in DESC')

                    hr_attendance = last_employee_attendance[attendance_activity.id][employee.id]

                    if hr_attendance:
                        try:
                            hr_attendance.with_context(synch_ignore_constraints=synch_ignore_constraints).write({
                                'check_out': uatt.timestamp,
                                'checkout_device_id': uatt.device_id.id
                                })
                        except ValidationError as e:
                            if uatt.device_id not in error_msg:
                                error_msg[uatt.device_id] = ""

                            msg = ""
                            att_check_time = fields.Datetime.context_timestamp(uatt, uatt.timestamp)
                            msg += str(e) + "<br />"
                            msg += _("'Check Out' time cannot be earlier than 'Check In' time. Debug information:<br />"
                                          "* Employee: <strong>%s</strong><br />"
                                          "* Type: %s<br />"
                                          "* Attendance Check Time: %s<br />") % (employee.name, uatt.type, fields.Datetime.to_string(att_check_time))
                            _logger.error(msg)
                            error_msg[uatt.device_id] += msg
                else:
                    # create hr attendance data
                    vals = {
                        'employee_id': employee.id,
                        'check_in': uatt.timestamp,
                        'checkin_device_id': uatt.device_id.id,
                        'activity_id': attendance_activity.id,
                        }
                    hr_attendance = HrAttendance.search([
                        ('employee_id', '=', employee.id),
                        ('check_in', '=', uatt.timestamp),
                        ('checkin_device_id', '=', uatt.device_id.id),
                        ('activity_id', '=', attendance_activity.id)], limit=1)
                    if not hr_attendance:
                        try:
                            hr_attendance = HrAttendance.create(vals)
                        except Exception as e:
                            _logger.error(e)

                if hr_attendance:
                    uatt.write({
                        'hr_attendance_id': hr_attendance.id
                        })

        if bool(error_msg):
            for device in error_msg.keys():

                if not device.debug_message:
                    continue
                device.message_post(body=error_msg[device])

    def clear_attendance(self):
        if not self.device_ids:
            raise UserError(_('You must select at least one device to continue!'))
        if not self.env.user.has_group('hr_attendance.group_hr_attendance_manager'):
            raise UserError(_('Only HR Attendance Managers can manually clear device attendance data'))

        for device in self.device_ids:
                device.clearAttendance()

    def action_fix_user_attendance_valid(self):
        self.env['user.attendance'].search([])._update_valid()
