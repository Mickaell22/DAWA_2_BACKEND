from marshmallow import Schema, fields

class InvoicePaymentInsertRequest(Schema):
    inp_invoice_id = fields.Int(required=False, allow_none=True)
    inp_payment_method_id = fields.Int(required=True)
    inp_amount = fields.Decimal(required=True)
    inp_reference = fields.String(required=True)
    inp_proof_image_path = fields.String(required=False, allow_none=True)
    user_process = fields.String(required=True)

class InvoicePaymentUpdateRequest(Schema):
    inp_id = fields.Int(required=True)
    inp_invoice_id = fields.Int(required=True)
    inp_payment_method_id = fields.Int(required=True)
    inp_amount = fields.Decimal(required=True)
    inp_reference = fields.String(required=True)
    inp_proof_image_path = fields.String(required=False, allow_none=True)
    user_process = fields.String(required=True)