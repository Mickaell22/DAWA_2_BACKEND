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

class Invoice_Payment_Component:
    @staticmethod
    def ListAllInvoicesPayments():
        try:
            query = (
                "SELECT inp_id, inp_invoice_id, inp_payment_method_id, inp_amount, "
                "inp_reference, inp_proof_image_path, inp_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_payment"
            )
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def ListAllInvoicesPaymentsByStateTrue():
        try:
            query = (
                "SELECT inp_id, inp_invoice_id, inp_payment_method_id, inp_amount, "
                "inp_reference, inp_proof_image_path, inp_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_payment WHERE inp_state = true"
            )
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetInvoicePaymentById(id):
        try:
            query = (
                "SELECT inp_id, inp_invoice_id, inp_payment_method_id, inp_amount, "
                "inp_reference, inp_proof_image_path, inp_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_payment WHERE inp_id = %s"
            )
            record = DataBaseHandle.getRecords(query, 1, (id,))
            if record:
                record = _convert_decimals_to_floats(record)
            return record
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetInvoicePaymentByInvoiceId(inp_invoice_id):
        try:
            query = (
                "SELECT inp_id, inp_invoice_id, inp_payment_method_id, inp_amount, "
                "inp_reference, inp_proof_image_path, inp_state, "
                "user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_invoice_payment WHERE inp_invoice_id = %s"
            )
            records = DataBaseHandle.getRecords(query, 0, (inp_invoice_id,))
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetTotalPaidAmountByInvoiceId(invoice_id):
        try:
            query = """
                SELECT COALESCE(SUM(inp_amount), 0) as total_paid
                FROM ceragen.admin_invoice_payment
                WHERE inp_invoice_id = %s AND inp_state = true
            """
            result = DataBaseHandle.getRecords(query, 1, (invoice_id,))
            if result:
                total_paid = result.get('total_paid', 0)
                if isinstance(total_paid, Decimal):
                    return float(total_paid)
                return total_paid
            return 0
        except Exception as err:
            HandleLogs.write_error(err)
            return 0

    @staticmethod
    def GetTotalIncomeAmount():
        try:
            query = """
                SELECT COALESCE(SUM(inp_amount), 0) as total_income
                FROM ceragen.admin_invoice_payment
                WHERE inp_state = true
            """
            result = DataBaseHandle.getRecords(query, 1)

            if result["result"] and result["data"]:
                # result["data"] es un dict si usamos RealDictCursor
                # Si es tupla, usa result["data"][0]
                total_income = result["data"]["total_income"]
                return float(total_income) if isinstance(total_income, Decimal) else total_income

            return 0
        except Exception as err:
            HandleLogs.write_error(err)
            return 0

    @staticmethod
    def AddInvoicePayment(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                INSERT INTO ceragen.admin_invoice_payment(
                    inp_invoice_id, inp_payment_method_id, inp_amount, inp_reference, 
                    inp_proof_image_path, inp_state, user_created, date_created
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """

            record = (
                data_to_insert['inp_invoice_id'],
                data_to_insert['inp_payment_method_id'],
                data_to_insert['inp_amount'],
                data_to_insert['inp_reference'],
                data_to_insert['inp_proof_image_path'],
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
            v_message = "Error al agregar pago de factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def UpdateInvoicePayment(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                UPDATE ceragen.admin_invoice_payment 
                SET inp_invoice_id=%s, inp_payment_method_id=%s, inp_amount=%s, 
                    inp_reference=%s, inp_proof_image_path=%s, user_modified=%s, date_modified=%s 
                WHERE inp_id = %s
            """

            record = (
                data_to_update['inp_invoice_id'],
                data_to_update['inp_payment_method_id'],
                data_to_update['inp_amount'],
                data_to_update['inp_reference'],
                data_to_update['inp_proof_image_path'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['inp_id']
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data['result']:
                v_result = True
            else:
                v_message = v_data['message']

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar pago de factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def LogicalDeleteInvoicePayment(id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_invoice_payment 
                SET inp_state = false, user_deleted = %s, date_deleted = %s 
                WHERE inp_id = %s
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
    def LogicalDeleteInvoicePaymentByInvoiceId(inp_invoice_id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_invoice_payment 
                SET inp_state = false, user_deleted = %s, date_deleted = %s 
                WHERE inp_invoice_id = %s
            """
            record = (p_user, datetime.now(), inp_invoice_id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']

            if filas_afectadas > 0:
                return True, f"Registros con ID de factura {inp_invoice_id} eliminados exitosamente."
            elif filas_afectadas == 0:
                return False, f"No existen registros con ID de factura {inp_invoice_id} o ya fueron eliminados."
            else:
                return False, "Ocurrió un error inesperado al eliminar los registros."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"
