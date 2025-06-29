from marshmallow import Schema, fields

class DiseaseTypeInsertRequest(Schema):
    dst_name = fields.String(required=True)
    dst_description = fields.String(required=True)
    user_process = fields.String(required=True)

class DiseaseTypeUpdateRequest(Schema):
    dst_id = fields.Int(required=True)
    dst_name = fields.String(required=True)
    dst_description = fields.String(required=True)
    user_process = fields.String(required=True)
