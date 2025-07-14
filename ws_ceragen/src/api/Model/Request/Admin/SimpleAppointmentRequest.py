from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import datetime


class SimpleAppointmentScheduleRequest(Schema):
    """Schema simplificado para agendar nueva cita"""

    # Campos obligatorios
    patient_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=200),
        error_messages={'required': 'El nombre del paciente es obligatorio'}
    )
    sec_ses_agend_date = fields.Str(
        required=False, allow_none=True,
        error_messages={'required': 'La fecha y hora de la cita es obligatoria'}
    )

    # Campos opcionales del paciente
    patient_phone = fields.Str(
        required=False,
        validate=validate.Length(max=20),
        missing=None,
        allow_none=True
    )
    patient_email = fields.Email(
        required=False,
        missing=None,
        allow_none=True
    )
    patient_id = fields.Int(
        required=False,
        validate=validate.Range(min=1),
        missing=None,
        allow_none=True
    )

    # Campos de la sesión
    sec_ses_number = fields.Int(
        required=False,
        validate=validate.Range(min=1),
        missing=1
    )
    duration_minutes = fields.Int(
        required=False,
        validate=validate.Range(min=15, max=480),  # Entre 15 minutos y 8 horas
        missing=60
    )

    # Campos de terapia
    therapy_name = fields.Str(
        required=False,
        validate=validate.Length(max=200),
        missing=None,
        allow_none=True
    )
    therapy_type = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        missing=None,
        allow_none=True
    )
    product_name = fields.Str(
        required=False,
        validate=validate.Length(max=200),
        missing=None,
        allow_none=True
    )

    # Campos del terapeuta
    therapist_name = fields.Str(
        required=False,
        validate=validate.Length(max=200),
        missing=None,
        allow_none=True
    )
    therapist_specialty = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        missing=None,
        allow_none=True
    )

    # Campos adicionales
    notes = fields.Str(
        required=False,
        missing=None,
        allow_none=True
    )
    price = fields.Decimal(
        required=False,
        validate=validate.Range(min=0),
        missing=None,
        allow_none=True
    )

    @validates('sec_ses_agend_date')
    def validate_appointment_date(self, value):
        """Validar que la fecha de la cita sea válida y futura"""
        try:
            # Intentar parsear la fecha
            appointment_date = datetime.fromisoformat(value.replace('Z', ''))

            # Verificar que no sea en el pasado
            if appointment_date < datetime.now():
                raise ValidationError('La fecha de la cita no puede ser en el pasado')

        except ValueError:
            raise ValidationError('Formato de fecha inválido. Use formato ISO (YYYY-MM-DDTHH:MM:SS)')


class SimpleAppointmentRescheduleRequest(Schema):
    """Schema simplificado para reagendar cita"""

    sec_id = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        error_messages={'required': 'El ID de la cita es obligatorio'}
    )
    new_agend_date = fields.Str(
        required=True,
        error_messages={'required': 'La nueva fecha es obligatoria'}
    )

    @validates('new_agend_date')
    def validate_new_date(self, value):
        """Validar nueva fecha"""
        try:
            new_date = datetime.fromisoformat(value.replace('Z', ''))
            if new_date < datetime.now():
                raise ValidationError('La nueva fecha no puede ser en el pasado')
        except ValueError:
            raise ValidationError('Formato de fecha inválido')


class SimpleAppointmentUpdateRequest(Schema):
    """Schema simplificado para actualizar cita"""

    # Todos los campos son opcionales para updates parciales
    patient_name = fields.Str(
        required=False,
        validate=validate.Length(min=2, max=200)
    )
    patient_phone = fields.Str(
        required=False,
        validate=validate.Length(max=20),
        allow_none=True
    )
    patient_email = fields.Email(
        required=False,
        allow_none=True
    )
    patient_id = fields.Int(
        required=False,
        validate=validate.Range(min=1),
        allow_none=True
    )
    sec_ses_number = fields.Int(
        required=False,
        validate=validate.Range(min=1)
    )
    sec_ses_agend_date = fields.Str(
        required=False
    )
    therapy_name = fields.Str(
        required=False,
        validate=validate.Length(max=200),
        allow_none=True
    )
    therapy_type = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        allow_none=True
    )
    product_name = fields.Str(
        required=False,
        validate=validate.Length(max=200),
        allow_none=True
    )
    therapist_name = fields.Str(
        required=False,
        validate=validate.Length(max=200),
        allow_none=True
    )
    therapist_specialty = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        allow_none=True
    )
    duration_minutes = fields.Int(
        required=False,
        validate=validate.Range(min=15, max=480)
    )
    notes = fields.Str(
        required=False,
        allow_none=True
    )
    price = fields.Decimal(
        required=False,
        validate=validate.Range(min=0),
        allow_none=True
    )
    status = fields.Str(
        required=False,
        validate=validate.OneOf(['scheduled', 'completed', 'cancelled', 'no_show'])
    )

    @validates('sec_ses_agend_date')
    def validate_appointment_date(self, value):
        """Validar fecha si se proporciona"""
        if value:  # Solo validar si se proporciona
            try:
                appointment_date = datetime.fromisoformat(value.replace('Z', ''))
                if appointment_date < datetime.now():
                    raise ValidationError('La fecha de la cita no puede ser en el pasado')
            except ValueError:
                raise ValidationError('Formato de fecha inválido')


class SimpleAppointmentExecuteRequest(Schema):
    """Schema para marcar sesión como ejecutada"""

    execution_notes = fields.Str(
        required=False,
        missing='Sesión completada',
        validate=validate.Length(max=500)
    )


# Función de utilidad para validar requests
def validate_request_data(schema_class, data):
    """
    Función helper para validar datos de request

    Args:
        schema_class: Clase del schema a usar
        data: Datos a validar

    Returns:
        dict: Datos validados o errores
    """
    try:
        schema = schema_class()
        result = schema.load(data)
        return {'success': True, 'data': result, 'errors': None}
    except ValidationError as err:
        return {'success': False, 'data': None, 'errors': err.messages}
