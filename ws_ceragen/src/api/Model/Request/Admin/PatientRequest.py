from marshmallow import Schema, fields

class PatientInsertRequest(Schema):
    pat_person_id = fields.Int(required=True)
    pat_client_id = fields.Int(required=True)
    pat_code = fields.String(required=False)
    pat_medical_conditions = fields.String(required=False)
    pat_allergies = fields.String(required=False)
    pat_blood_type = fields.String(required=False)
    pat_emergency_contact_name = fields.String(required=False)
    pat_emergency_contact_phone = fields.String(required=False)
    pat_state = fields.Boolean(required=True)
    user_created = fields.String(required=True)

class PatientUpdateRequest(Schema):
    pat_id = fields.Int(required=True)
    pat_person_id = fields.Int(required=True)
    pat_client_id = fields.Int(required=True)
    pat_code = fields.String(required=False)
    pat_medical_conditions = fields.String(required=False)
    pat_allergies = fields.String(required=False)
    pat_blood_type = fields.String(required=False)
    pat_emergency_contact_name = fields.String(required=False)
    pat_emergency_contact_phone = fields.String(required=False)
    pat_state = fields.Boolean(required=True)
    user_modified = fields.String(required=True)