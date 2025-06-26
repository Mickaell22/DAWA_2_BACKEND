from marshmallow import Schema, fields

class PersonalStaffInsertRequest(Schema):
    med_person_id = fields.Int(required=True)
    med_type_id = fields.Int(required=True)
    med_registration_number = fields.Int(required=True)
    med_specialty = fields.String(required=True)
    user_process = fields.String(required=True)

class PersonalStaffUpdateRequest(Schema):
    med_id = fields.Int(required=True)
    med_person_id = fields.Int(required=True)
    med_type_id = fields.Int(required=True)
    med_registration_number = fields.Int(required=True)
    med_specialty = fields.String(required=True)
    user_process = fields.String(required=True)
