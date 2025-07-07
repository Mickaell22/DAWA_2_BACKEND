from marshmallow import Schema, fields

class InvoiceInsertRequest(Schema):
    inv_number = fields.String(required=True)
    inv_client_id = fields.Int(required=True)
    inv_patient_id = fields.Int(required=True)
    inv_subtotal = fields.Decimal(required=True)
    inv_discount = fields.Decimal(required=True)
    inv_tax = fields.Decimal(required=True)
    inv_grand_total = fields.Decimal(required=True)
    user_process = fields.String(required=True)


class InvoiceUpdateRequest(Schema):
    inv_id = fields.Int(required=True)
    inv_number = fields.String(required=True)
    inv_client_id = fields.Int(required=True)
    inv_patient_id = fields.Int(required=True)
    inv_subtotal = fields.Decimal(required=True)
    inv_discount = fields.Decimal(required=True)
    inv_tax = fields.Decimal(required=True)
    inv_grand_total = fields.Decimal(required=True)
    user_process = fields.String(required=True)