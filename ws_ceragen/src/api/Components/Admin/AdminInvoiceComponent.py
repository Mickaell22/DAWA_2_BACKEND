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

class Invoice_Component:
    @staticmethod
    def ListAllInvoices():
        try:
            query = (
                "SELECT inv_id, inv_number, to_char(inv_date, 'DD/MM/YYYY HH24:MI:SS') as inv_date, "
                "inv_client_id, inv_patient_id, inv_subtotal, inv_discount, inv_tax, inv_grand_total, inv_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice ORDER BY date_created DESC"
            )
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def ListAllInvoicesByStateTrue():
        try:
            query = (
                "SELECT inv_id, inv_number, to_char(inv_date, 'DD/MM/YYYY HH24:MI:SS') as inv_date, "
                "inv_client_id, inv_patient_id, inv_subtotal, inv_discount, inv_tax, inv_grand_total, inv_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice WHERE inv_state = true ORDER BY date_created DESC"
            )
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetInvoiceById(inv_id):
        try:
            query = (
                "SELECT inv_id, inv_number, to_char(inv_date, 'DD/MM/YYYY HH24:MI:SS') as inv_date, "
                "inv_client_id, inv_patient_id, inv_subtotal, inv_discount, inv_tax, inv_grand_total, inv_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice WHERE inv_id = %s"
            )
            record = DataBaseHandle.getRecords(query, 1, (inv_id,))
            if record:
                record = _convert_decimals_to_floats(record)
            return record
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def AddInvoice(data_to_insert):
        try:
            v_result = False
            v_data = None
            v_message = None

            sql = """
                INSERT INTO ceragen.admin_invoice(
                    inv_number, inv_date, inv_client_id, inv_patient_id, 
                    inv_subtotal, inv_discount, inv_tax, 
                    inv_state, user_created, date_created
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            record = (
                data_to_insert['inv_number'],
                datetime.now(),
                data_to_insert['inv_client_id'],
                data_to_insert['inv_patient_id'],
                data_to_insert['inv_subtotal'],
                data_to_insert['inv_discount'],
                data_to_insert['inv_tax'],
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
            v_message = "Error al agregar la factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def UpdateInvoice(data_to_update):
        try:
            v_result = False
            v_data = None
            v_message = None

            sql = """
                UPDATE ceragen.admin_invoice 
                SET inv_number=%s, inv_client_id=%s, inv_patient_id=%s,
                    inv_subtotal=%s, inv_discount=%s, inv_tax=%s,
                    user_modified=%s, date_modified=%s 
                WHERE inv_id = %s
            """

            record = (
                data_to_update['inv_number'],
                data_to_update['inv_client_id'],
                data_to_update['inv_patient_id'],
                data_to_update['inv_subtotal'],
                data_to_update['inv_discount'],
                data_to_update['inv_tax'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['inv_id']
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data['result']:
                v_result = True
            else:
                v_message = v_data['message']

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar la factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def LogicalDeleteInvoice(inv_id, user_process):
        try:
            query = """
                UPDATE ceragen.admin_invoice 
                SET inv_state = false, user_deleted = %s, date_deleted = %s 
                WHERE inv_id = %s
            """
            record = (user_process, datetime.now(), inv_id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']

            if filas_afectadas > 0:
                return True, f"Factura con ID {inv_id} eliminada exitosamente."
            elif filas_afectadas == 0:
                return False, f"La factura con ID {inv_id} no existe o ya fue eliminada."
            else:
                return False, "Ocurrió un error inesperado al eliminar la factura."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"
