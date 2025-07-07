from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
import re
from decimal import Decimal, InvalidOperation


class TaxValidationMixin:
    """Mixin con validaciones de negocio comunes para impuestos"""
    
    @staticmethod
    def sanitize_tax_name(name):
        """Sanitizar el nombre del impuesto"""
        if not name:
            return ""

        # Convertir a string y limpiar
        name = str(name).strip()

        # Remover caracteres peligrosos para SQL
        dangerous_chars = ["'", '"', ";", "--", "/", "/", "xp_", "sp_"]
        for char in dangerous_chars:
            name = name.replace(char, "")

        # Limpiar espacios múltiples
        name = ' '.join(name.split())

        return name

    @staticmethod
    def validate_percentage_precision(percentage):
        """Validar que el porcentaje tenga máximo 2 decimales"""
        try:
            decimal_value = Decimal(str(percentage))
            return decimal_value.as_tuple().exponent >= -2
        except (InvalidOperation, ValueError, TypeError):
            return False

    @staticmethod
    def validate_business_rules(tax_name, percentage):
        """Validar reglas de negocio específicas"""
        warnings = []
        
        # Advertir sobre porcentajes inusuales
        if percentage is not None:
            try:
                percent = float(percentage)
                if percent > 50:
                    warnings.append("Advertencia: El porcentaje es mayor al 50%, verifique si es correcto")
                elif percent == 0:
                    warnings.append("Advertencia: El porcentaje es 0%, verifique si es correcto")
            except (ValueError, TypeError):
                pass
        
        return warnings


class AdminTaxInsertRequest(Schema, TaxValidationMixin):
    """Schema para crear un nuevo impuesto"""
    
    tax_name = fields.String(
        required=True,
        validate=[
            validate.Length(min=2, max=50, error="El nombre debe tener entre 2 y 50 caracteres"),
            validate.Regexp(
                r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\d\.\-\%\(\)]+$', 
                error="El nombre contiene caracteres no válidos. Solo se permiten letras, números, espacios, puntos, guiones, % y paréntesis"
            )
        ],
        error_messages={
            'required': 'El nombre del impuesto es obligatorio',
            'null': 'El nombre del impuesto no puede ser nulo',
            'invalid': 'El nombre del impuesto debe ser una cadena de texto'
        }
    )
    
    tax_percentage = fields.Float(
        required=True,
        validate=[
            validate.Range(min=0, max=100, error="El porcentaje debe estar entre 0 y 100")
        ],
        error_messages={
            'required': 'El porcentaje del impuesto es obligatorio',
            'null': 'El porcentaje del impuesto no puede ser nulo',
            'invalid': 'El porcentaje debe ser un número válido'
        }
    )
    
    tax_description = fields.String(
        required=False,
        allow_none=True,
        missing=None,
        validate=[
            validate.Length(max=500, error="La descripción no puede exceder 500 caracteres")
        ],
        error_messages={
            'invalid': 'La descripción debe ser una cadena de texto'
        }
    )
    
    user_process = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=50, error="El usuario debe tener entre 1 y 50 caracteres")
        ],
        error_messages={
            'required': 'El usuario que procesa es obligatorio',
            'null': 'El usuario que procesa no puede ser nulo',
            'invalid': 'El usuario debe ser una cadena de texto'
        }
    )

    @validates('tax_name')
    def validate_tax_name(self, value):
        """Validación adicional para el nombre del impuesto"""
        if value:
            # Remover espacios extra y verificar que no esté vacío
            cleaned_value = value.strip()
            if not cleaned_value:
                raise ValidationError('El nombre del impuesto no puede estar vacío')
            
            # Verificar que no sea solo números
            if cleaned_value.replace('.', '').replace('-', '').replace('%', '').replace('(', '').replace(')', '').replace(' ', '').isdigit():
                raise ValidationError('El nombre del impuesto no puede ser solo números')

    @validates('tax_percentage')
    def validate_tax_percentage(self, value):
        """Validación adicional para el porcentaje"""
        if value is not None:
            # Verificar que tenga máximo 2 decimales
            if not self.validate_percentage_precision(value):
                raise ValidationError('El porcentaje no puede tener más de 2 decimales')

    @post_load
    def clean_and_validate_data(self, data, **kwargs):
        """Limpiar y validar datos después de la validación de esquema"""
        # Limpiar y sanitizar nombre
        if 'tax_name' in data and data['tax_name']:
            data['tax_name'] = self.sanitize_tax_name(data['tax_name'])
        
        # Limpiar descripción
        if 'tax_description' in data and data['tax_description']:
            data['tax_description'] = data['tax_description'].strip()
            # Convertir cadena vacía a None
            if not data['tax_description']:
                data['tax_description'] = None
        
        # Limpiar usuario
        if 'user_process' in data and data['user_process']:
            data['user_process'] = data['user_process'].strip()
        
        # Redondear porcentaje a 2 decimales
        if 'tax_percentage' in data and data['tax_percentage'] is not None:
            data['tax_percentage'] = round(data['tax_percentage'], 2)
        
        # Validar reglas de negocio y agregar advertencias como metadata
        if 'tax_name' in data and 'tax_percentage' in data:
            warnings = self.validate_business_rules(data['tax_name'], data['tax_percentage'])
            if warnings:
                # Las advertencias se pueden manejar en el servicio si es necesario
                data['_warnings'] = warnings
        
        return data


class AdminTaxUpdateRequest(Schema, TaxValidationMixin):
    """Schema para actualizar un impuesto existente"""
    
    tax_id = fields.Int(
        required=True,
        validate=[
            validate.Range(min=1, error="El ID del impuesto debe ser un número positivo")
        ],
        error_messages={
            'required': 'El ID del impuesto es obligatorio',
            'null': 'El ID del impuesto no puede ser nulo',
            'invalid': 'El ID del impuesto debe ser un número entero'
        }
    )
    
    tax_name = fields.String(
        required=True,
        validate=[
            validate.Length(min=2, max=50, error="El nombre debe tener entre 2 y 50 caracteres"),
            validate.Regexp(
                r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\d\.\-\%\(\)]+$', 
                error="El nombre contiene caracteres no válidos. Solo se permiten letras, números, espacios, puntos, guiones, % y paréntesis"
            )
        ],
        error_messages={
            'required': 'El nombre del impuesto es obligatorio',
            'null': 'El nombre del impuesto no puede ser nulo',
            'invalid': 'El nombre del impuesto debe ser una cadena de texto'
        }
    )
    
    tax_percentage = fields.Float(
        required=True,
        validate=[
            validate.Range(min=0, max=100, error="El porcentaje debe estar entre 0 y 100")
        ],
        error_messages={
            'required': 'El porcentaje del impuesto es obligatorio',
            'null': 'El porcentaje del impuesto no puede ser nulo',
            'invalid': 'El porcentaje debe ser un número válido'
        }
    )
    
    tax_description = fields.String(
        required=False,
        allow_none=True,
        missing=None,
        validate=[
            validate.Length(max=500, error="La descripción no puede exceder 500 caracteres")
        ],
        error_messages={
            'invalid': 'La descripción debe ser una cadena de texto'
        }
    )
    
    user_process = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=50, error="El usuario debe tener entre 1 y 50 caracteres")
        ],
        error_messages={
            'required': 'El usuario que procesa es obligatorio',
            'null': 'El usuario que procesa no puede ser nulo',
            'invalid': 'El usuario debe ser una cadena de texto'
        }
    )

    @validates('tax_name')
    def validate_tax_name(self, value):
        """Validación adicional para el nombre del impuesto"""
        if value:
            # Remover espacios extra y verificar que no esté vacío
            cleaned_value = value.strip()
            if not cleaned_value:
                raise ValidationError('El nombre del impuesto no puede estar vacío')
            
            # Verificar que no sea solo números
            if cleaned_value.replace('.', '').replace('-', '').replace('%', '').replace('(', '').replace(')', '').replace(' ', '').isdigit():
                raise ValidationError('El nombre del impuesto no puede ser solo números')

    @validates('tax_percentage')
    def validate_tax_percentage(self, value):
        """Validación adicional para el porcentaje"""
        if value is not None:
            # Verificar que tenga máximo 2 decimales
            if not self.validate_percentage_precision(value):
                raise ValidationError('El porcentaje no puede tener más de 2 decimales')

    @post_load
    def clean_and_validate_data(self, data, **kwargs):
        """Limpiar y validar datos después de la validación de esquema"""
        # Limpiar y sanitizar nombre
        if 'tax_name' in data and data['tax_name']:
            data['tax_name'] = self.sanitize_tax_name(data['tax_name'])
        
        # Limpiar descripción
        if 'tax_description' in data and data['tax_description']:
            data['tax_description'] = data['tax_description'].strip()
            # Convertir cadena vacía a None
            if not data['tax_description']:
                data['tax_description'] = None
        
        # Limpiar usuario
        if 'user_process' in data and data['user_process']:
            data['user_process'] = data['user_process'].strip()
        
        # Redondear porcentaje a 2 decimales
        if 'tax_percentage' in data and data['tax_percentage'] is not None:
            data['tax_percentage'] = round(data['tax_percentage'], 2)
        
        # Validar reglas de negocio y agregar advertencias como metadata
        if 'tax_name' in data and 'tax_percentage' in data:
            warnings = self.validate_business_rules(data['tax_name'], data['tax_percentage'])
            if warnings:
                # Las advertencias se pueden manejar en el servicio si es necesario
                data['_warnings'] = warnings
        
        return data


class AdminTaxDeleteRequest(Schema):
    """Schema para eliminar un impuesto"""
    tax_id = fields.Int(
        required=True,
        validate=[
            validate.Range(min=1, error="El ID del impuesto debe ser un número positivo")
        ],
        error_messages={
            'required': 'El ID del impuesto es obligatorio',
            'null': 'El ID del impuesto no puede ser nulo',
            'invalid': 'El ID del impuesto debe ser un número entero'
        }
    )
    
    user_process = fields.String(
        required=True,
        validate=[
            validate.Length(min=1, max=50, error="El usuario debe tener entre 1 y 50 caracteres")
        ],
        error_messages={
            'required': 'El usuario que procesa es obligatorio',
            'null': 'El usuario que procesa no puede ser nulo',
            'invalid': 'El usuario debe ser una cadena de texto'
        }
    )

    @post_load
    def clean_data(self, data, **kwargs):
        """Limpiar y normalizar los datos después de la validación"""
        if 'user_process' in data and data['user_process']:
            data['user_process'] = data['user_process'].strip()
        
        return data


