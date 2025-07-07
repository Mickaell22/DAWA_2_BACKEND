from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.logs import HandleLogs
from ....utils.general.response import internal_response

class AdminPatientMedicalHistoryComponent:
    @staticmethod
    def list_all_histories():
        try:
            query = "SELECT * FROM ceragen.clinic_patient_medical_history;"
            print("Consulta SQL de historial médico:", query)
            result = DataBaseHandle.getRecords(query, 0)
            print("DEBUG: Historiales médicos obtenidos de la BD:", result)
            return result
        except Exception as err:
            HandleLogs.write_error(err)
            print("ERROR list_all_histories:", err)
            return None

    @staticmethod
    def get_history_by_id(hist_id):
        try:
            query = "SELECT * FROM ceragen.clinic_patient_medical_history WHERE hist_id = %s"
            record = (hist_id,)
            print("Consulta SQL get_history_by_id:", query, record)
            result = DataBaseHandle.getRecords(query, 1, record)
            print("DEBUG: Historial médico obtenido:", result)
            return result
        except Exception as err:
            HandleLogs.write_error(err)
            print("ERROR get_history_by_id:", err)
            return None

    @staticmethod
    def add_history(data):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
            INSERT INTO ceragen.clinic_patient_medical_history(
                hist_patient_id, hist_primary_complaint, hist_onset_date, hist_related_trauma,
                hist_current_treatment, hist_notes, user_created, date_created
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """
            record = (
                data['hist_patient_id'], data.get('hist_primary_complaint'),
                data.get('hist_onset_date'), data.get('hist_related_trauma'),
                data.get('hist_current_treatment'), data.get('hist_notes'),
                data['user_created'], datetime.now()
            )
            print("INSERT historial médico:", sql, record)
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            print("ERROR add_history:", err)
            v_message = "Error al insertar historial médico: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_history(data):
        print("Datos recibidos para update historial médico:", data)
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
            UPDATE ceragen.clinic_patient_medical_history SET
                hist_patient_id=%s, hist_primary_complaint=%s, hist_onset_date=%s,
                hist_related_trauma=%s, hist_current_treatment=%s, hist_notes=%s,
                user_modified=%s, date_modified=%s
            WHERE hist_id=%s
            """
            record = (
                data['hist_patient_id'], data.get('hist_primary_complaint'),
                data.get('hist_onset_date'), data.get('hist_related_trauma'),
                data.get('hist_current_treatment'), data.get('hist_notes'),
                data['user_modified'], datetime.now(), data['hist_id']
            )
            print("UPDATE historial médico:", sql, record)
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            print("ERROR update_history:", err)
            v_message = "Error al actualizar historial médico: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def delete_history(hist_id, user):
        try:
            query = "DELETE FROM ceragen.clinic_patient_medical_history WHERE hist_id = %s"
            record = (hist_id,)
            print("DELETE físico historial médico:", query, record)
            rows_affected = DataBaseHandle.ExecuteNonQuery(query, record)
            if rows_affected > 0:
                return True, f"Historial médico con ID {hist_id} eliminado físicamente."
            else:
                return False, f"No se encontró ningún historial médico con ID {hist_id}."
        except Exception as err:
            HandleLogs.write_error(err)
            print("ERROR delete_history:", err)
            return None