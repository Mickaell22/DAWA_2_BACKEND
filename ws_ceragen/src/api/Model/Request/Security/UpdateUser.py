from marshmallow import Schema, fields

class UpdateUserSchema(Schema):
    id_user = fields.Integer(required=True)
    person_ci = fields.String(required=False)
    person_mail = fields.String(required=False) 
    person_password = fields.String(required=False)
    rol_id = fields.Integer(required=False)
    person_id = fields.Integer(required=False)