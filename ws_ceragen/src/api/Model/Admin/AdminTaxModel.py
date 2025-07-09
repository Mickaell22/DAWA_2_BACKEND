# your_project_root/src/api/Model/Admin/AdminTaxModel.py

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
        """Convierte el objeto a un diccionario para JSON/Marshmallow."""
        return {
            'tax_id': self.tax_id,
            'tax_name': self.tax_name,
            'tax_percentage': float(self.tax_percentage) if self.tax_percentage is not None else None,
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
        """Crea una instancia de AdminTaxModel desde un diccionario."""
        return AdminTaxModel(
            tax_id=data.get('tax_id'),
            tax_name=data.get('tax_name'),
            tax_percentage=Decimal(str(data.get('tax_percentage'))) if data.get('tax_percentage') is not None else None,
            tax_description=data.get('tax_description'),
            tax_state=data.get('tax_state', True),  # Por defecto a True si no se especifica
            user_created=data.get('user_created'),
            date_created=data.get('date_created'),
            user_modified=data.get('user_modified'),
            date_modified=data.get('date_modified'),
            user_deleted=data.get('user_deleted'),
            date_deleted=data.get('date_deleted')
        )

    def validate(self):
        """Valida los campos básicos del modelo (uso opcional, Marshmallow es mejor para esto)."""
        errors = []
        if not self.tax_name or not self.tax_name.strip():
            errors.append("El nombre del impuesto es requerido.")
        if self.tax_percentage is None:
            errors.append("El porcentaje del impuesto es requerido.")
        elif not isinstance(self.tax_percentage,
                            (int, float, Decimal)) or self.tax_percentage < 0 or self.tax_percentage > 100:
            errors.append("El porcentaje del impuesto debe ser un número entre 0 y 100.")

        # Considera otras validaciones de negocio aquí si son necesarias antes de interactuar con la DB

        return errors