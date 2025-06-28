from marshmallow import Schema, fields

class ProductInsertRequest(Schema):
    pro_code = fields.String(required=True)
    pro_name = fields.String(required=True)
    pro_description = fields.String(required=False)
    pro_price = fields.Float(required=True)
    pro_total_sessions = fields.Int(required=True)
    pro_duration_days = fields.Int(required=True)
    pro_image_url = fields.String(required=False)
    pro_therapy_type_id = fields.Int(required=True)
    user_process = fields.String(required=True)

class ProductUpdateRequest(Schema):
    pro_id = fields.Int(required=True)
    pro_code = fields.String(required=True)
    pro_name = fields.String(required=True)
    pro_description = fields.String(required=False)
    pro_price = fields.Float(required=True)
    pro_total_sessions = fields.Int(required=True)
    pro_duration_days = fields.Int(required=True)
    pro_image_url = fields.String(required=False)
    pro_therapy_type_id = fields.Int(required=True)
    user_process = fields.String(required=True)