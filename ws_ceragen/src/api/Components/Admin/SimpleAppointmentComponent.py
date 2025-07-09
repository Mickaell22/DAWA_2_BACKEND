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
            base_query = """
                SELECT 
                    sec_id,
                    patient_name,
                    patient_phone,
                    patient_email,
                    patient_id,
                    sec_ses_number,
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
                params = None

            query += " ORDER BY sec_ses_agend_date ASC"

            res = DataBaseHandle.getRecords(query, 0, params)
            return json.loads(json.dumps(res, default=SimpleAppointmentComponent.json_serial))
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Obtener cita específica por ID (versión simplificada)"""
        try:
            query = """
                SELECT 
                    sec_id,
                    patient_name,
                    patient_phone,
                    patient_email,
                    patient_id,
                    sec_ses_number,
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

            res = DataBaseHandle.getRecords(query, 0, (appointment_id,))
            return res[0] if res else None
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def schedule_appointment(data):
        """Agendar nueva cita (versión simplificada)"""
        v_result = False
        v_message = ""
        v_data = None

        try:
            # Convertir fecha string a datetime
            agend_datetime = datetime.fromisoformat(data['sec_ses_agend_date'].replace('Z', ''))

            # Validación básica de fecha
            if agend_datetime < datetime.now():
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
                agend_datetime,
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

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
                v_message = "Cita agendada exitosamente"

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = f"Error al agendar cita: {str(err)}"
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def reschedule_appointment(appointment_id, new_date_time, user_process):
        """Reagendar cita existente (versión simplificada)"""
        try:
            # Verificar que la cita existe
            appointment = SimpleAppointmentComponent.get_appointment_by_id(appointment_id)
            if not appointment:
                return internal_response(False, "Cita no encontrada", None)

            # Convertir nueva fecha
            new_datetime = datetime.fromisoformat(new_date_time.replace('Z', ''))

            # Validación básica
            if new_datetime < datetime.now():
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
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                return internal_response(True, "Cita reagendada exitosamente", result)
            else:
                return internal_response(False, "No se pudo reagendar la cita", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al reagendar cita: {str(err)}", None)

    @staticmethod
    def cancel_appointment(appointment_id, user_process):
        """Cancelar cita (eliminación lógica)"""
        try:
            sql = """
                UPDATE ceragen.clinic_session_control1 
                SET ses_state = false,
                    status = 'cancelled',
                    user_deleted = %s,
                    date_deleted = %s
                WHERE sec_id = %s AND ses_state = true
            """

            record = (user_process, datetime.now(), appointment_id)
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                return internal_response(True, "Cita cancelada exitosamente", result)
            else:
                return internal_response(False, "No se pudo cancelar la cita", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al cancelar cita: {str(err)}", None)

    @staticmethod
    def execute_session(appointment_id, user_process, execution_notes=None):
        """Marcar sesión como ejecutada"""
        try:
            sql = """
                UPDATE ceragen.clinic_session_control1 
                SET ses_consumed = true,
                    status = 'completed',
                    sec_ses_exec_date = %s,
                    notes = COALESCE(notes || '\n\nEjecución: ' || %s, %s),
                    user_modified = %s,
                    date_modified = %s
                WHERE sec_id = %s AND ses_state = true
            """

            record = (
                datetime.now(),
                execution_notes,
                execution_notes,
                user_process,
                datetime.now(),
                appointment_id
            )
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                return internal_response(True, "Sesión marcada como ejecutada", result)
            else:
                return internal_response(False, "No se pudo marcar la sesión como ejecutada", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al ejecutar sesión: {str(err)}", None)

    @staticmethod
    def update_appointment(appointment_id, data, user_process):
        """Actualizar información de cita"""
        try:
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

            result = DataBaseHandle.ExecuteNonQuery(sql, tuple(values))

            if result > 0:
                return internal_response(True, "Cita actualizada exitosamente", result)
            else:
                return internal_response(False, "No se pudo actualizar la cita", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al actualizar cita: {str(err)}", None)

    @staticmethod
    def get_appointments_by_therapist(therapist_name, date_filter=None):
        """Obtener citas por terapeuta"""
        try:
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

            res = DataBaseHandle.getRecords(base_query, 0, tuple(params))
            return json.loads(json.dumps(res, default=SimpleAppointmentComponent.json_serial))
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_daily_statistics(date_filter=None):
        """Obtener estadísticas del día"""
        try:
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

            res = DataBaseHandle.getRecords(query, 0, (date_filter,))
            return res[0] if res else None
        except Exception as err:
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