from marshmallow import Schema, fields

class TherapyInsertRequest(Schema):
    tht_name = fields.String(required=True)
    tht_description = fields.String(required=False)
    user_process = fields.String(required=True)

class TherapyUpdateRequest(Schema):
    tht_id = fields.Int(required=True)
    tht_name = fields.String(required=True)
    tht_description = fields.String(required=False)
    user_process = fields.String(required=True)