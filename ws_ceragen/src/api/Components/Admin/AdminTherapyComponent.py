from flask import jsonify
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.logs import HandleLogs
from ....utils.general.response import internal_response

class AdminTherapyComponent:
    @staticmethod
    def list_all_admin_therapies():
        try:
            query = """
                SELECT tht_id, tht_name, tht_description, tht_state, user_created, 
                       to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_therapy_type
                WHERE tht_state = true
                ORDER BY tht_id DESC
            """
            result = DataBaseHandle.getRecords(query, 0)
            return result  # Devuelve lista de terapias o []
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_admin_therapy_by_id(tht_id):
        try:
            query = """
                SELECT tht_id, tht_name, tht_description, tht_state, user_created, 
                       to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_therapy_type
                WHERE tht_id = %s
            """
            record = (tht_id,)
            result = DataBaseHandle.getRecords(query, 1, record)
            return result
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def add_admin_therapy(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
                INSERT INTO ceragen.admin_therapy_type
                (tht_name, tht_description, tht_state, user_created, date_created)
                VALUES (%s, %s, true, %s, %s)
            """
            record = (
                data_to_insert['tht_name'],
                data_to_insert.get('tht_description', ''),
                data_to_insert['user_process'],
                datetime.now()
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al insertar terapia: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_admin_therapy(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
                UPDATE ceragen.admin_therapy_type
                SET tht_name = %s, tht_description = %s, user_modified = %s, date_modified = %s
                WHERE tht_id = %s
            """
            record = (
                data_to_update['tht_name'],
                data_to_update.get('tht_description', ''),
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['tht_id']
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar terapia: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def delete_admin_therapy(tht_id, p_user):
        try:
            sql = """
                    UPDATE ceragen.admin_therapy_type
                    SET tht_state = false, user_deleted = %s, date_deleted = %s
                    WHERE tht_id = %s
                """
            record = (p_user, datetime.now(), tht_id)
            rows_affected = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log("Filas afectadas: " + str(rows_affected))
            if rows_affected > 0:
                return {
                    "result": True,
                    "message": f"Terapia con ID {tht_id} eliminada exitosamente.",
                    "data": rows_affected
                }
            else:
                return {
                    "result": False,
                    "message": f"No se encontró ninguna terapia con ID {tht_id}.",
                    "data": 0
                }
        except Exception as err:
            HandleLogs.write_error(err)
            return {
                "result": False,
                "message": str(err),
                "data": 0
            }