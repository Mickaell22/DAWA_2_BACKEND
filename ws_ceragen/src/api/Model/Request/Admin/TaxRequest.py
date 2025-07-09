# your_project_root/src/api/Model/Request/Admin/TaxRequest.py

from marshmallow import Schema, fields, validate, post_load, ValidationError
from decimal import Decimal, InvalidOperation


class TaxValidationMixin:
    """Validaciones reutilizables para impuestos."""

    @staticmethod
    def sanitize_name(name):
        if not name:
            return ""
        return ' '.join(str(name).strip().split())

    @staticmethod
    def validate_percentage_precision(percentage):
        try:
            decimal_value = Decimal(str(percentage))
            # Permite hasta 2 decimales para porcentajes
            return decimal_value.as_tuple().exponent >= -2
        except (InvalidOperation, ValueError, TypeError):
            return False


class AdminTaxInsertRequest(Schema, TaxValidationMixin):
    tax_name = fields.String(
        required=True,
        validate=[
            validate.Length(min=2, max=50, error="El nombre del impuesto debe tener entre 2 y 50 caracteres."),
            validate.Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\d\.\-\%()]+$',
                            error="El nombre del impuesto contiene caracteres inválidos.")
        ]
    )
    tax_percentage = fields.Float(
        required=True,
        validate=[
            validate.Range(min=0, max=100, error="El porcentaje del impuesto debe estar entre 0 y 100."),
        ]
    )
    tax_description = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=500, error="La descripción del impuesto no debe exceder los 500 caracteres.")
    )
    user_process = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50,
                                 error="El usuario de proceso es requerido y debe tener entre 1 y 50 caracteres.")
    )

    @post_load
    def process_data(self, data, **kwargs):
        data['tax_name'] = self.sanitize_name(data['tax_name'])
        data['tax_description'] = data['tax_description'].strip() if data.get('tax_description') else None
        data['user_process'] = data['user_process'].strip()

        # Validar precisión después de la carga
        if not self.validate_percentage_precision(data['tax_percentage']):
            raise ValidationError("El porcentaje del impuesto no puede tener más de 2 decimales.",
                                  field_name="tax_percentage")

        data['tax_percentage'] = round(Decimal(str(data['tax_percentage'])), 2)  # Asegurar 2 decimales
        return data


class AdminTaxUpdateRequest(AdminTaxInsertRequest):
    tax_id = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="ID de impuesto inválido.")
    )


class AdminTaxDeleteRequest(Schema):
    tax_id = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="ID de impuesto inválido.")
    )
    user_process = fields.String(
        required=True,
        validate=validate.Length(min=1, max=50,
                                 error="El usuario de proceso es requerido y debe tener entre 1 y 50 caracteres.")
    )

    @post_load
    def clean_delete_data(self, data, **kwargs):
        data['user_process'] = data['user_process'].strip()
        return data


class AdminTaxResponse(Schema):
    """Esquema para serializar un solo objeto de impuesto para la respuesta."""
    tax_id = fields.Int()
    tax_name = fields.String()
    tax_percentage = fields.Float()
    tax_description = fields.String(allow_none=True)
    tax_state = fields.Boolean()
    user_created = fields.String()
    date_created = fields.DateTime(format="%Y-%m-%d %H:%M:%S")  # Formato de fecha y hora
    user_modified = fields.String(allow_none=True)
    date_modified = fields.DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True)
    user_deleted = fields.String(allow_none=True)
    date_deleted = fields.DateTime(format="%Y-%m-%d %H:%M:%S", allow_none=True)


class AdminTaxListResponse(Schema):
    """Esquema para serializar una lista de objetos de impuesto para la respuesta."""
    taxes = fields.List(fields.Nested(AdminTaxResponse))


# Instancias de esquemas para usar en los servicios
admin_tax_insert_schema = AdminTaxInsertRequest()
admin_tax_update_schema = AdminTaxUpdateRequest()
admin_tax_delete_schema = AdminTaxDeleteRequest()
admin_tax_response_schema = AdminTaxResponse()
admin_tax_list_response_schema = AdminTaxResponse(many=True)  # Para cuando se devuelve una lista de impuestos