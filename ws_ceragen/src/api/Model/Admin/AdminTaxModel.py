from datetime import datetime
from decimal import Decimal


class AdminTaxModel:
    def __init__(self,
                 tax_id=None,
                 tax_name=None,
                 tax_percentage=None,
                 tax_description=None,
                 tax_state=True,
                 user_created=None,
                 date_created=None,
                 user_modified=None,
                 date_modified=None,
                 user_deleted=None,
                 date_deleted=None):

        self.tax_id = tax_id
        self.tax_name = tax_name
        self.tax_percentage = tax_percentage
        self.tax_description = tax_description
        self.tax_state = tax_state
        self.user_created = user_created
        self.date_created = date_created
        self.user_modified = user_modified
        self.date_modified = date_modified
        self.user_deleted = user_deleted
        self.date_deleted = date_deleted

    def to_dict(self):
        """Convertir el modelo a diccionario"""
        return {
            'tax_id': self.tax_id,
            'tax_name': self.tax_name,
            'tax_percentage': float(self.tax_percentage) if self.tax_percentage else None,
            'tax_description': self.tax_description,
            'tax_state': self.tax_state,
            'user_created': self.user_created,
            'date_created': self.date_created.isoformat() if isinstance(self.date_created,
                                                                        datetime) else self.date_created,
            'user_modified': self.user_modified,
            'date_modified': self.date_modified.isoformat() if isinstance(self.date_modified,
                                                                          datetime) else self.date_modified,
            'user_deleted': self.user_deleted,
            'date_deleted': self.date_deleted.isoformat() if isinstance(self.date_deleted,
                                                                        datetime) else self.date_deleted
        }

    @staticmethod
    def from_dict(data):
        """Crear instancia del modelo desde diccionario"""
        return AdminTaxModel(
            tax_id=data.get('tax_id'),
            tax_name=data.get('tax_name'),
            tax_percentage=Decimal(str(data.get('tax_percentage'))) if data.get('tax_percentage') is not None else None,
            tax_description=data.get('tax_description'),
            tax_state=data.get('tax_state', True),
            user_created=data.get('user_created'),
            date_created=data.get('date_created'),
            user_modified=data.get('user_modified'),
            date_modified=data.get('date_modified'),
            user_deleted=data.get('user_deleted'),
            date_deleted=data.get('date_deleted')
        )

    @staticmethod
    def from_db_row(row):
        """Crear instancia del modelo desde fila de base de datos"""
        if not row:
            return None

        return AdminTaxModel(
            tax_id=row[0] if len(row) > 0 else None,
            tax_name=row[1] if len(row) > 1 else None,
            tax_percentage=row[2] if len(row) > 2 else None,
            tax_description=row[3] if len(row) > 3 else None,
            tax_state=row[4] if len(row) > 4 else True,
            user_created=row[5] if len(row) > 5 else None,
            date_created=row[6] if len(row) > 6 else None,
            user_modified=row[7] if len(row) > 7 else None,
            date_modified=row[8] if len(row) > 8 else None,
            user_deleted=row[9] if len(row) > 9 else None,
            date_deleted=row[10] if len(row) > 10 else None
        )

    def __str__(self):
        return f"AdminTax(id={self.tax_id}, name='{self.tax_name}', percentage={self.tax_percentage}%)"

    def __repr__(self):
        return self.__str__()

    def is_active(self):
        """Verificar si el impuesto está activo"""
        return self.tax_state is True

    def get_percentage_as_decimal(self):
        """Obtener el porcentaje como decimal para cálculos"""
        if self.tax_percentage:
            return self.tax_percentage / 100
        return Decimal('0')

    def calculate_tax_amount(self, base_amount):
        """Calcular el monto del impuesto sobre un monto base"""
        if not self.tax_percentage or not base_amount:
            return Decimal('0')

        base_decimal = Decimal(str(base_amount))
        percentage_decimal = self.get_percentage_as_decimal()

        return base_decimal * percentage_decimal

    def validate(self):
        """Validar que el modelo tenga datos válidos"""
        errors = []

        if not self.tax_name or not self.tax_name.strip():
            errors.append("El nombre del impuesto es requerido")

        if self.tax_percentage is None:
            errors.append("El porcentaje del impuesto es requerido")
        elif self.tax_percentage < 0:
            errors.append("El porcentaje del impuesto no puede ser negativo")
        elif self.tax_percentage > 100:
            errors.append("El porcentaje del impuesto no puede ser mayor a 100%")

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }