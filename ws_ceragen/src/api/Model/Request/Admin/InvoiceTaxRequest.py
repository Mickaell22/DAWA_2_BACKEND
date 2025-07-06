from marshmallow import Schema, fields

class InvoiceTaxInsertRequest(Schema):
    int_invoice_id = fields.Int(required=False, allow_none=True)
    int_tax_id = fields.Int(required=True)
    int_tax_amount = fields.Decimal(required=True)
    user_process = fields.String(required=True)

class InvoiceTaxUpdateRequest(Schema):
    int_id = fields.Int(required=True)
    int_invoice_id = fields.Int(required=True)
    int_tax_id = fields.Int(required=True)
    int_tax_amount = fields.Decimal(required=True)
    user_process = fields.String(required=True)