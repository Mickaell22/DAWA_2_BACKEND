from marshmallow import Schema, fields

class InvoiceDetailInsertRequest(Schema):
    ind_invoice_id = fields.Int(required=False, allow_none=True)
    ind_product_id = fields.Int(required=True)
    ind_quantity = fields.Int(required=True)
    ind_unit_price = fields.Decimal(required=True)
    ind_total = fields.Decimal(required=True)
    user_process = fields.String(required=True)

class InvoiceDetailUpdateRequest(Schema):
    ind_id = fields.Int(required=True)
    ind_invoice_id = fields.Int(required=True)
    ind_product_id = fields.Int(required=True)
    ind_quantity = fields.Int(required=True)
    ind_unit_price = fields.Decimal(required=True)
    ind_total = fields.Decimal(required=True)
    user_process = fields.String(required=True)
