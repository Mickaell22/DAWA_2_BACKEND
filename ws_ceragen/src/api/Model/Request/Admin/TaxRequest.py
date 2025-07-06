import re
from decimal import Decimal, InvalidOperation


class TaxInsertRequest:
    @staticmethod
    def validate_tax_insert(data):
        """Validar datos para crear un nuevo impuesto"""
        errors = []

        # Validar tax_name (requerido)
        tax_name = data.get('tax_name', '').strip()
        if not tax_name:
            errors.append("El nombre del impuesto es requerido")
        elif len(tax_name) < 2:
            errors.append("El nombre del impuesto debe tener al menos 2 caracteres")
        elif len(tax_name) > 50:
            errors.append("El nombre del impuesto no puede tener más de 50 caracteres")
        elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\d\.\-\%\(\)]+$', tax_name):
            errors.append("El nombre del impuesto contiene caracteres no válidos")

        # Validar tax_percentage (requerido)
        tax_percentage = data.get('tax_percentage')
        if tax_percentage is None:
            errors.append("El porcentaje del impuesto es requerido")
        else:
            try:
                percentage_decimal = Decimal(str(tax_percentage))
                if percentage_decimal < 0:
                    errors.append("El porcentaje del impuesto no puede ser negativo")
                elif percentage_decimal > 100:
                    errors.append("El porcentaje del impuesto no puede ser mayor a 100%")
                # Validar que tenga máximo 2 decimales
                if percentage_decimal.as_tuple().exponent < -2:
                    errors.append("El porcentaje del impuesto no puede tener más de 2 decimales")
            except (InvalidOperation, ValueError, TypeError):
                errors.append("El porcentaje del impuesto debe ser un número válido")

        # Validar tax_description (opcional)
        tax_description = data.get('tax_description', '').strip()
        if tax_description and len(tax_description) > 500:
            errors.append("La descripción del impuesto no puede tener más de 500 caracteres")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }


class TaxUpdateRequest:
    @staticmethod
    def validate_tax_update(data):
        """Validar datos para actualizar un impuesto existente"""
        errors = []

        # Validar tax_name (requerido)
        tax_name = data.get('tax_name', '').strip()
        if not tax_name:
            errors.append("El nombre del impuesto es requerido")
        elif len(tax_name) < 2:
            errors.append("El nombre del impuesto debe tener al menos 2 caracteres")
        elif len(tax_name) > 50:
            errors.append("El nombre del impuesto no puede tener más de 50 caracteres")
        elif not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s\d\.\-\%\(\)]+$', tax_name):
            errors.append("El nombre del impuesto contiene caracteres no válidos")

        # Validar tax_percentage (requerido)
        tax_percentage = data.get('tax_percentage')
        if tax_percentage is None:
            errors.append("El porcentaje del impuesto es requerido")
        else:
            try:
                percentage_decimal = Decimal(str(tax_percentage))
                if percentage_decimal < 0:
                    errors.append("El porcentaje del impuesto no puede ser negativo")
                elif percentage_decimal > 100:
                    errors.append("El porcentaje del impuesto no puede ser mayor a 100%")
                # Validar que tenga máximo 2 decimales
                if percentage_decimal.as_tuple().exponent < -2:
                    errors.append("El porcentaje del impuesto no puede tener más de 2 decimales")
            except (InvalidOperation, ValueError, TypeError):
                errors.append("El porcentaje del impuesto debe ser un número válido")

        # Validar tax_description (opcional)
        tax_description = data.get('tax_description', '').strip()
        if tax_description and len(tax_description) > 500:
            errors.append("La descripción del impuesto no puede tener más de 500 caracteres")

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }


class TaxValidation:
    @staticmethod
    def validate_tax_id(tax_id):
        """Validar que el ID del impuesto sea válido"""
        try:
            tax_id_int = int(tax_id)
            return tax_id_int > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def clean_tax_data(data):
        """Limpiar y normalizar datos del impuesto"""
        cleaned_data = {}

        # Limpiar nombre
        if 'tax_name' in data:
            name = data['tax_name']
            if name:
                # Remover espacios extra y normalizar
                cleaned_data['tax_name'] = ' '.join(str(name).strip().split())
            else:
                cleaned_data['tax_name'] = ''

        # Limpiar porcentaje
        if 'tax_percentage' in data:
            try:
                # Convertir a float primero para manejar strings
                percentage_value = float(data['tax_percentage'])
                # Redondear a 2 decimales
                cleaned_data['tax_percentage'] = round(percentage_value, 2)
            except (ValueError, TypeError):
                cleaned_data['tax_percentage'] = data['tax_percentage']

        # Limpiar descripción
        if 'tax_description' in data:
            description = data['tax_description']
            if description:
                # Limpiar espacios extra pero preservar saltos de línea
                cleaned_data['tax_description'] = str(description).strip()
            else:
                cleaned_data['tax_description'] = None

        return cleaned_data

    @staticmethod
    def sanitize_tax_name(name):
        """Sanitizar el nombre del impuesto"""
        if not name:
            return ""

        # Convertir a string y limpiar
        name = str(name).strip()

        # Remover caracteres peligrosos para SQL
        dangerous_chars = ["'", '"', ";", "--", "/*", "*/", "xp_", "sp_"]
        for char in dangerous_chars:
            name = name.replace(char, "")

        # Limitar longitud
        if len(name) > 50:
            name = name[:50]

        return name

    @staticmethod
    def validate_percentage_range(percentage):
        """Validar que el porcentaje esté en un rango válido"""
        try:
            percent = float(percentage)
            return 0 <= percent <= 100
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
    def validate_business_rules(tax_data, existing_taxes=None):
        """Validar reglas de negocio específicas"""
        errors = []

        # Regla: No puede haber dos impuestos con el mismo nombre
        tax_name = tax_data.get('tax_name', '').strip().lower()
        if existing_taxes:
            for existing_tax in existing_taxes:
                if existing_tax.get('tax_name', '').strip().lower() == tax_name:
                    errors.append(f"Ya existe un impuesto con el nombre '{tax_data.get('tax_name')}'")
                    break

        # Regla: Porcentajes comunes de validación
        percentage = tax_data.get('tax_percentage')
        if percentage is not None:
            try:
                percent = float(percentage)
                # Advertir sobre porcentajes inusuales
                if percent > 50:
                    errors.append("Advertencia: El porcentaje es mayor al 50%, verifique si es correcto")
            except (ValueError, TypeError):
                pass

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": [error for error in errors if error.startswith("Advertencia:")]
        }

    @staticmethod
    def prepare_tax_for_database(tax_data):
        """Preparar datos del impuesto para insertar en base de datos"""
        prepared_data = {}

        # Preparar nombre
        if 'tax_name' in tax_data:
            prepared_data['tax_name'] = TaxValidation.sanitize_tax_name(tax_data['tax_name'])

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