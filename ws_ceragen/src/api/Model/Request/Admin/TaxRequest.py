from marshmallow import Schema, fields

class AdminTaxInsertRequest(Schema):
    tax_name = fields.String(required=True)
    tax_percentage = fields.Float(required=True)
    tax_description = fields.String(required=True)
    user_process = fields.String(required=True)

class AdminTaxUpdateRequest(Schema):
    tax_id = fields.Int(required=True)
    tax_name = fields.String(required=True)
    tax_percentage = fields.Float(required=True)
    tax_description = fields.String(required=True)
    user_process = fields.String(required=True)
