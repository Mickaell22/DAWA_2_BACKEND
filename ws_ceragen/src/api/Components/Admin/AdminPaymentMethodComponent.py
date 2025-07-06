from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from flask import Flask, jsonify, request
from ....utils.general.response import internal_response

class PaymentMethodComponent:
    @staticmethod
    def list_all_payment_methods():
        try:
            query = """
                SELECT pme_id, pme_name, pme_description, pme_require_references, 
                       pme_require_picture_proff, pme_state, user_created, 
                       to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_payment_method
                WHERE pme_state = true
                ORDER BY pme_id DESC
            """
            res = DataBaseHandle.getRecords(query, 0)
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_payment_method_by_id(pme_id):
        try:
            query = """
                SELECT pme_id, pme_name, pme_description, pme_require_references, 
                       pme_require_picture_proff, pme_state, user_created, 
                       to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_payment_method
                WHERE pme_id = %s
            """
            record = (pme_id,)
            res = DataBaseHandle.getRecords(query, 1, record)
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def add_payment_method(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
                INSERT INTO ceragen.admin_payment_method(
                    pme_name, pme_description, pme_require_references, 
                    pme_require_picture_proff, pme_state, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            record = (
                data_to_insert['pme_name'],
                data_to_insert['pme_description'],
                data_to_insert['pme_require_references'],
                data_to_insert['pme_require_picture_proff'],
                True,
                data_to_insert['user_process'],
                datetime.now()
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al agregar método de pago: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_payment_method(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
                UPDATE ceragen.admin_payment_method
                SET pme_name = %s, pme_description = %s, 
                    pme_require_references = %s, pme_require_picture_proff = %s,
                    user_modified = %s, date_modified = %s
                WHERE pme_id = %s
            """
            record = (
                data_to_update['pme_name'],
                data_to_update['pme_description'],
                data_to_update['pme_require_references'],
                data_to_update['pme_require_picture_proff'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['pme_id']
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar método de pago: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def logical_delete_payment_method(pme_id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_payment_method
                SET pme_state = false, user_deleted = %s, date_deleted = %s
                WHERE pme_id = %s
            """
            record = (p_user, datetime.now(), pme_id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']
            if filas_afectadas > 0:
                return True, f"Método de pago con ID {pme_id} eliminado exitosamente."
            elif filas_afectadas == 0:
                return False, f"El método de pago con ID {pme_id} no existe o ya fue eliminado."
            else:
                return False, "Ocurrió un error inesperado al eliminar el registro."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"
