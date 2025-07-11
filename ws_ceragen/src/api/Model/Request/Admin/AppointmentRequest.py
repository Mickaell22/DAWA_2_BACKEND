from marshmallow import Schema, fields, validate

class AppointmentScheduleRequest(Schema):
    """Schema para agendar nueva cita"""
    sec_inv_id = fields.Int(required=True, validate=validate.Range(min=1))
    sec_pro_id = fields.Int(required=True, validate=validate.Range(min=1))
    sec_ses_number = fields.Int(required=True, validate=validate.Range(min=1))
    sec_ses_agend_date = fields.Str(required=True)  # ISO format datetime string
    sec_typ_id = fields.Int(required=True, validate=validate.Range(min=1))
    sec_med_staff_id = fields.Int(required=True, validate=validate.Range(min=1))
    user_process = fields.Str(required=True, validate=validate.Length(min=1, max=100))

class AppointmentRescheduleRequest(Schema):
    """Schema para reagendar cita existente"""
    sec_id = fields.Int(required=True, validate=validate.Range(min=1))
    new_agend_date = fields.Str(required=True)  # ISO format datetime string

class AppointmentAvailabilityRequest(Schema):
    """Schema para verificar disponibilidad"""
    date_time = fields.Str(required=True)  # ISO format datetime string
    therapy_type_id = fields.Int(required=True, validate=validate.Range(min=1))
    staff_id = fields.Int(required=False, validate=validate.Range(min=1))

class AppointmentUpdateRequest(Schema):
    """Schema para actualizar cita"""
    sec_id = fields.Int(required=True, validate=validate.Range(min=1))
    sec_inv_id = fields.Int(required=False, validate=validate.Range(min=1))
    sec_pro_id = fields.Int(required=False, validate=validate.Range(min=1))
    sec_ses_number = fields.Int(required=False, validate=validate.Range(min=1))
    sec_ses_agend_date = fields.Str(required=False)  # ISO format datetime string
    sec_typ_id = fields.Int(required=False, validate=validate.Range(min=1))
    sec_med_staff_id = fields.Int(required=False, validate=validate.Range(min=1))
    user_process = fields.Str(required=True, validate=validate.Length(min=1, max=100))

