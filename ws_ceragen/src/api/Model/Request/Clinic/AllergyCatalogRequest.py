from marshmallow import Schema, fields

class AllergyCatalogInsertRequest(Schema):
    al_name = fields.String(required=True)
    al_description = fields.String(required=True)
    user_process = fields.String(required=True)

class AllergyCatalogUpdateRequest(Schema):
    al_id = fields.Int(required=True)
    al_name = fields.String(required=True)
    al_description = fields.String(required=True)
    user_process = fields.String(required=True)
