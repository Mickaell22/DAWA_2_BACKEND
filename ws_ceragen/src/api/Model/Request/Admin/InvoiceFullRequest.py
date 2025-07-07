from marshmallow import Schema, fields

class InvoiceDetailSchema(Schema):
    ind_product_id = fields.Int(required=True)
    ind_quantity = fields.Int(required=True)
    ind_unit_price = fields.Decimal(required=True)
    ind_total = fields.Decimal(required=True)

class InvoicePaymentSchema(Schema):
    inp_payment_method_id = fields.Int(required=True)
    inp_amount = fields.Decimal(required=True)
    inp_reference = fields.String(allow_none=True)
    inp_proof_image_path = fields.String(allow_none=True)

class InvoiceTaxSchema(Schema):
    int_tax_id = fields.Int(required=True)
    int_tax_amount = fields.Decimal(required=True)

class InvoiceFullRequest(Schema):
    inv_number = fields.String(required=True)
    inv_client_id = fields.Int(required=True)
    inv_patient_id = fields.Int(required=True)
    inv_subtotal = fields.Decimal(required=True)
    inv_discount = fields.Decimal(required=True)
    inv_tax = fields.Decimal(required=True)
    #inv_grand_total = fields.Decimal(required=True)
    user_process = fields.String(required=True)

    details = fields.List(fields.Nested(InvoiceDetailSchema), required=True)
    payments = fields.List(fields.Nested(InvoicePaymentSchema), required=True)
    taxes = fields.List(fields.Nested(InvoiceTaxSchema), required=True)
