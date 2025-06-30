from marshmallow import Schema, fields

class ClinicDiseaseCatalogInsertRequest(Schema):
    dis_name = fields.String(required=True)
    dis_description = fields.String(required=True)
    dis_type_id = fields.Integer(required=True)
    user_process = fields.String(required=True)

class ClinicDiseaseCatalogUpdateRequest(Schema):
    dis_id = fields.Integer(required=True)
    dis_name = fields.String(required=True)
    dis_description = fields.String(required=True)
    dis_type_id = fields.Integer(required=True)
    user_process = fields.String(required=True)
