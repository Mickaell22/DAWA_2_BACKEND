from flask_restful import Resource
from ...Components.Admin.SimpleAppointmentComponent import SimpleAppointmentComponent
from ....utils.database.connection_db import DataBaseHandle
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.SimpleAppointmentRequest import (
    SimpleAppointmentScheduleRequest,
    SimpleAppointmentRescheduleRequest,
    SimpleAppointmentUpdateRequest,
    SimpleAppointmentExecuteRequest,
    validate_request_data
)
from ...Components.Security.TokenComponent import TokenComponent
from datetime import datetime


class SimpleAppointmentServiceV2_get(Resource):
    @staticmethod
    def get():
        """Obtener todas las citas con filtros opcionales"""
        try:
            HandleLogs.write_log("📋 Listado de Citas Simplificado V2")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Parámetros opcionales para filtro
            filters = {
                'start_date': request.args.get('start_date'),
                'end_date': request.args.get('end_date'),
                'therapist_name': request.args.get('therapist'),
                'status': request.args.get('status'),
                'patient_name': request.args.get('patient')
            }

            # Filtrar valores None
            filters = {k: v for k, v in filters.items() if v is not None}

            # Obtener citas
            res = SimpleAppointmentComponent.list_all_appointments(
                filters.get('start_date'),
                filters.get('end_date')
            )

            if res is not None:
                # Aplicar filtros adicionales en memoria si es necesario
                if filters.get('therapist_name'):
                    res = [apt for apt in res if
                           apt.get('therapist_name', '').lower().find(filters['therapist_name'].lower()) >= 0]

                if filters.get('status'):
                    res = [apt for apt in res if apt.get('status') == filters['status']]

                if filters.get('patient_name'):
                    res = [apt for apt in res if
                           apt.get('patient_name', '').lower().find(filters['patient_name'].lower()) >= 0]

                if res is not None:
                    return response_success({
                        'appointments': res,
                        'total': len(res),
                        'filters_applied': filters
                    })
                else:
                    return response_success({
                        'appointments': [],
                        'total': 0,
                        'filters_applied': filters
                    })
            else:
                return response_not_found()

        except Exception as err:
            HandleLogs.write_error(f"Error en listado de citas: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_getbyid(Resource):
    @staticmethod
    def get(appointment_id):
        """Obtener cita específica por ID"""
        try:
            HandleLogs.write_log(f"🔍 Obtener cita por ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Validar ID
            try:
                appointment_id = int(appointment_id)
                if appointment_id <= 0:
                    return response_error("ID de cita inválido")
            except (ValueError, TypeError):
                return response_error("ID de cita debe ser un número válido")

            # Obtener cita
            res = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            if res:
                return response_success(res)
            else:
                return response_not_found("Cita no encontrada")

        except Exception as err:
            HandleLogs.write_error(f"Error obteniendo cita: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_schedule(Resource):
    @staticmethod
    def post():
        """Agendar nueva cita con validaciones completas"""
        try:
            HandleLogs.write_log("➕ Agendar nueva cita simplificada V2")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener datos del request
            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("Datos JSON requeridos en el cuerpo de la petición")

            # Validar con el schema
            validation = validate_request_data(SimpleAppointmentScheduleRequest, data_to_insert)
            if not validation['success']:
                HandleLogs.write_error(f"Errores de validación: {validation['errors']}")
                return response_error(f"Errores de validación: {validation['errors']}")

            validated_data = validation['data']

            # Obtener usuario del token
            user_process = TokenComponent.User(token)
            validated_data['user_process'] = user_process

            # Log de datos a insertar (sin información sensible)
            HandleLogs.write_log(
                f"Agendando cita para: {validated_data.get('patient_name')} en {validated_data.get('sec_ses_agend_date')}")

            # Agendar cita
            result = SimpleAppointmentComponent.schedule_appointment(validated_data)

            if result['result']:
                HandleLogs.write_log(f"✅ Cita agendada exitosamente con ID: {result['data']}")
                return response_success({
                    'message': 'Cita agendada exitosamente',
                    'appointment_id': result['data'],
                    'patient_name': validated_data.get('patient_name'),
                    'appointment_date': validated_data.get('sec_ses_agend_date')
                })
            else:
                HandleLogs.write_error(f"Error agendando cita: {result['message']}")
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(f"Error crítico agendando cita: {str(err)}")
            return response_error(f"Error interno del servidor: {str(err)}")


class SimpleAppointmentServiceV2_reschedule(Resource):
    @staticmethod
    def patch():
        """Reagendar cita existente con validaciones"""
        try:
            HandleLogs.write_log("🔄 Reagendar cita simplificada V2")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener datos del request
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Datos JSON requeridos")

            # Validar con el schema
            validation = validate_request_data(SimpleAppointmentRescheduleRequest, data_to_update)
            if not validation['success']:
                return response_error(f"Errores de validación: {validation['errors']}")

            validated_data = validation['data']

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Log de la operación
            HandleLogs.write_log(
                f"Reagendando cita ID: {validated_data['sec_id']} a nueva fecha: {validated_data['new_agend_date']}")

            # Reagendar cita
            result = SimpleAppointmentComponent.reschedule_appointment(
                validated_data['sec_id'],
                validated_data['new_agend_date'],
                user_process
            )

            if result['result']:
                HandleLogs.write_log(f"✅ Cita reagendada exitosamente")
                return response_success({
                    'message': 'Cita reagendada exitosamente',
                    'appointment_id': validated_data['sec_id'],
                    'new_date': validated_data['new_agend_date']
                })
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(f"Error reagendando cita: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_update(Resource):
    @staticmethod
    def put(appointment_id):
        """Actualizar información completa de cita"""
        try:
            HandleLogs.write_log(f"✏️ Actualizar cita ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Validar ID
            try:
                appointment_id = int(appointment_id)
                if appointment_id <= 0:
                    return response_error("ID de cita inválido")
            except (ValueError, TypeError):
                return response_error("ID de cita debe ser un número válido")

            # Obtener datos del request
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Datos JSON requeridos")

            # Validar con el schema
            validation = validate_request_data(SimpleAppointmentUpdateRequest, data_to_update)
            if not validation['success']:
                return response_error(f"Errores de validación: {validation['errors']}")

            validated_data = validation['data']

            # Verificar que hay campos para actualizar
            if not validated_data:
                return response_error("No se proporcionaron campos para actualizar")

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Log de campos a actualizar
            updated_fields = list(validated_data.keys())
            HandleLogs.write_log(f"Actualizando cita {appointment_id}, campos: {', '.join(updated_fields)}")

            # Actualizar cita
            result = SimpleAppointmentComponent.update_appointment(
                appointment_id,
                validated_data,
                user_process
            )

            if result['result']:
                HandleLogs.write_log(f"✅ Cita actualizada exitosamente")
                return response_success({
                    'message': 'Cita actualizada exitosamente',
                    'appointment_id': appointment_id,
                    'updated_fields': updated_fields
                })
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(f"Error actualizando cita: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_cancel(Resource):
    @staticmethod
    def delete(appointment_id):
        """Eliminar cita con validaciones"""
        try:
            HandleLogs.write_log(f"❌ Eliminar cita ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Validar ID
            try:
                appointment_id = int(appointment_id)
                if appointment_id <= 0:
                    return response_error("ID de cita inválido")
            except (ValueError, TypeError):
                return response_error("ID de cita debe ser un número válido")

            # Verificar que la cita existe
            appointment = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            if not appointment:
                return response_not_found("Cita no encontrada")

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Eliminar cita (físico)
            result = SimpleAppointmentComponent.cancel_appointment(appointment_id, user_process)

            if result['result']:
                HandleLogs.write_log(f"✅ Cita eliminada exitosamente")
                return response_success({
                    'message': 'Cita eliminada exitosamente',
                    'appointment_id': appointment_id,
                    'patient_name': appointment.get('patient_name')
                })
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(f"Error eliminando cita: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_execute(Resource):
    @staticmethod
    def patch(appointment_id):
        """Marcar sesión como ejecutada con validaciones"""
        try:
            HandleLogs.write_log(f"✅ Ejecutar sesión ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Validar ID
            try:
                appointment_id = int(appointment_id)
                if appointment_id <= 0:
                    return response_error("ID de cita inválido")
            except (ValueError, TypeError):
                return response_error("ID de cita debe ser un número válido")

            # Verificar que la cita existe y se puede ejecutar
            appointment = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            if not appointment:
                return response_not_found("Cita no encontrada")

            if appointment.get('status') != 'scheduled':
                return response_error(f"No se puede ejecutar una cita con estado: {appointment.get('status')}")

            if appointment.get('ses_consumed'):
                return response_error("La sesión ya fue marcada como ejecutada")

            # Obtener datos opcionales del request
            data = request.get_json() or {}

            # Validar con el schema
            validation = validate_request_data(SimpleAppointmentExecuteRequest, data)
            if not validation['success']:
                return response_error(f"Errores de validación: {validation['errors']}")

            validated_data = validation['data']
            execution_notes = validated_data.get('execution_notes', 'Sesión completada')

            # Obtener usuario del token
            user_process = TokenComponent.User(token)

            # Ejecutar sesión
            result = SimpleAppointmentComponent.execute_session(
                appointment_id,
                user_process,
                execution_notes
            )

            if result['result']:
                HandleLogs.write_log(f"✅ Sesión ejecutada exitosamente")
                return response_success({
                    'message': 'Sesión marcada como ejecutada exitosamente',
                    'appointment_id': appointment_id,
                    'patient_name': appointment.get('patient_name'),
                    'execution_notes': execution_notes
                })
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(f"Error ejecutando sesión: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_statistics(Resource):
    @staticmethod
    def get():
        """Obtener estadísticas con filtros opcionales"""
        try:
            HandleLogs.write_log("📊 Estadísticas de citas V2")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Parámetro opcional para filtro de fecha
            date_filter = request.args.get('date')
            if date_filter:
                try:
                    date_filter = datetime.strptime(date_filter, '%Y-%m-%d').date()
                except ValueError:
                    return response_error("Formato de fecha inválido. Use YYYY-MM-DD")

            # Obtener estadísticas
            res = SimpleAppointmentComponent.get_daily_statistics(date_filter)
            if res:
                # Agregar información adicional
                response_data = {
                    'statistics': res,
                    'date_filter': date_filter.isoformat() if date_filter else 'today',
                    'generated_at': datetime.now().isoformat()
                }
                return response_success(response_data)
            else:
                return response_not_found("No se encontraron estadísticas")

        except Exception as err:
            HandleLogs.write_error(f"Error obteniendo estadísticas: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_by_therapist(Resource):
    @staticmethod
    def get(therapist_name):
        """Obtener citas por terapeuta con validaciones"""
        try:
            HandleLogs.write_log(f"👨‍⚕️ Citas por terapeuta: {therapist_name}")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Validar nombre del terapeuta
            if not therapist_name or len(therapist_name.strip()) < 2:
                return response_error("Nombre del terapeuta debe tener al menos 2 caracteres")

            # Parámetro opcional para filtro de fecha
            date_filter = request.args.get('date')
            if date_filter:
                try:
                    datetime.strptime(date_filter, '%Y-%m-%d')
                except ValueError:
                    return response_error("Formato de fecha inválido. Use YYYY-MM-DD")

            # Obtener citas
            res = SimpleAppointmentComponent.get_appointments_by_therapist(therapist_name, date_filter)
            if res is not None:
                return response_success({
                    'therapist_name': therapist_name,
                    'date_filter': date_filter,
                    'appointments': res,
                    'total_appointments': len(res)
                })
            else:
                return response_not_found(f"No se encontraron citas para el terapeuta: {therapist_name}")

        except Exception as err:
            HandleLogs.write_error(f"Error obteniendo citas por terapeuta: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_patients(Resource):
    @staticmethod
    def get():
        """Obtener lista de pacientes para dropdown"""
        try:
            HandleLogs.write_log("📋 Obteniendo lista de pacientes")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener pacientes del sistema complejo (si existe) o de citas simplificadas
            try:
                # Intentar obtener de la tabla de pacientes completa primero
                query = """
                    SELECT DISTINCT 
                        p.per_id as patient_id,
                        CONCAT(p.per_names, ' ', p.per_surnames) as patient_name,
                        p.per_phone as patient_phone,
                        p.per_mail as patient_email,
                        pat.pat_code as patient_code
                    FROM ceragen.admin_patient pat
                    INNER JOIN ceragen.admin_person p ON pat.pat_person_id = p.per_id
                    WHERE pat.pat_state = true 
                    AND p.per_state = true
                    ORDER BY p.per_names, p.per_surnames
                """

                response = DataBaseHandle.getRecords(query, 0)

                if response['result'] and response['data']:
                    patients = response['data']
                else:
                    # Si no hay pacientes en el sistema complejo, obtener de citas simplificadas
                    query_simple = """
                        SELECT DISTINCT 
                            patient_id,
                            patient_name,
                            patient_phone,
                            patient_email
                        FROM ceragen.clinic_session_control1
                        WHERE ses_state = true 
                        AND date_deleted IS NULL
                        AND patient_name IS NOT NULL
                        ORDER BY patient_name
                    """

                    response = DataBaseHandle.getRecords(query_simple, 0)
                    if response['result'] and response['data']:
                        patients = response['data']
                    else:
                        patients = []

                return response_success({
                    'patients': patients,
                    'total': len(patients)
                })

            except Exception as err:
                HandleLogs.write_error(f"Error obteniendo pacientes: {str(err)}")
                return response_error(f"Error interno: {str(err)}")

        except Exception as err:
            HandleLogs.write_error(f"Error en endpoint de pacientes: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_therapies(Resource):
    @staticmethod
    def get():
        """Obtener lista de terapias para dropdown"""
        try:
            HandleLogs.write_log("📋 Obteniendo lista de terapias")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            therapies = []

            # Intentar obtener de la tabla de tipos de terapia completa primero
            try:
                query = """
                    SELECT 
                        tht_id as therapy_id,
                        tht_name as therapy_name,
                        tht_description as therapy_description
                    FROM ceragen.admin_therapy_type
                    WHERE tht_state = true
                    ORDER BY tht_name
                """

                response = DataBaseHandle.getRecords(query, 0)

                if response['result'] and response['data']:
                    therapies = response['data']
                else:
                    # Si no hay tipos de terapia, obtener de citas simplificadas
                    query_simple = """
                        SELECT DISTINCT 
                            therapy_name,
                            therapy_type
                        FROM ceragen.clinic_session_control1
                        WHERE ses_state = true 
                        AND date_deleted IS NULL
                        AND therapy_name IS NOT NULL
                        ORDER BY therapy_name
                    """

                    response = DataBaseHandle.getRecords(query_simple, 0)
                    if response['result'] and response['data']:
                        # Convertir a formato estándar
                        therapies = [
                            {
                                'therapy_id': i + 1,
                                'therapy_name': item['therapy_name'],
                                'therapy_description': item['therapy_type']
                            }
                            for i, item in enumerate(response['data'])
                        ]
                    else:
                        # Datos por defecto si no hay nada
                        therapies = [
                            {'therapy_id': 1, 'therapy_name': 'Fisioterapia General',
                             'therapy_description': 'Rehabilitación física'},
                            {'therapy_id': 2, 'therapy_name': 'Masoterapia',
                             'therapy_description': 'Terapia de masajes'},
                            {'therapy_id': 3, 'therapy_name': 'Acupuntura',
                             'therapy_description': 'Medicina alternativa'},
                            {'therapy_id': 4, 'therapy_name': 'Quiropraxia',
                             'therapy_description': 'Terapia quiroprática'},
                            {'therapy_id': 5, 'therapy_name': 'Electroterapia',
                             'therapy_description': 'Estimulación eléctrica'},
                        ]

                return response_success({
                    'therapies': therapies,
                    'total': len(therapies)
                })

            except Exception as err:
                HandleLogs.write_error(f"Error obteniendo terapias: {str(err)}")
                return response_error(f"Error interno: {str(err)}")

        except Exception as err:
            HandleLogs.write_error(f"Error en endpoint de terapias: {str(err)}")
            return response_error(f"Error interno: {str(err)}")


class SimpleAppointmentServiceV2_therapists(Resource):
    @staticmethod
    def get():
        """Obtener lista de terapeutas para dropdown"""
        try:
            HandleLogs.write_log("📋 Obteniendo lista de terapeutas")

            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            therapists = []

            # Intentar obtener del sistema de personal médico completo primero
            try:
                query = """
                    SELECT 
                        ms.med_id as therapist_id,
                        CONCAT(p.per_names, ' ', p.per_surnames) as therapist_name,
                        ms.med_specialty as therapist_specialty,
                        mpt.mpt_name as therapist_type,
                        ms.med_registration_number
                    FROM ceragen.admin_medical_staff ms
                    INNER JOIN ceragen.admin_person p ON ms.med_person_id = p.per_id
                    INNER JOIN ceragen.admin_medic_person_type mpt ON ms.med_type_id = mpt.mpt_id
                    WHERE ms.med_state = true 
                    AND p.per_state = true
                    ORDER BY p.per_names, p.per_surnames
                """

                response = DataBaseHandle.getRecords(query, 0)

                if response['result'] and response['data']:
                    therapists = response['data']
                else:
                    # Si no hay personal médico, obtener de citas simplificadas
                    query_simple = """
                        SELECT DISTINCT 
                            therapist_name,
                            therapist_specialty
                        FROM ceragen.clinic_session_control1
                        WHERE ses_state = true 
                        AND date_deleted IS NULL
                        AND therapist_name IS NOT NULL
                        ORDER BY therapist_name
                    """

                    response = DataBaseHandle.getRecords(query_simple, 0)
                    if response['result'] and response['data']:
                        # Convertir a formato estándar
                        therapists = [
                            {
                                'therapist_id': i + 1,
                                'therapist_name': item['therapist_name'],
                                'therapist_specialty': item['therapist_specialty'],
                                'therapist_type': 'Terapeuta',
                                'med_registration_number': None
                            }
                            for i, item in enumerate(response['data'])
                        ]
                    else:
                        # Datos por defecto si no hay nada
                        therapists = [
                            {'therapist_id': 1, 'therapist_name': 'Dr. María González',
                             'therapist_specialty': 'Fisioterapeuta', 'therapist_type': 'Doctor'},
                            {'therapist_id': 2, 'therapist_name': 'Lic. Pedro Silva',
                             'therapist_specialty': 'Masajista', 'therapist_type': 'Licenciado'},
                            {'therapist_id': 3, 'therapist_name': 'Dr. Luis Castro',
                             'therapist_specialty': 'Acupunturista', 'therapist_type': 'Doctor'},
                            {'therapist_id': 4, 'therapist_name': 'Lic. Ana Torres',
                             'therapist_specialty': 'Quiropráctico', 'therapist_type': 'Licenciado'},
                            {'therapist_id': 5, 'therapist_name': 'Dr. Carlos Mendoza',
                             'therapist_specialty': 'Fisioterapeuta', 'therapist_type': 'Doctor'},
                        ]

                return response_success({
                    'therapists': therapists,
                    'total': len(therapists)
                })

            except Exception as err:
                HandleLogs.write_error(f"Error obteniendo terapeutas: {str(err)}")
                return response_error(f"Error interno: {str(err)}")

        except Exception as err:
            HandleLogs.write_error(f"Error en endpoint de terapeutas: {str(err)}")
            return response_error(f"Error interno: {str(err)}")

class SimpleAppointmentServiceV2_register_session(Resource):
    @staticmethod
    def post(appointment_id):
        print("[DEBUG] LLEGÓ LA PETICIÓN AL ENDPOINT DE REGISTRO DE SESIÓN (POST)")
        """
        Registrar una sesión ejecutada para una cita (marcar como ejecutada).
        """
        try:
            print(f"[DEBUG] Iniciando registro de sesión para cita ID: {appointment_id}")
            HandleLogs.write_log(f"📝 Registrar sesión para cita ID: {appointment_id}")

            # Validar token
            token = request.headers.get('tokenapp')
            print(f"[DEBUG] Token recibido: {token}")
            if not token:
                print("[DEBUG] Token de autenticación requerido")
                return response_error("Token de autenticación requerido")

            token_valido = TokenComponent.Token_Validate(token)
            print(f"[DEBUG] Token válido: {token_valido}")
            if not token_valido:
                print("[DEBUG] Token inválido o expirado")
                return response_unauthorize()

            # Validar ID
            try:
                appointment_id = int(appointment_id)
                if appointment_id <= 0:
                    print("[DEBUG] ID de cita inválido")
                    return response_error("ID de cita inválido")
            except (ValueError, TypeError):
                print("[DEBUG] ID de cita debe ser un número válido")
                return response_error("ID de cita debe ser un número válido")

            # Verificar que la cita existe y se puede ejecutar
            appointment = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            print(f"[DEBUG] Datos de la cita obtenidos: {appointment}")
            if not appointment:
                print("[DEBUG] Cita no encontrada")
                return response_not_found("Cita no encontrada")

            if appointment.get('status') != 'scheduled':
                print(f"[DEBUG] Estado de la cita no permite registrar sesión: {appointment.get('status')}")
                return response_error(
                    f"No se puede registrar sesión para una cita con estado: {appointment.get('status')}")

            if appointment.get('ses_consumed'):
                print("[DEBUG] La sesión ya fue registrada como ejecutada")
                return response_error("La sesión ya fue registrada como ejecutada")

            # Obtener datos opcionales del request
            try:
                data = request.get_json(force=True, silent=True)
                if not data:
                    data = {}
            except Exception as e:
                print(f"[DEBUG] No se pudo decodificar JSON, usando dict vacío. Error: {e}")
                data = {}
            print(f"[DEBUG] Datos recibidos en el body: {data}")
            execution_notes = data.get('execution_notes', 'Sesión registrada desde frontend')

            # Obtener usuario del token
            user_process = TokenComponent.User(token)
            print(f"[DEBUG] Usuario que procesa: {user_process}")

            # Registrar sesión (marcar como ejecutada)
            result = SimpleAppointmentComponent.execute_session(
                appointment_id,
                user_process,
                execution_notes
            )
            print(f"[DEBUG] Resultado de execute_session: {result}")

            if result['result']:
                HandleLogs.write_log(f"✅ Sesión registrada exitosamente")
                print("[DEBUG] Sesión registrada exitosamente")
                return response_success({
                    'message': 'Sesión registrada exitosamente',
                    'appointment_id': appointment_id,
                    'patient_name': appointment.get('patient_name'),
                    'execution_notes': execution_notes
                })
            else:
                print(f"[DEBUG] Error al registrar sesión: {result['message']}")
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(f"Error registrando sesión: {str(err)}")
            print(f"[DEBUG] Excepción en registro de sesión: {err}")
            return response_error(f"Error interno: {str(err)}")

    @staticmethod
    def patch(appointment_id):
        print("[DEBUG] LLEGÓ LA PETICIÓN AL ENDPOINT DE REGISTRO DE SESIÓN (PATCH)")
        # Simplemente reutiliza la lógica de post
        return SimpleAppointmentServiceV2_register_session.post(appointment_id)