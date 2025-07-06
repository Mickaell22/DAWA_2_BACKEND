from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.response import internal_response
from decimal import Decimal

def _convert_decimals_to_floats(records):
    if isinstance(records, list):
        return [_convert_decimals_to_floats(r) for r in records]
    elif isinstance(records, dict):
        return {k: (float(v) if isinstance(v, Decimal) else v) for k, v in records.items()}
    else:
        return records

class Invoice_Tax_Component:
    @staticmethod
    def ListAllInvoicesTaxes():
        try:
            query = """
                SELECT int_id, int_invoice_id, int_tax_id, int_tax_amount, int_state,
                       user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') AS date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') AS date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') AS date_deleted
                FROM ceragen.admin_invoice_tax
            """
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, "Error al listar los impuestos de facturas", None)

    @staticmethod
    def ListAllInvoicesTaxesByStateTrue():
        try:
            query = """
                SELECT int_id, int_invoice_id, int_tax_id, int_tax_amount, int_state,
                       user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') AS date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') AS date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') AS date_deleted
                FROM ceragen.admin_invoice_tax
                WHERE int_state = true
            """
            records = DataBaseHandle.getRecords(query, 0)
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, "Error al listar impuestos activos", None)

    @staticmethod
    def GetInvoiceTaxById(id):
        try:
            query = """
                SELECT int_id, int_invoice_id, int_tax_id, int_tax_amount, int_state,
                       user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') AS date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') AS date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') AS date_deleted
                FROM ceragen.admin_invoice_tax
                WHERE int_id = %s
            """
            record = DataBaseHandle.getRecords(query, 1, (id,))
            if record:
                record = _convert_decimals_to_floats(record)
            return record
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, f"Error al obtener el impuesto con ID {id}", None)

    @staticmethod
    def GetInvoiceTaxByInvoiceId(int_invoice_id):
        try:
            query = """
                SELECT int_id, int_invoice_id, int_tax_id, int_tax_amount, int_state,
                       user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') AS date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') AS date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') AS date_deleted
                FROM ceragen.admin_invoice_tax
                WHERE int_invoice_id = %s
            """
            records = DataBaseHandle.getRecords(query, 0, (int_invoice_id,))
            if records:
                records = _convert_decimals_to_floats(records)
            return records
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, "Error al obtener los impuestos de la factura", None)

    @staticmethod
    def AddInvoiceTax(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                INSERT INTO ceragen.admin_invoice_tax (
                    int_invoice_id, int_tax_id, int_tax_amount, int_state,
                    user_created, date_created
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """

            record = (
                data_to_insert['int_invoice_id'],
                data_to_insert['int_tax_id'],
                data_to_insert['int_tax_amount'],
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
            v_message = "Error al agregar impuesto de factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def UpdateInvoiceTax(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None

            sql = """
                UPDATE ceragen.admin_invoice_tax
                SET int_invoice_id = %s, int_tax_id = %s, int_tax_amount = %s,
                    user_modified = %s, date_modified = %s
                WHERE int_id = %s
            """

            record = (
                data_to_update['int_invoice_id'],
                data_to_update['int_tax_id'],
                data_to_update['int_tax_amount'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['int_id']
            )

            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data['result']:
                v_result = True
            else:
                v_message = v_data['message']

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al actualizar impuesto de factura: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def LogicalDeleteInvoiceTax(id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_invoice_tax
                SET int_state = false, user_deleted = %s, date_deleted = %s
                WHERE int_id = %s
            """
            record = (p_user, datetime.now(), id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']
            if filas_afectadas > 0:
                return True, f"Impuesto con ID {id} eliminado exitosamente."
            elif filas_afectadas == 0:
                return False, f"El impuesto con ID {id} no existe o ya fue eliminado."
            else:
                return False, "Ocurrió un error inesperado al eliminar el impuesto."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"

    @staticmethod
    def LogicalDeleteInvoiceTaxByInvoiceId(int_invoice_id, p_user):
        try:
            query = """
                UPDATE ceragen.admin_invoice_tax
                SET int_state = false, user_deleted = %s, date_deleted = %s
                WHERE int_invoice_id = %s
            """
            record = (p_user, datetime.now(), int_invoice_id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            if not res['result']:
                return False, f"Error en la base de datos: {res['message']}"

            filas_afectadas = res['data']
            if filas_afectadas > 0:
                return True, f"Impuestos con ID de factura {int_invoice_id} eliminados exitosamente."
            elif filas_afectadas == 0:
                return False, f"No existen impuestos con ID de factura {int_invoice_id} o ya fueron eliminados."
            else:
                return False, "Ocurrió un error inesperado al eliminar los impuestos."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, f"Error inesperado: {str(err)}"
