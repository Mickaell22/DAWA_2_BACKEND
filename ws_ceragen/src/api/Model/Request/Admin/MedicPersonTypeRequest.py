from marshmallow import Schema, fields

class MedicPersonTypeInsertRequest(Schema):
    mpt_name = fields.String(required=True)
    mpt_description = fields.String(required=True)
    user_process = fields.String(required=True)

class MedicPersonTypeUpdateRequest(Schema):
    mpt_id = fields.Int(required=True)
    mpt_name = fields.String(required=True)
    mpt_description = fields.String(required=True)
    user_process = fields.String(required=True)
