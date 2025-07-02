from marshmallow import Schema, fields, ValidationError

class PromotionInsertRequest(Schema):
    ppr_product_id = fields.Int(required=True)
    ppr_name = fields.String(required=True)
    ppr_description = fields.String(required=False)
    ppr_discount_percent = fields.Float(required=True)
    ppr_extra_sessions = fields.Int(required=True)
    ppr_start_date = fields.Date(required=True)
    ppr_end_date = fields.Date(required=True)
    user_created = fields.String(required=True)

    def validate(self, data):
        try:
            print("DEBUG - Validando PromotionInsertRequest:", data)
            self.load(data)
            return None
        except ValidationError as err:
            print("DEBUG - Error de validación PromotionInsertRequest:", err.messages)
            return err.messages

class PromotionUpdateRequest(Schema):
    ppr_id = fields.Int(required=True)
    ppr_product_id = fields.Int(required=True)
    ppr_name = fields.String(required=True)
    ppr_description = fields.String(required=False)
    ppr_discount_percent = fields.Float(required=True)
    ppr_extra_sessions = fields.Int(required=True)
    ppr_start_date = fields.Date(required=True)
    ppr_end_date = fields.Date(required=True)
    ppr_state = fields.Boolean(required=True)  # <-- Campo para permitir cambiar el estado
    user_modified = fields.String(required=True)

    def validate(self, data):
        try:
            print("DEBUG - Validando PromotionUpdateRequest:", data)
            self.load(data)
            return None
        except ValidationError as err:
            print("DEBUG - Error de validación PromotionUpdateRequest:", err.messages)
            return err.messages