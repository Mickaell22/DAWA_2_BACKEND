from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime, date, timedelta
from ....utils.general.response import internal_response
import json
from decimal import Decimal

class SimpleAppointmentComponent:
    """
    Componente simplificado para manejo de citas usando clinic_session_control1
    """

    @staticmethod
    def list_all_appointments(start_date=None, end_date=None):
        """Obtener todas las citas en un rango de fechas (versión simplificada)"""
        try:
            print(f"[DEBUG] list_all_appointments called with start_date={start_date}, end_date={end_date}")
            HandleLogs.write_log(f"[DEBUG] list_all_appointments called with start_date={start_date}, end_date={end_date}")

            base_query = """
                SELECT 
                    sec_id,
                    patient_name,
                    patient_phone,
                    patient_email,
                    patient_id,
                    sec_ses_number,
                    sessions_registered,
                    sec_ses_agend_date,
                    sec_ses_exec_date,
                    therapy_name,
                    therapy_type,
                    therapist_name,
                    therapist_specialty,
                    ses_consumed,
                    ses_state,
                    status,
                    duration_minutes,
                    notes,
                    price,
                    user_created,
                    date_created,
                    user_modified,
                    date_modified,
                    -- Fechas formateadas
                    TO_CHAR(sec_ses_agend_date, 'DD/MM/YYYY HH24:MI') as agend_date_formatted,
                    TO_CHAR(sec_ses_exec_date, 'DD/MM/YYYY HH24:MI') as exec_date_formatted
                FROM ceragen.clinic_session_control1
                WHERE ses_state = true
                AND date_deleted IS NULL
            """

            if start_date and end_date:
                query = base_query + " AND sec_ses_agend_date BETWEEN %s AND %s"
                params = (start_date, end_date)
            else:
                query = base_query
                params = ()

            query += " ORDER BY sec_ses_agend_date ASC"

            print(f"[DEBUG] Ejecutando query: {query} con params: {params}")
            HandleLogs.write_log(f"[DEBUG] Ejecutando query: {query} con params: {params}")

            response = DataBaseHandle.getRecords(query, 0, params)
            print(f"[DEBUG] Respuesta de getRecords: {response}")
            HandleLogs.write_log(f"[DEBUG] Respuesta de getRecords: {response}")

            # Check if response is successful and extract data
            if response and response.get('result') and response.get('data'):
                print("[DEBUG] Citas encontradas, retornando datos.")
                return json.loads(json.dumps(response['data'], default=SimpleAppointmentComponent.json_serial))
            else:
                print("[DEBUG] No se encontraron citas.")
                return []
        except Exception as err:
            print(f"[ERROR] list_all_appointments: {err}")
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def get_appointment_by_id(appointment_id):
        try:
            print(f"[DEBUG] get_appointment_by_id called with appointment_id={appointment_id}")
            HandleLogs.write_log(f"[DEBUG] get_appointment_by_id called with appointment_id={appointment_id}")

            sql = """
                SELECT 
                    sec_id,
                    patient_name,
                    patient_phone,
                    patient_email,
                    patient_id,
                    sec_ses_number,
                    sessions_registered,
                    sec_ses_agend_date,
                    sec_ses_exec_date,
                    therapy_name,
                    therapy_type,
                    therapist_name,
                    therapist_specialty,
                    ses_consumed,
                    ses_state,
                    status,
                    duration_minutes,
                    notes,
                    price,
                    TO_CHAR(sec_ses_agend_date, 'DD/MM/YYYY HH24:MI') as agend_date_formatted,
                    TO_CHAR(sec_ses_exec_date, 'DD/MM/YYYY HH24:MI') as exec_date_formatted
                FROM ceragen.clinic_session_control1
                WHERE sec_id = %s AND ses_state = true AND date_deleted IS NULL
            """

            # CORRECCIÓN aquí: el 0 es el segundo parámetro, y los parámetros SQL el tercero
            result = DataBaseHandle.getRecords(sql, 0, (appointment_id,))
            print("[DEBUG] Respuesta de getRecords:", result)

            if result['result'] and result['data']:
                print("[DEBUG] Cita encontrada, retornando datos.")
                return result['data'][0]
            else:
                return None
        except Exception as err:
            print(f"[ERROR] get_appointment_by_id: {err}")
            return None

    def schedule_appointment(data):
        """Agendar nueva cita (versión simplificada)"""
        v_result = False
        v_message = ""
        v_data = None

        try:
            print(f"[DEBUG] schedule_appointment called with data: {data}")
            HandleLogs.write_log(f"[DEBUG] schedule_appointment called with data: {data}")

            # Verificar si la fecha existe en los datos
            agend_datetime = None
            if 'sec_ses_agend_date' in data and data['sec_ses_agend_date']:
                agend_datetime = datetime.fromisoformat(data['sec_ses_agend_date'].replace('Z', ''))
                # Validación básica de fecha
                if agend_datetime < datetime.now():
                    print("[DEBUG] La fecha de la cita no puede ser en el pasado.")
                    return internal_response(False, "La fecha de la cita no puede ser en el pasado", None)

            sql = """
                INSERT INTO ceragen.clinic_session_control1 
                (patient_name, patient_phone, patient_email, patient_id,
                 sec_ses_number, sec_ses_agend_date, therapy_name, therapy_type,
                 therapist_name, therapist_specialty, duration_minutes, 
                 notes, price, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING sec_id
            """

            record = (
                data.get('patient_name', ''),
                data.get('patient_phone'),
                data.get('patient_email'),
                data.get('patient_id'),
                data.get('sec_ses_number', 1),
                agend_datetime,  # puede ser None aquí
                data.get('therapy_name'),
                data.get('therapy_type'),
                data.get('therapist_name'),
                data.get('therapist_specialty'),
                data.get('duration_minutes', 60),
                data.get('notes'),
                data.get('price'),
                data.get('user_process', 'system'),
                datetime.now()
            )

            print(f"[DEBUG] Ejecutando insert: {sql} con record: {record}")
            HandleLogs.write_log(f"[DEBUG] Ejecutando insert: {sql} con record: {record}")

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            print(f"[DEBUG] Resultado de ExecuteNonQuery: {v_data}")

            if v_data is not None:
                v_result = True
                v_message = "Cita agendada exitosamente"
                print("[DEBUG] Cita agendada exitosamente.")
            else:
                print("[DEBUG] No se pudo agendar la cita.")

        except Exception as err:
            print(f"[ERROR] schedule_appointment: {err}")
            HandleLogs.write_error(err)
            v_message = f"Error al agendar cita: {str(err)}"
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def reschedule_appointment(appointment_id, new_date_time, user_process):
        """Reagendar cita existente (versión simplificada)"""
        try:
            print(f"[DEBUG] reschedule_appointment called with appointment_id={appointment_id}, new_date_time={new_date_time}, user_process={user_process}")
            HandleLogs.write_log(f"[DEBUG] reschedule_appointment called with appointment_id={appointment_id}, new_date_time={new_date_time}, user_process={user_process}")

            # Verificar que la cita existe
            appointment = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            if not appointment:
                print("[DEBUG] Cita no encontrada para reagendar.")
                return internal_response(False, "Cita no encontrada", None)

            # Convertir nueva fecha
            new_datetime = datetime.fromisoformat(new_date_time.replace('Z', ''))

            # Validación básica
            if new_datetime < datetime.now():
                print("[DEBUG] La nueva fecha no puede ser en el pasado.")
                return internal_response(False, "La nueva fecha no puede ser en el pasado", None)

            # Actualizar la cita
            sql = """
                UPDATE ceragen.clinic_session_control1 
                SET sec_ses_agend_date = %s, 
                    user_modified = %s, 
                    date_modified = %s
                WHERE sec_id = %s AND ses_state = true AND date_deleted IS NULL
            """

            record = (new_datetime, user_process, datetime.now(), appointment_id)
            print(f"[DEBUG] Ejecutando update: {sql} con record: {record}")
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                print("[DEBUG] Cita reagendada exitosamente.")
                return internal_response(True, "Cita reagendada exitosamente", result)
            else:
                print("[DEBUG] No se pudo reagendar la cita.")
                return internal_response(False, "No se pudo reagendar la cita", None)

        except Exception as err:
            print(f"[ERROR] reschedule_appointment: {err}")
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al reagendar cita: {str(err)}", None)

    @staticmethod
    def cancel_appointment(appointment_id, user_process):
        """Cancelar cita (eliminación lógica)"""
        try:
            print(f"[DEBUG] cancel_appointment called with appointment_id={appointment_id}, user_process={user_process}")
            HandleLogs.write_log(f"[DEBUG] cancel_appointment called with appointment_id={appointment_id}, user_process={user_process}")

            sql = """
                UPDATE ceragen.clinic_session_control1 
                SET ses_state = false,
                    status = 'cancelled',
                    user_deleted = %s,
                    date_deleted = %s
                WHERE sec_id = %s AND ses_state = true
            """

            record = (user_process, datetime.now(), appointment_id)
            print(f"[DEBUG] Ejecutando update: {sql} con record: {record}")
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                print("[DEBUG] Cita cancelada exitosamente.")
                return internal_response(True, "Cita cancelada exitosamente", result)
            else:
                print("[DEBUG] No se pudo cancelar la cita.")
                return internal_response(False, "No se pudo cancelar la cita", None)

        except Exception as err:
            print(f"[ERROR] cancel_appointment: {err}")
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al cancelar cita: {str(err)}", None)

    @staticmethod
    def execute_session(appointment_id, user_process, execution_notes=None):
        """Registrar UNA sesión ejecutada (incremental)"""
        try:
            print(
                f"[DEBUG] execute_session called with appointment_id={appointment_id}, user_process={user_process}, execution_notes={execution_notes}")
            HandleLogs.write_log(
                f"[DEBUG] execute_session called with appointment_id={appointment_id}, user_process={user_process}, execution_notes={execution_notes}")

            # Obtener la cita actual
            appointment = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            if not appointment:
                return internal_response(False, "Cita no encontrada", None)

            total_sessions = appointment.get('sec_ses_number', 1)
            registered = appointment.get('sessions_registered', 0)

            if registered >= total_sessions:
                return internal_response(False, "Ya se registraron todas las sesiones", None)

            # Incrementar el contador
            new_registered = registered + 1

            # Si llegó al máximo, marcar como completada y consumida
            if new_registered >= total_sessions:
                sql = """
                    UPDATE ceragen.clinic_session_control1 
                    SET sessions_registered = %s,
                        ses_consumed = true,
                        status = 'completed',
                        sec_ses_exec_date = %s,
                        notes = COALESCE(notes || '\n\nEjecución: ' || %s, %s),
                        user_modified = %s,
                        date_modified = %s
                    WHERE sec_id = %s AND ses_state = true
                """
                record = (
                    new_registered,
                    datetime.now(),
                    execution_notes,
                    execution_notes,
                    user_process,
                    datetime.now(),
                    appointment_id
                )
            else:
                # Solo suma una sesión, no marca como completada
                sql = """
                    UPDATE ceragen.clinic_session_control1 
                    SET sessions_registered = %s,
                        notes = COALESCE(notes || '\n\nEjecución: ' || %s, %s),
                        user_modified = %s,
                        date_modified = %s
                    WHERE sec_id = %s AND ses_state = true
                """
                record = (
                    new_registered,
                    execution_notes,
                    execution_notes,
                    user_process,
                    datetime.now(),
                    appointment_id
                )

            print(f"[DEBUG] Ejecutando update: {sql} con record: {record}")
            result = DataBaseHandle.ExecuteNonQuery(sql, record)
            print("[DEBUG] Valor de result en execute_session:", result)

            # Validar cuántas filas fueron afectadas
            affected = 0
            if isinstance(result, dict):
                affected = result.get('data', 0)  # << CORREGIDO: antes estaba result.get('rowcount')
            elif isinstance(result, int):
                affected = result

            if affected > 0:
                print("[DEBUG] Sesión registrada correctamente.")
                return internal_response(True, "Sesión registrada correctamente",
                                         {"sessions_registered": new_registered})
            else:
                print("[DEBUG] No se pudo registrar la sesión.")
                return internal_response(False, "No se pudo registrar la sesión", None)

        except Exception as err:
            print(f"[ERROR] execute_session: {err}")
            try:
                HandleLogs.write_error(err)  # Asegúrate de que use encoding='utf-8' en esa función
            except Exception as log_err:
                print(f"[ERROR] Error al escribir log: {log_err}")
            return internal_response(False, f"Error al ejecutar sesión: {str(err)}", None)

    @staticmethod
    def update_appointment(appointment_id, data, user_process):
        """Actualizar información de cita"""
        try:
            print(f"[DEBUG] update_appointment called with appointment_id={appointment_id}, data={data}, user_process={user_process}")
            HandleLogs.write_log(f"[DEBUG] update_appointment called with appointment_id={appointment_id}, data={data}, user_process={user_process}")

            # Construir query dinámicamente según los campos proporcionados
            update_fields = []
            values = []

            field_mapping = {
                'patient_name': 'patient_name',
                'patient_phone': 'patient_phone',
                'patient_email': 'patient_email',
                'patient_id': 'patient_id',
                'sec_ses_number': 'sec_ses_number',
                'sec_ses_agend_date': 'sec_ses_agend_date',
                'therapy_name': 'therapy_name',
                'therapy_type': 'therapy_type',
                'therapist_name': 'therapist_name',
                'therapist_specialty': 'therapist_specialty',
                'duration_minutes': 'duration_minutes',
                'notes': 'notes',
                'price': 'price',
                'status': 'status'
            }

            for field_key, db_field in field_mapping.items():
                if field_key in data and data[field_key] is not None:
                    if field_key == 'sec_ses_agend_date':
                        # Convertir fecha
                        agend_datetime = datetime.fromisoformat(data[field_key].replace('Z', ''))
                        update_fields.append(f"{db_field} = %s")
                        values.append(agend_datetime)
                    else:
                        update_fields.append(f"{db_field} = %s")
                        values.append(data[field_key])

            if not update_fields:
                print("[DEBUG] No hay campos para actualizar.")
                return internal_response(False, "No hay campos para actualizar", None)

            # Agregar campos de auditoría
            update_fields.extend(['user_modified = %s', 'date_modified = %s'])
            values.extend([user_process, datetime.now()])
            values.append(appointment_id)

            sql = f"""
                UPDATE ceragen.clinic_session_control1 
                SET {', '.join(update_fields)}
                WHERE sec_id = %s AND ses_state = true AND date_deleted IS NULL
            """

            print(f"[DEBUG] Ejecutando update: {sql} con values: {tuple(values)}")
            result = DataBaseHandle.ExecuteNonQuery(sql, tuple(values))
            print(f"[DEBUG] Result from ExecuteNonQuery: {result}")

            affected_rows = 0
            if isinstance(result, dict):
                # Extraer el número de filas afectadas según tu estructura real
                affected_rows = result.get('rowcount') or result.get('data') or 0
            elif isinstance(result, int):
                affected_rows = result

            if affected_rows > 0:
                print("[DEBUG] Cita actualizada exitosamente.")
                return internal_response(True, "Cita actualizada exitosamente", affected_rows)
            else:
                print("[DEBUG] No se pudo actualizar la cita.")
                return internal_response(False, "No se pudo actualizar la cita", None)

        except Exception as err:
            print(f"[ERROR] update_appointment: {err}")
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al actualizar cita: {str(err)}", None)

    @staticmethod
    def get_appointments_by_therapist(therapist_name, date_filter=None):
        """Obtener citas por terapeuta"""
        try:
            print(f"[DEBUG] get_appointments_by_therapist called with therapist_name={therapist_name}, date_filter={date_filter}")
            HandleLogs.write_log(f"[DEBUG] get_appointments_by_therapist called with therapist_name={therapist_name}, date_filter={date_filter}")

            base_query = """
                SELECT * FROM ceragen.clinic_session_control1
                WHERE therapist_name = %s 
                AND ses_state = true 
                AND date_deleted IS NULL
            """
            params = [therapist_name]

            if date_filter:
                base_query += " AND DATE(sec_ses_agend_date) = %s"
                params.append(date_filter)

            base_query += " ORDER BY sec_ses_agend_date"

            print(f"[DEBUG] Ejecutando query: {base_query} con params: {tuple(params)}")
            response = DataBaseHandle.getRecords(base_query, 0, tuple(params))
            print(f"[DEBUG] Respuesta de getRecords: {response}")

            if response and response.get('result') and response.get('data'):
                print("[DEBUG] Citas encontradas para terapeuta.")
                return json.loads(json.dumps(response['data'], default=SimpleAppointmentComponent.json_serial))
            else:
                print("[DEBUG] No se encontraron citas para terapeuta.")
                return []
        except Exception as err:
            print(f"[ERROR] get_appointments_by_therapist: {err}")
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def get_daily_statistics(date_filter=None):
        """Obtener estadísticas del día"""
        try:
            print(f"[DEBUG] get_daily_statistics called with date_filter={date_filter}")
            HandleLogs.write_log(f"[DEBUG] get_daily_statistics called with date_filter={date_filter}")

            if not date_filter:
                date_filter = datetime.now().date()

            query = """
                SELECT 
                    COUNT(*) as total_appointments,
                    COUNT(CASE WHEN status = 'scheduled' THEN 1 END) as scheduled,
                    COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                    COUNT(CASE WHEN status = 'cancelled' THEN 1 END) as cancelled,
                    COUNT(CASE WHEN status = 'no_show' THEN 1 END) as no_show,
                    SUM(CASE WHEN ses_consumed THEN price ELSE 0 END) as total_revenue
                FROM ceragen.clinic_session_control1
                WHERE DATE(sec_ses_agend_date) = %s
                AND ses_state = true
                AND date_deleted IS NULL
            """

            print(f"[DEBUG] Ejecutando query: {query} con date_filter: {date_filter}")
            response = DataBaseHandle.getRecords(query, 0, (date_filter,))
            print(f"[DEBUG] Respuesta de getRecords: {response}")

            if response and response.get('result') and response.get('data'):
                print("[DEBUG] Estadísticas encontradas.")
                return response['data'][0] if response['data'] else None
            print("[DEBUG] No se encontraron estadísticas.")
            return None
        except Exception as err:
            print(f"[ERROR] get_daily_statistics: {err}")
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def json_serial(obj):
        """Serializador JSON para objetos datetime y decimal"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")

