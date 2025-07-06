from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from decimal import Decimal
from flask import jsonify
from ....utils.general.response import internal_response


class AdminTaxComponent:

    @staticmethod
    def list_all_admin_taxes():
        try:
            query = """
                SELECT tax_id, tax_name, tax_percentage, tax_description, tax_state, 
                       user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_tax
                WHERE tax_state = true
                ORDER BY tax_id DESC
            """
            res = DataBaseHandle.getRecords(query, 0)

            if not res['result']:
                return []

            data = res['data']
            for row in data:
                if isinstance(row['tax_percentage'], Decimal):
                    row['tax_percentage'] = float(row['tax_percentage'])

            return data

        except Exception as err:
            HandleLogs.write_error(err)
            return []

    @staticmethod
    def get_admin_tax_by_id(tax_id):
        try:
            query = """
                SELECT tax_id, tax_name, tax_percentage, tax_description, tax_state, 
                       user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_tax
                WHERE tax_id = %s
            """
            record = (tax_id,)
            res = DataBaseHandle.getRecords(query, 1, record)

            if not res['result'] or not res['data']:
                return None

            row = res['data']
            if isinstance(row.get("tax_percentage"), Decimal):
                row["tax_percentage"] = float(row["tax_percentage"])

            return row

        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def add_admin_tax(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                INSERT INTO ceragen.admin_tax(
                    tax_name, tax_percentage, tax_description, 
                    tax_state, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            record = (
                data_to_insert['tax_name'],
                data_to_insert['tax_percentage'],
                data_to_insert['tax_description'],
                True,
                data_to_insert['user_process'],
                datetime.now()
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al agregar impuesto: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_admin_tax(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                UPDATE ceragen.admin_tax
                SET tax_name = %s, tax_percentage = %s, tax_description = %s,
                    user_modified = %s, date_modified = %s
                WHERE tax_id = %s
            """
            record = (
                data_to_update['tax_name'],
                data_to_update['tax_percentage'],
                data_to_update['tax_description'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['tax_id']
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar impuesto: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def logical_delete_admin_tax(tax_id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_tax
                SET tax_state = false, user_deleted = %s, date_deleted = %s
                WHERE tax_id = %s
            """
            record = (p_user, datetime.now(), tax_id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']
            if filas_afectadas > 0:
                return True, f"Registro con ID {tax_id} eliminado exitosamente."
            elif filas_afectadas == 0:
                return False, f"El registro con ID {tax_id} no existe o ya fue eliminado."
            else:
                return False, "Ocurrió un error inesperado al eliminar el registro."

        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"
