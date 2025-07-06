from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from flask import Flask, jsonify, request
from ....utils.general.response import internal_response
from decimal import Decimal

def _convert_decimals_to_floats(records):
    if isinstance(records, list):
        return [_convert_decimals_to_floats(r) for r in records]
    elif isinstance(records, dict):
        return {k: (float(v) if isinstance(v, Decimal) else v) for k, v in records.items()}
    else:
        return records

class Invoice_Detail_Component:
    @staticmethod
    def ListAllInvoicesDetails():
        try:
            query = (
                "SELECT ind_id, ind_invoice_id, ind_product_id, ind_quantity, "
                "ind_unit_price, ind_total, ind_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_detail ORDER BY date_created DESC"
            )
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def ListAllInvoicesDetailsByStateTrue():
        try:
            query = (
                "SELECT ind_id, ind_invoice_id, ind_product_id, ind_quantity, "
                "ind_unit_price, ind_total, ind_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_detail WHERE ind_state = true ORDER BY date_created DESC"
            )
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetInvoiceDetailById(id):
        try:
            query = (
                "SELECT ind_id, ind_invoice_id, ind_product_id, ind_quantity, "
                "ind_unit_price, ind_total, ind_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_detail WHERE ind_id = %s"
            )
            record = DataBaseHandle.getRecords(query, 1, (id,))
            if record:
                record = _convert_decimals_to_floats(record)
            return record
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetInvoiceDetailsByInvoiceId(ind_invoice_id):
        try:
            query = (
                "SELECT ind_id, ind_invoice_id, ind_product_id, ind_quantity, "
                "ind_unit_price, ind_total, ind_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_detail WHERE ind_invoice_id = %s"
            )
            records = DataBaseHandle.getRecords(query, 0, (ind_invoice_id,))
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def AddInvoiceDetail(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                INSERT INTO ceragen.admin_invoice_detail(
                    ind_invoice_id, ind_product_id, ind_quantity, ind_unit_price, 
                    ind_total, ind_state, user_created, date_created
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """

            record = (
                data_to_insert['ind_invoice_id'],
                data_to_insert['ind_product_id'],
                data_to_insert['ind_quantity'],
                data_to_insert['ind_unit_price'],
                data_to_insert['ind_total'],
                True,
                data_to_insert['user_process'],
                datetime.now()
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data['result']:
                v_result = True
            else:
                v_message = v_data['message']

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al agregar detalle de factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def UpdateInvoiceDetail(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                UPDATE ceragen.admin_invoice_detail 
                SET ind_invoice_id=%s, ind_product_id=%s, ind_quantity=%s, 
                    ind_unit_price=%s, ind_total=%s, user_modified=%s, date_modified=%s 
                WHERE ind_id = %s
            """

            record = (
                data_to_update['ind_invoice_id'],
                data_to_update['ind_product_id'],
                data_to_update['ind_quantity'],
                data_to_update['ind_unit_price'],
                data_to_update['ind_total'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['ind_id']
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data['result']:
                v_result = True
            else:
                v_message = v_data['message']

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar detalle de factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def LogicalDeleteInvoiceDetail(id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_invoice_detail 
                SET ind_state = false, user_deleted = %s, date_deleted = %s 
                WHERE ind_id = %s
            """
            record = (p_user, datetime.now(), id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']

            if filas_afectadas > 0:
                return True, f"Registro con ID {id} eliminado exitosamente."
            elif filas_afectadas == 0:
                return False, f"El registro con ID {id} no existe o ya fue eliminado."
            else:
                return False, "Ocurrió un error inesperado al eliminar el registro."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"

    @staticmethod
    def LogicalDeleteInvoiceDetailsByInvoiceId(ind_invoice_id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_invoice_detail 
                SET ind_state = false, user_deleted = %s, date_deleted = %s 
                WHERE ind_invoice_id = %s
            """
            record = (p_user, datetime.now(), ind_invoice_id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']

            if filas_afectadas > 0:
                return True, f"Registros con ID de factura {ind_invoice_id} eliminados exitosamente."
            elif filas_afectadas == 0:
                return False, f"No existen registros con ID de factura {ind_invoice_id} o ya fueron eliminados."
            else:
                return False, "Ocurrió un error inesperado al eliminar los registros."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"
