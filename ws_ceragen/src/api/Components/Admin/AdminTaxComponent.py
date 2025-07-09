# your_project_root/src/api/Components/Admin/AdminTaxComponent.py

from datetime import datetime
from decimal import Decimal
from src.utils.general.logs import HandleLogs
from src.utils.database.connection_db import DataBaseHandle
from src.utils.general.response import internal_response


class AdminTaxComponent:

    @staticmethod
    def list_all_admin_taxes():
        try:
            query = """
                SELECT tax_id, tax_name, tax_percentage, tax_description, tax_state,
                       user_created, date_created, user_modified, date_modified,
                       user_deleted, date_deleted
                FROM ceragen.admin_tax
                WHERE tax_state = TRUE
                ORDER BY tax_id DESC
            """
            # ¡LA CORRECCIÓN CLAVE AQUÍ!
            result = DataBaseHandle.getRecords(query, 0, ())  # 0 para todos, () para sin parámetros

            if not result['result']:
                return internal_response(False, result.get('message', 'Error al listar impuestos desde DB'), [])

            return internal_response(True, "Impuestos listados con éxito", result['data'])
        except Exception as e:
            HandleLogs.write_error(f"Error en list_all_admin_taxes: {e}")
            return internal_response(False, "Error interno al listar impuestos", [])

    @staticmethod
    def get_admin_tax_by_id(tax_id):
        try:
            query = """
                SELECT tax_id, tax_name, tax_percentage, tax_description, tax_state,
                       user_created, date_created, user_modified, date_modified,
                       user_deleted, date_deleted
                FROM ceragen.admin_tax
                WHERE tax_id = %s AND tax_state = TRUE
            """
            # Para un solo registro, pasamos 1 para tamanio y (tax_id,) para los parámetros
            result = DataBaseHandle.getRecords(query, 1, (tax_id,))

            if not result['result']:
                return internal_response(False, result.get('message', 'Error al obtener impuesto'), None)

            if not result['data']:
                return internal_response(False, f"No existe el impuesto con ID {tax_id} o está inactivo.", None)

            return internal_response(True, "Impuesto obtenido con éxito",
                                     result['data'])  # .data ya es el diccionario si es 1
        except Exception as e:
            HandleLogs.write_error(f"Error en get_admin_tax_by_id: {e}")
            return internal_response(False, "Error interno al obtener impuesto", None)

    @staticmethod
    def check_tax_name_exists(tax_name, exclude_tax_id=None):
        try:
            query = "SELECT COUNT(*) FROM ceragen.admin_tax WHERE tax_name = %s AND tax_state = TRUE"
            params = [tax_name]
            if exclude_tax_id:
                query += " AND tax_id != %s"
                params.append(exclude_tax_id)

            # Para COUNT(*), siempre es un solo resultado
            result = DataBaseHandle.getRecords(query, 1, tuple(params))
            if not result['result']:
                HandleLogs.write_error(f"Error al verificar existencia de nombre de impuesto: {result.get('message')}")
                return False

            return result['data'][
                'count'] > 0  # psycogp2 RealDictCursor retorna 'count' si la columna se llama COUNT(*)
        except Exception as e:
            HandleLogs.write_error(f"Error en check_tax_name_exists: {e}")
            return False

    @staticmethod
    def insert_admin_tax(data):
        try:
            if AdminTaxComponent.check_tax_name_exists(data['tax_name']):
                return internal_response(False, "Ya existe un impuesto activo con ese nombre.")

            sql = """
                INSERT INTO ceragen.admin_tax (
                    tax_name, tax_percentage, tax_description, tax_state, user_created, date_created
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                data['tax_name'],
                data['tax_percentage'],
                data.get('tax_description'),
                True,
                data['user_process'],
                datetime.now()
            )
            res = DataBaseHandle.ExecuteNonQuery(sql, values)
            if res['result']:
                return internal_response(True, "Impuesto insertado con éxito", {
                    'tax_id': res.get('data', None)})  # ExecuteNonQuery data es lastrowid o rowcount
            else:
                return internal_response(False, res.get('message', "No se pudo insertar el impuesto."))
        except Exception as e:
            HandleLogs.write_error(f"Error en insert_admin_tax: {e}")
            return internal_response(False, "Error interno al insertar impuesto.")

    @staticmethod
    def update_admin_tax(data):
        try:
            if AdminTaxComponent.check_tax_name_exists(data['tax_name'], data['tax_id']):
                return internal_response(False, "Ya existe otro impuesto activo con ese nombre.")

            existing_tax_res = AdminTaxComponent.get_admin_tax_by_id(data['tax_id'])
            if not existing_tax_res['result'] or existing_tax_res['data'] is None:
                return internal_response(False, f"El impuesto con ID {data['tax_id']} no existe o está inactivo.", None)

            sql = """
                UPDATE ceragen.admin_tax
                SET tax_name = %s,
                    tax_percentage = %s,
                    tax_description = %s,
                    user_modified = %s,
                    date_modified = %s
                WHERE tax_id = %s AND tax_state = TRUE
            """
            values = (
                data['tax_name'],
                data['tax_percentage'],
                data.get('tax_description'),
                data['user_process'],
                datetime.now(),
                data['tax_id']
            )
            res = DataBaseHandle.ExecuteNonQuery(sql, values)
            if res['result'] and res.get('data', 0) > 0:  # data es rowcount para UPDATE
                return internal_response(True, "Impuesto actualizado con éxito", {'tax_id': data['tax_id']})
            elif res['result'] and res.get('data', 0) == 0:
                return internal_response(False,
                                         "El impuesto no fue actualizado (posiblemente ID no encontrado o sin cambios).",
                                         {'tax_id': data['tax_id']})
            else:
                return internal_response(False, res.get('message', "No se pudo actualizar el impuesto."))
        except Exception as e:
            HandleLogs.write_error(f"Error en update_admin_tax: {e}")
            return internal_response(False, "Error interno al actualizar impuesto.")

    @staticmethod
    def delete_admin_tax(tax_id, user_process):
        try:
            existing_tax_res = AdminTaxComponent.get_admin_tax_by_id(tax_id)
            if not existing_tax_res['result'] or existing_tax_res['data'] is None:
                return internal_response(False, f"El impuesto con ID {tax_id} no existe o ya está inactivo.", None)

            sql = """
                UPDATE ceragen.admin_tax
                SET tax_state = FALSE,
                    user_deleted = %s,
                    date_deleted = %s
                WHERE tax_id = %s
            """
            values = (user_process, datetime.now(), tax_id)
            result = DataBaseHandle.ExecuteNonQuery(sql, values)
            if result['result'] and result.get('data', 0) > 0:
                return internal_response(True, "Impuesto eliminado (inactivado) con éxito", {'tax_id': tax_id})
            else:
                return internal_response(False, result.get('message', "No se pudo eliminar el impuesto."))
        except Exception as e:
            HandleLogs.write_error(f"Error en delete_admin_tax: {e}")
            return internal_response(False, "Error interno al eliminar impuesto.")