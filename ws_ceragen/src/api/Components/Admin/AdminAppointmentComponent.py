from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime, date, timedelta
from ....utils.general.response import internal_response
import json
from decimal import Decimal


class AppointmentComponent:

    @staticmethod
    def list_all_appointments(start_date=None, end_date=None):
        """Obtener todas las citas en un rango de fechas"""
        try:
            base_query = """
                SELECT 
                    sc.sec_id,
                    sc.sec_inv_id,
                    sc.sec_pro_id,
                    sc.sec_ses_number,
                    sc.sec_ses_agend_date,
                    sc.sec_ses_exec_date,
                    sc.sec_typ_id,
                    sc.sec_med_staff_id,
                    sc.ses_consumed,
                    sc.ses_state,
                    -- Información del paciente (a través de invoice)
                    COALESCE(
                        p_patient.per_names || ' ' || p_patient.per_surnames,
                        p_client.per_names || ' ' || p_client.per_surnames
                    ) as patient_name,
                    COALESCE(pat.pat_code, 'N/A') as patient_code,
                    COALESCE(p_patient.per_phone, p_client.per_phone) as patient_phone,
                    COALESCE(p_patient.per_mail, p_client.per_mail) as patient_email,
                    -- Información del producto/terapia
                    prod.pro_name as therapy_name,
                    prod.pro_price,
                    prod.pro_total_sessions,
                    prod.pro_duration_days,
                    -- Tipo de terapia
                    tt.tht_name as therapy_type,
                    tt.tht_description as therapy_type_desc,
                    -- Personal médico
                    mp.per_names || ' ' || mp.per_surnames as staff_name,
                    ms.med_specialty,
                    ms.med_registration_number,
                    mpt.mpt_name as staff_type,
                    -- Información de factura
                    inv.inv_number,
                    inv.inv_date,
                    inv.inv_grand_total,
                    inv.inv_state as invoice_state,
                    -- Fechas formateadas
                    TO_CHAR(sc.sec_ses_agend_date, 'DD/MM/YYYY HH24:MI') as agend_date_formatted,
                    TO_CHAR(sc.sec_ses_exec_date, 'DD/MM/YYYY HH24:MI') as exec_date_formatted
                FROM ceragen.clinic_session_control sc
                INNER JOIN ceragen.admin_invoice inv ON sc.sec_inv_id = inv.inv_id
                INNER JOIN ceragen.admin_product prod ON sc.sec_pro_id = prod.pro_id
                INNER JOIN ceragen.admin_therapy_type tt ON sc.sec_typ_id = tt.tht_id
                INNER JOIN ceragen.admin_medical_staff ms ON sc.sec_med_staff_id = ms.med_id
                INNER JOIN ceragen.admin_person mp ON ms.med_person_id = mp.per_id
                INNER JOIN ceragen.admin_medic_person_type mpt ON ms.med_type_id = mpt.mpt_id
                -- Cliente (siempre existe)
                INNER JOIN ceragen.admin_client cli ON inv.inv_client_id = cli.cli_id
                INNER JOIN ceragen.admin_person p_client ON cli.cli_person_id = p_client.per_id
                -- Paciente (opcional)
                LEFT JOIN ceragen.admin_patient pat ON inv.inv_patient_id = pat.pat_id
                LEFT JOIN ceragen.admin_person p_patient ON pat.pat_person_id = p_patient.per_id
                WHERE sc.ses_state = true
                AND inv.inv_state = true
                AND prod.pro_state = true
                AND ms.med_state = true
            """

            if start_date and end_date:
                query = base_query + " AND sc.sec_ses_agend_date BETWEEN %s AND %s"
                params = (start_date, end_date)
            else:
                query = base_query
                params = None

            query += " ORDER BY sc.sec_ses_agend_date ASC"

            res = DataBaseHandle.getRecords(query, 0, params)
            return json.loads(json.dumps(res, default=AppointmentComponent.json_serial))
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Obtener cita específica por ID"""
        try:
            query = """
                SELECT 
                    sc.sec_id,
                    sc.sec_inv_id,
                    sc.sec_pro_id,
                    sc.sec_ses_number,
                    sc.sec_ses_agend_date,
                    sc.sec_ses_exec_date,
                    sc.sec_typ_id,
                    sc.sec_med_staff_id,
                    sc.ses_consumed,
                    sc.ses_state,
                    -- Info del paciente
                    COALESCE(
                        p_patient.per_names || ' ' || p_patient.per_surnames,
                        p_client.per_names || ' ' || p_client.per_surnames
                    ) as patient_name,
                    COALESCE(p_patient.per_phone, p_client.per_phone) as patient_phone,
                    -- Info del producto
                    prod.pro_name as therapy_name,
                    prod.pro_total_sessions,
                    -- Tipo de terapia
                    tt.tht_name as therapy_type,
                    -- Personal médico
                    mp.per_names || ' ' || mp.per_surnames as staff_name,
                    ms.med_specialty,
                    mpt.mpt_name as staff_type,
                    -- Info de factura
                    inv.inv_number,
                    inv.inv_grand_total
                FROM ceragen.clinic_session_control sc
                INNER JOIN ceragen.admin_invoice inv ON sc.sec_inv_id = inv.inv_id
                INNER JOIN ceragen.admin_product prod ON sc.sec_pro_id = prod.pro_id
                INNER JOIN ceragen.admin_therapy_type tt ON sc.sec_typ_id = tt.tht_id
                INNER JOIN ceragen.admin_medical_staff ms ON sc.sec_med_staff_id = ms.med_id
                INNER JOIN ceragen.admin_person mp ON ms.med_person_id = mp.per_id
                INNER JOIN ceragen.admin_medic_person_type mpt ON ms.med_type_id = mpt.mpt_id
                INNER JOIN ceragen.admin_client cli ON inv.inv_client_id = cli.cli_id
                INNER JOIN ceragen.admin_person p_client ON cli.cli_person_id = p_client.per_id
                LEFT JOIN ceragen.admin_patient pat ON inv.inv_patient_id = pat.pat_id
                LEFT JOIN ceragen.admin_person p_patient ON pat.pat_person_id = p_patient.per_id
                WHERE sc.sec_id = %s AND sc.ses_state = true
            """
            res = DataBaseHandle.getRecords(query, 1, (appointment_id,))
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def check_availability(date_time, therapy_type_id, staff_id=None):
        """Verificar disponibilidad para una fecha/hora específica"""
        try:
            # Verificar si es día festivo
            if AppointmentComponent.is_holiday(date_time.date()):
                return {
                    'available': False,
                    'reason': 'Es día festivo',
                    'available_slots': []
                }

            # Verificar si es día laboral
            if not AppointmentComponent.is_work_day(date_time.date()):
                return {
                    'available': False,
                    'reason': 'No es día laboral',
                    'available_slots': []
                }

            # Verificar horario de trabajo
            if not AppointmentComponent.is_work_hour(date_time.time()):
                return {
                    'available': False,
                    'reason': 'Fuera del horario de atención',
                    'available_slots': []
                }

            # Verificar camas disponibles
            beds_available = AppointmentComponent.get_available_beds(date_time, therapy_type_id)

            if beds_available <= 0:
                return {
                    'available': False,
                    'reason': 'No hay camas disponibles',
                    'available_slots': []
                }

            # Verificar disponibilidad del staff específico
            if staff_id:
                staff_busy = AppointmentComponent.is_staff_busy(staff_id, date_time)
                if staff_busy:
                    return {
                        'available': False,
                        'reason': 'El terapeuta no está disponible en esa hora',
                        'available_slots': []
                    }

            return {
                'available': True,
                'reason': 'Disponible',
                'beds_available': beds_available,
                'available_slots': AppointmentComponent.get_available_time_slots(date_time.date(), therapy_type_id)
            }

        except Exception as err:
            HandleLogs.write_error(err)
            return {
                'available': False,
                'reason': f'Error del sistema: {str(err)}',
                'available_slots': []
            }

    @staticmethod
    def schedule_appointment(data):
        """Agendar nueva cita"""
        try:
            v_message = None
            v_result = False
            v_data = None

            # Verificar disponibilidad antes de agendar
            agend_datetime = datetime.fromisoformat(data['sec_ses_agend_date'].replace('Z', ''))
            availability = AppointmentComponent.check_availability(
                agend_datetime,
                data['sec_typ_id'],
                data.get('sec_med_staff_id')
            )

            if not availability['available']:
                return internal_response(False, f"No disponible: {availability['reason']}", None)

            # Insertar nueva cita
            sql = """
                INSERT INTO ceragen.clinic_session_control
                (sec_inv_id, sec_pro_id, sec_ses_number, sec_ses_agend_date, 
                 sec_typ_id, sec_med_staff_id, ses_consumed, ses_state, 
                 user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING sec_id
            """

            record = (
                data['sec_inv_id'],
                data['sec_pro_id'],
                data['sec_ses_number'],
                agend_datetime,
                data['sec_typ_id'],
                data['sec_med_staff_id'],
                False,  # ses_consumed
                True,  # ses_state
                data['user_process'],
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
        """Reagendar cita existente"""
        try:
            # Verificar que la cita existe
            appointment = AppointmentComponent.get_appointment_by_id(appointment_id)
            if not appointment:
                return internal_response(False, "Cita no encontrada", None)

            # Verificar disponibilidad en nueva fecha
            new_datetime = datetime.fromisoformat(new_date_time.replace('Z', ''))
            availability = AppointmentComponent.check_availability(
                new_datetime,
                appointment['sec_typ_id'],
                appointment['sec_med_staff_id']
            )

            if not availability['available']:
                return internal_response(False, f"Nueva fecha no disponible: {availability['reason']}", None)

            # Actualizar la cita
            sql = """
                UPDATE ceragen.clinic_session_control 
                SET sec_ses_agend_date = %s, 
                    user_modified = %s, 
                    date_modified = %s
                WHERE sec_id = %s AND ses_state = true
            """

            record = (new_datetime, user_process, datetime.now(), appointment_id)
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                return internal_response(True, "Cita reagendada exitosamente", result)
            else:
                return internal_response(False, "No se pudo reagendar la cita", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al reagendar: {str(err)}", None)

    @staticmethod
    def cancel_appointment(appointment_id, user_process):
        """Cancelar cita (eliminación lógica)"""
        try:
            sql = """
                UPDATE ceragen.clinic_session_control 
                SET ses_state = false, 
                    user_deleted = %s, 
                    date_deleted = %s
                WHERE sec_id = %s
            """

            record = (user_process, datetime.now(), appointment_id)
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                return internal_response(True, "Cita cancelada exitosamente", result)
            else:
                return internal_response(False, "No se encontró la cita o ya fue cancelada", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al cancelar: {str(err)}", None)

    @staticmethod
    def mark_session_as_executed(appointment_id, user_process):
        """Marcar sesión como ejecutada"""
        try:
            sql = """
                UPDATE ceragen.clinic_session_control 
                SET sec_ses_exec_date = %s,
                    ses_consumed = true,
                    user_modified = %s, 
                    date_modified = %s
                WHERE sec_id = %s AND ses_state = true
            """

            record = (datetime.now(), user_process, datetime.now(), appointment_id)
            result = DataBaseHandle.ExecuteNonQuery(sql, record)

            if result > 0:
                return internal_response(True, "Sesión marcada como ejecutada", result)
            else:
                return internal_response(False, "No se encontró la cita", None)

        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al marcar como ejecutada: {str(err)}", None)

    # ========== HELPER METHODS ==========

    @staticmethod
    def get_system_parameter(code):
        """Obtener parámetro del sistema"""
        try:
            query = """
                SELECT pli_string_value_return, pli_numeric_value_return, pli_is_numeric_return_value
                FROM ceragen.admin_parameter_list 
                WHERE pli_code_parameter = %s AND pli_state = true
            """
            result = DataBaseHandle.getRecords(query, 1, (code,))
            if result:
                if result['pli_is_numeric_return_value']:
                    return result['pli_numeric_value_return']
                else:
                    return result['pli_string_value_return']
            return None
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def is_holiday(check_date):
        """Verificar si una fecha es feriado"""
        try:
            holidays_str = AppointmentComponent.get_system_parameter('HOLIDAYS_2025')
            if holidays_str:
                holidays = holidays_str.split(',')
                return check_date.strftime('%Y-%m-%d') in holidays
            return False
        except Exception as err:
            HandleLogs.write_error(err)
            return False

    @staticmethod
    def is_work_day(check_date):
        """Verificar si es día laboral (lunes=1, domingo=7)"""
        try:
            work_days_str = AppointmentComponent.get_system_parameter('WORK_DAYS')
            if work_days_str:
                work_days = [int(d) for d in work_days_str.split(',')]
                # Python: lunes=0, domingo=6 -> convertir a lunes=1, domingo=7
                python_weekday = check_date.weekday() + 1
                return python_weekday in work_days
            return False
        except Exception as err:
            HandleLogs.write_error(err)
            return False

    @staticmethod
    def is_work_hour(check_time):
        """Verificar si está en horario de trabajo"""
        try:
            start_hour = AppointmentComponent.get_system_parameter('WORK_START_HOUR')
            end_hour = AppointmentComponent.get_system_parameter('WORK_END_HOUR')
            lunch_start = AppointmentComponent.get_system_parameter('LUNCH_START_HOUR')
            lunch_end = AppointmentComponent.get_system_parameter('LUNCH_END_HOUR')

            if not all([start_hour, end_hour]):
                return False

            # Convertir strings a time objects
            start_time = datetime.strptime(start_hour, '%H:%M').time()
            end_time = datetime.strptime(end_hour, '%H:%M').time()

            # Verificar si está en horario laboral
            in_work_hours = start_time <= check_time <= end_time

            # Verificar si no está en hora de almuerzo
            if lunch_start and lunch_end:
                lunch_start_time = datetime.strptime(lunch_start, '%H:%M').time()
                lunch_end_time = datetime.strptime(lunch_end, '%H:%M').time()
                in_lunch = lunch_start_time <= check_time <= lunch_end_time
                return in_work_hours and not in_lunch

            return in_work_hours
        except Exception as err:
            HandleLogs.write_error(err)
            return False

    @staticmethod
    def get_available_beds(date_time, therapy_type_id):
        """Obtener camas disponibles para un tipo de terapia"""
        try:
            # Obtener total de camas por tipo de terapia
            if therapy_type_id == 1:  # Terapia física (ajustar según tus IDs)
                total_beds = AppointmentComponent.get_system_parameter('BEDS_PHYSICAL_THERAPY')
            elif therapy_type_id == 2:  # Terapia alternativa
                total_beds = AppointmentComponent.get_system_parameter('BEDS_ALTERNATIVE_THERAPY')
            else:
                total_beds = AppointmentComponent.get_system_parameter('TOTAL_BEDS_AVAILABLE')

            if not total_beds:
                total_beds = 10  # Default

            # Contar citas ya agendadas para esa hora y tipo de terapia
            session_duration = AppointmentComponent.get_system_parameter('SESSION_DURATION_MINUTES') or 60
            end_time = date_time + timedelta(minutes=session_duration)

            query = """
                SELECT COUNT(*) as occupied_beds
                FROM ceragen.clinic_session_control sc
                WHERE sc.sec_typ_id = %s 
                AND sc.ses_state = true
                AND sc.sec_ses_agend_date < %s
                AND (sc.sec_ses_agend_date + INTERVAL '%s minutes') > %s
            """

            result = DataBaseHandle.getRecords(query, 1, (therapy_type_id, end_time, session_duration, date_time))

            if result:
                occupied_beds = result.get('occupied_beds', 0)
                return max(0, total_beds - occupied_beds)

            return total_beds

        except Exception as err:
            HandleLogs.write_error(err)
            return 0

    @staticmethod
    def is_staff_busy(staff_id, date_time):
        """Verificar si el staff está ocupado en esa hora"""
        try:
            session_duration = AppointmentComponent.get_system_parameter('SESSION_DURATION_MINUTES') or 60
            end_time = date_time + timedelta(minutes=session_duration)

            query = """
                SELECT COUNT(*) as busy_count
                FROM ceragen.clinic_session_control sc
                WHERE sc.sec_med_staff_id = %s 
                AND sc.ses_state = true
                AND sc.sec_ses_agend_date < %s
                AND (sc.sec_ses_agend_date + INTERVAL '%s minutes') > %s
            """

            result = DataBaseHandle.getRecords(query, 1, (staff_id, end_time, session_duration, date_time))

            if result:
                return result.get('busy_count', 0) > 0

            return False

        except Exception as err:
            HandleLogs.write_error(err)
            return True  # En caso de error, asumir que está ocupado

    @staticmethod
    def get_available_time_slots(check_date, therapy_type_id):
        """Obtener horarios disponibles para un día específico"""
        try:
            available_slots = []

            # Obtener parámetros de horario
            start_hour = AppointmentComponent.get_system_parameter('WORK_START_HOUR')
            end_hour = AppointmentComponent.get_system_parameter('WORK_END_HOUR')
            session_duration = AppointmentComponent.get_system_parameter('SESSION_DURATION_MINUTES') or 60

            if not start_hour or not end_hour:
                return []

            # Generar slots de tiempo
            start_time = datetime.strptime(start_hour, '%H:%M').time()
            end_time = datetime.strptime(end_hour, '%H:%M').time()

            current_datetime = datetime.combine(check_date, start_time)
            end_datetime = datetime.combine(check_date, end_time)

            while current_datetime < end_datetime:
                # Verificar disponibilidad para este slot
                availability = AppointmentComponent.check_availability(
                    current_datetime,
                    therapy_type_id
                )

                if availability['available']:
                    available_slots.append({
                        'time': current_datetime.strftime('%H:%M'),
                        'datetime': current_datetime.isoformat(),
                        'beds_available': availability.get('beds_available', 0)
                    })

                # Avanzar al siguiente slot
                current_datetime += timedelta(minutes=session_duration)

            return available_slots

        except Exception as err:
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def get_therapy_types():
        """Obtener tipos de terapia disponibles"""
        try:
            query = """
                SELECT tht_id, tht_name, tht_description
                FROM ceragen.admin_therapy_type
                WHERE tht_state = true
                ORDER BY tht_name
            """
            res = DataBaseHandle.getRecords(query, 0)
            return json.loads(json.dumps(res, default=AppointmentComponent.json_serial))
        except Exception as err:
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def get_medical_staff(therapy_type_id=None):
        """Obtener personal médico disponible"""
        try:
            base_query = """
                SELECT 
                    ms.med_id,
                    p.per_names || ' ' || p.per_surnames as staff_name,
                    ms.med_specialty,
                    ms.med_registration_number,
                    mpt.mpt_name as staff_type
                FROM ceragen.admin_medical_staff ms
                INNER JOIN ceragen.admin_person p ON ms.med_person_id = p.per_id
                INNER JOIN ceragen.admin_medic_person_type mpt ON ms.med_type_id = mpt.mpt_id
                WHERE ms.med_state = true
                AND p.per_state = true
            """

            if therapy_type_id:
                # Filtrar por tipo de terapia si es necesario
                query = base_query + " ORDER BY p.per_names"
            else:
                query = base_query + " ORDER BY p.per_names"

            res = DataBaseHandle.getRecords(query, 0)
            return json.loads(json.dumps(res, default=AppointmentComponent.json_serial))
        except Exception as err:
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def get_products_by_therapy_type(therapy_type_id):
        """Obtener productos/paquetes por tipo de terapia"""
        try:
            query = """
                SELECT 
                    pro_id,
                    pro_code,
                    pro_name,
                    pro_description,
                    pro_price,
                    pro_total_sessions,
                    pro_duration_days
                FROM ceragen.admin_product
                WHERE pro_therapy_type_id = %s
                AND pro_state = true
                ORDER BY pro_name
            """
            res = DataBaseHandle.getRecords(query, 0, (therapy_type_id,))
            return json.loads(json.dumps(res, default=AppointmentComponent.json_serial))
        except Exception as err:
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def json_serial(obj):
        """JSON serializer para objetos no serializables por default"""
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")