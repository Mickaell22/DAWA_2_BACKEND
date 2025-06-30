from marshmallow import Schema, fields

class AllergyCatalogInsertRequest(Schema):
    alc_name = fields.String(required=True)
    alc_description = fields.String(required=True)
    alc_type_id = fields.Int(required=True)
    user_process = fields.String(required=True)

class AllergyCatalogUpdateRequest(Schema):
    alc_id = fields.Int(required=True)
    alc_name = fields.String(required=True)
    alc_description = fields.String(required=True)
    alc_type_id = fields.Int(required=True)
    user_process = fields.String(required=True)
