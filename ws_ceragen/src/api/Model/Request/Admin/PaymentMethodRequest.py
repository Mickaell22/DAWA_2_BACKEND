from marshmallow import Schema, fields

class PaymentMethodInsertRequest(Schema):
    pme_name = fields.String(required=True)
    pme_description = fields.String(required=True)
    pme_require_references = fields.Boolean(required=True)
    pme_require_picture_proff = fields.Boolean(required=True)
    user_process = fields.String(required=True)

class PaymentMethodUpdateRequest(Schema):
    pme_id = fields.Int(required=True)
    pme_name = fields.String(required=True)
    pme_description = fields.String(required=True)
    pme_require_references = fields.Boolean(required=True)
    pme_require_picture_proff = fields.Boolean(required=True)
    user_process = fields.String(required=True)
