from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.logs import HandleLogs
from ....utils.general.response import internal_response

class AdminPatientComponent:
    @staticmethod
    def list_all_patients():
        try:
            query = """
            SELECT * FROM ceragen.admin_patient;
            """
            print("Consulta SQL de pacientes:", query)
            result = DataBaseHandle.getRecords(query, 0)
            print("DEBUG: Pacientes obtenidos de la BD:", result)
            return result
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_patient_by_id(pat_id):
        try:
            query = "SELECT * FROM ceragen.admin_patient WHERE pat_id = %s"
            record = (pat_id,)
            result = DataBaseHandle.getRecords(query, 1, record)
            return result
        except Exception as err:
            HandleLogs.write_error(err)
            return None



    @staticmethod
    def add_patient(data):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
            INSERT INTO ceragen.admin_patient(
                pat_person_id, pat_client_id, pat_code, pat_medical_conditions, pat_allergies,
                pat_blood_type, pat_emergency_contact_name, pat_emergency_contact_phone, pat_state,
                user_created, date_created
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            record = (
                data['pat_person_id'], data['pat_client_id'], data.get('pat_code'),
                data.get('pat_medical_conditions'), data.get('pat_allergies'),
                data.get('pat_blood_type'), data.get('pat_emergency_contact_name'),
                data.get('pat_emergency_contact_phone'), data['pat_state'],
                data['user_created'], datetime.now()
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al insertar paciente: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_patient(data):
        print("Datos recibidos para update:", data)
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
            UPDATE ceragen.admin_patient SET
                pat_person_id=%s, pat_client_id=%s, pat_code=%s, pat_medical_conditions=%s,
                pat_allergies=%s, pat_blood_type=%s, pat_emergency_contact_name=%s,
                pat_emergency_contact_phone=%s, pat_state=%s, user_modified=%s, date_modified=%s
            WHERE pat_id=%s
            """
            record = (
                data['pat_person_id'], data['pat_client_id'], data.get('pat_code'),
                data.get('pat_medical_conditions'), data.get('pat_allergies'),
                data.get('pat_blood_type'), data.get('pat_emergency_contact_name'),
                data.get('pat_emergency_contact_phone'), data['pat_state'],
                data['user_modified'], datetime.now(), data['pat_id']
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            print("ERROR EN UPDATE:", err)
            HandleLogs.write_error(err)
            v_message = "Error al actualizar paciente: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def delete_patient(pat_id, user):
        try:
            query = """
            UPDATE ceragen.admin_patient SET pat_state = FALSE, user_deleted = %s, date_deleted = %s WHERE pat_id = %s
            """
            record = (user, datetime.now(), pat_id)
            rows_affected = DataBaseHandle.ExecuteNonQuery(query, record)
            if rows_affected > 0:
                return True, f"Paciente con ID {pat_id} eliminado exitosamente."
            else:
                return False, f"No se encontró ningún paciente con ID {pat_id}."
        except Exception as err:
            HandleLogs.write_error(err)
            return None