class AdminTaxResponse(Schema):
    """Schema para la respuesta de un impuesto"""
    tax_id = fields.Int()
    tax_name = fields.String()
    tax_percentage = fields.Float()
    tax_description = fields.String(allow_none=True)
    tax_state = fields.Boolean()
    user_created = fields.String(allow_none=True)
    date_created = fields.String(allow_none=True)
    user_modified = fields.String(allow_none=True)
    date_modified = fields.String(allow_none=True)
    user_deleted = fields.String(allow_none=True)
    date_deleted = fields.String(allow_none=True)


class TaxUtilities:
    """Utilidades adicionales para manejo de impuestos"""
    
    @staticmethod
    def validate_tax_id(tax_id):
        """Validar que el ID del impuesto sea válido"""
        try:
            tax_id_int = int(tax_id)
            return tax_id_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def format_percentage_for_display(percentage):
        """Formatear porcentaje para mostrar"""
        try:
            percent = float(percentage)
            return f"{percent:.2f}%"
        except (ValueError, TypeError):
            return "0.00%"

    @staticmethod
    def prepare_tax_for_database(tax_data):
        """Preparar datos del impuesto para insertar en base de datos"""
        prepared_data = {}

        # Preparar nombre
        if 'tax_name' in tax_data:
            prepared_data['tax_name'] = TaxValidationMixin.sanitize_tax_name(tax_data['tax_name'])

        # Preparar porcentaje
        if 'tax_percentage' in tax_data:
            try:
                prepared_data['tax_percentage'] = Decimal(str(tax_data['tax_percentage']))
            except (InvalidOperation, ValueError):
                prepared_data['tax_percentage'] = Decimal('0')

        # Preparar descripción
        if 'tax_description' in tax_data:
            description = tax_data['tax_description']
            if description:
                prepared_data['tax_description'] = str(description).strip()[:500]  # Limitar a 500 chars
            else:
                prepared_data['tax_description'] = None

        return prepared_data


# Clases de compatibilidad con la versión anterior
class TaxInsertRequest:
    """Clase de compatibilidad - usar AdminTaxInsertRequest"""
    @staticmethod
    def validate_tax_insert(data):
        try:
            schema = AdminTaxInsertRequest()
            schema.load(data)
            return {"valid": True, "errors": []}
        except ValidationError as err:
            errors = []
            for field, messages in err.messages.items():
                if isinstance(messages, list):
                    errors.extend(messages)
                else:
                    errors.append(str(messages))
            return {"valid": False, "errors": errors}


class TaxUpdateRequest:
    """Clase de compatibilidad - usar AdminTaxUpdateRequest"""
    @staticmethod
    def validate_tax_update(data):
        try:
            schema = AdminTaxUpdateRequest()
            schema.load(data)
            return {"valid": True, "errors": []}
        except ValidationError as err:
            errors = []
            for field, messages in err.messages.items():
                if isinstance(messages, list):
                    errors.extend(messages)
                else:
                    errors.append(str(messages))
            return {"valid": False, "errors": errors}


class TaxValidation:
    """Clase de compatibilidad - usar TaxUtilities y TaxValidationMixin"""
    @staticmethod
    def validate_tax_id(tax_id):
        return TaxUtilities.validate_tax_id(tax_id)
    
    @staticmethod
    def clean_tax_data(data):
        return TaxUtilities.prepare_tax_for_database(data)
    
    @staticmethod
    def sanitize_tax_name(name):
        return TaxValidationMixin.sanitize_tax_name(name)
    
    @staticmethod
    def validate_percentage_range(percentage):
        try:
            percent = float(percentage)
            return 0 <= percent <= 100
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def format_percentage_for_display(percentage):
        return TaxUtilities.format_percentage_for_display(percentage)
    
    @staticmethod
    def validate_business_rules(tax_data, existing_taxes=None):
        warnings = TaxValidationMixin.validate_business_rules(
            tax_data.get('tax_name'), 
            tax_data.get('tax_percentage')
        )
        return {
            "valid": True,
            "errors": [],
            "warnings": warnings
        }
    
    @staticmethod
    def prepare_tax_for_database(tax_data):
        return TaxUtilities.prepare_tax_for_database(tax_data)


# Instancias para uso directo
admin_tax_insert_schema = AdminTaxInsertRequest()
admin_tax_update_schema = AdminTaxUpdateRequest()
admin_tax_delete_schema = AdminTaxDeleteRequest()
admin_tax_response_schema = AdminTaxResponse()
admin_tax_list_response_schema = AdminTaxResponse(many=True)