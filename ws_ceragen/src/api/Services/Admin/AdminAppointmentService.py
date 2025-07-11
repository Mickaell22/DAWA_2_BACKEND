from flask_restful import Resource
from ...Components.Admin.AdminAppointmentComponent import AppointmentComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.AppointmentRequest import (
    AppointmentScheduleRequest,
    AppointmentRescheduleRequest,
    AppointmentAvailabilityRequest
)
from ...Components.Security.TokenComponent import TokenComponent
from datetime import datetime


class AdminAppointmentService_get(Resource):
    @staticmethod
    def get():
        """Obtener todas las citas"""
        try:
            HandleLogs.write_log("Listado de Citas")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Parámetros opcionales para filtro de fechas
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')

            # Obtener citas
            res = AppointmentComponent.list_all_appointments(start_date, end_date)
            if res:
                return response_success(res)
            else:
                return response_not_found()

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_getbyid(Resource):
    @staticmethod
    def get(appointment_id):
        """Obtener cita por ID"""
        try:
            HandleLogs.write_log(f"Obtener cita por ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener cita
            res = AppointmentComponent.get_appointment_by_id(appointment_id)
            if res:
                return response_success(res)
            else:
                return response_not_found()

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_schedule(Resource):
    @staticmethod
    def post():
        """Agendar nueva cita"""
        try:
            HandleLogs.write_log("Agendar nueva cita")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener datos del request
            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("Error en los datos para procesar")

            # Validar con el schema
            schema = AppointmentScheduleRequest()
            errors = schema.validate(data_to_insert)
            if errors:
                HandleLogs.write_error(f"Error al validar request: {errors}")
                return response_error(f"Error al validar request: {errors}")

            # Agendar cita
            result = AppointmentComponent.schedule_appointment(data_to_insert)

            if result['result']:
                return response_success(f"Cita agendada con ID: {result['data']}")
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_reschedule(Resource):
    @staticmethod
    def patch():
        """Reagendar cita existente"""
        try:
            HandleLogs.write_log("Reagendar cita")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener datos del request
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Error en los datos para procesar")

            # Validar con el schema
            schema = AppointmentRescheduleRequest()
            errors = schema.validate(data_to_update)
            if errors:
                HandleLogs.write_error(f"Error al validar request: {errors}")
                return response_error(f"Error al validar request: {errors}")

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Reagendar cita
            result = AppointmentComponent.reschedule_appointment(
                data_to_update['sec_id'],
                data_to_update['new_agend_date'],
                user_process
            )

            if result['result']:
                return response_success(data_to_update)
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_cancel(Resource):
    @staticmethod
    def delete(appointment_id):
        """Cancelar cita"""
        try:
            HandleLogs.write_log(f"Cancelar cita ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Cancelar cita
            result = AppointmentComponent.cancel_appointment(appointment_id, user_process)

            if result['result']:
                return response_success(result['message'])
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_execute(Resource):
    @staticmethod
    def patch(appointment_id):
        """Marcar sesión como ejecutada"""
        try:
            HandleLogs.write_log(f"Ejecutar sesión ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Marcar como ejecutada
            result = AppointmentComponent.mark_session_as_executed(appointment_id, user_process)

            if result['result']:
                return response_success(result['message'])
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_availability(Resource):
    @staticmethod
    def post():
        """Verificar disponibilidad para fecha/hora específica"""
        try:
            HandleLogs.write_log("Verificar disponibilidad")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener datos del request
            data = request.get_json()
            if not data:
                return response_error("Error en los datos para procesar")

            # Validar con el schema
            schema = AppointmentAvailabilityRequest()
            errors = schema.validate(data)
            if errors:
                HandleLogs.write_error(f"Error al validar request: {errors}")
                return response_error(f"Error al validar request: {errors}")

            # Convertir string a datetime
            check_datetime = datetime.fromisoformat(data['date_time'].replace('Z', ''))

            # Verificar disponibilidad
            availability = AppointmentComponent.check_availability(
                check_datetime,
                data['therapy_type_id'],
                data.get('staff_id')
            )

            return response_success(availability)

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_calendar(Resource):
    @staticmethod
    def get():
        """Obtener citas para el calendario (formato específico)"""
        try:
            HandleLogs.write_log("Obtener citas para calendario")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Parámetros del calendario
            start_date = request.args.get('start', required=True)
            end_date = request.args.get('end', required=True)

            # Obtener citas
            appointments = AppointmentComponent.list_all_appointments(start_date, end_date)

            # Formatear para react-big-calendar
            calendar_events = []
            if appointments:
                for apt in appointments:
                    event = {
                        'id': apt['sec_id'],
                        'title': f"{apt['patient_name']} - {apt['therapy_name']}",
                        'start': apt['sec_ses_agend_date'],
                        'end': apt['sec_ses_agend_date'],  # Calcular end basado en duración
                        'resource': {
                            'patient_name': apt['patient_name'],
                            'therapy_type': apt['therapy_type'],
                            'staff_name': apt['staff_name'],
                            'consumed': apt['ses_consumed'],
                            'invoice_number': apt.get('inv_number', ''),
                            'patient_phone': apt.get('patient_phone', '')
                        }
                    }
                    calendar_events.append(event)

            return response_success(calendar_events)

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


# ========== SERVICIOS AUXILIARES ==========

class AdminAppointmentService_therapy_types(Resource):
    @staticmethod
    def get():
        """Obtener tipos de terapia"""
        try:
            HandleLogs.write_log("Obtener tipos de terapia")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            res = AppointmentComponent.get_therapy_types()
            return response_success(res)

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_medical_staff(Resource):
    @staticmethod
    def get():
        """Obtener personal médico"""
        try:
            HandleLogs.write_log("Obtener personal médico")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            therapy_type_id = request.args.get('therapy_type_id')
            res = AppointmentComponent.get_medical_staff(therapy_type_id)
            return response_success(res)

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class AdminAppointmentService_products(Resource):
    @staticmethod
    def get(therapy_type_id):
        """Obtener productos por tipo de terapia"""
        try:
            HandleLogs.write_log(f"Obtener productos para terapia: {therapy_type_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            res = AppointmentComponent.get_products_by_therapy_type(therapy_type_id)
            return response_success(res)

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminAppointmentService_register_session(Resource):
    @staticmethod
    def patch(appointment_id):
        """Registrar una sesión realizada (incrementar sec_ses_number)"""
        try:
            HandleLogs.write_log(f"Registrar sesión para cita ID: {appointment_id}")

            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            user_process = TokenComponent.User(token)

            # Lógica: incrementar sec_ses_number y dejar status en 'scheduled' o 'pendiente'
            from ...Components.Admin.AdminAppointmentComponent import AppointmentComponent
            result = AppointmentComponent.register_session(appointment_id, user_process)
            if result['result']:
                return response_success(result['message'])
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))