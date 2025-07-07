from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from decimal import Decimal
from flask import jsonify
from ....utils.general.response import internal_response
import psycopg2


class AdminTaxComponent:

    @staticmethod
    def list_all_admin_taxes():
        """Obtener todos los impuestos activos"""
        try:
            HandleLogs.write_log("Listando todos los impuestos")

            query = """
                SELECT 
                    tax_id,
                    tax_name,
                    tax_percentage,
                    tax_description,
                    tax_state,
                    user_created,
                    to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                    user_modified,
                    to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                    user_deleted,
                    to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_tax 
                WHERE tax_state = true
                ORDER BY tax_id DESC
            """

            # Usar DataBaseHandle.getRecords para obtener todos los registros
            response = DataBaseHandle.getRecords(query, 0)  # 0 = todos los registros

            if not response['result']:
                HandleLogs.write_error(f"Error al obtener impuestos: {response['message']}")
                return []

            data = response['data'] if response['data'] else []

            # Convertir Decimal a float si es necesario
            for row in data:
                if isinstance(row.get('tax_percentage'), Decimal):
                    row['tax_percentage'] = float(row['tax_percentage'])

            HandleLogs.write_log(f"Encontrados {len(data)} impuestos")
            return data

        except Exception as e:
            HandleLogs.write_error(f"Error en list_all_admin_taxes: {e}")
            return []

    @staticmethod
    def get_admin_tax_by_id(tax_id):
        """Obtener un impuesto por ID"""
        try:
            HandleLogs.write_log(f"Obteniendo impuesto con ID: {tax_id}")

            query = """
                SELECT 
                    tax_id,
                    tax_name,
                    tax_percentage,
                    tax_description,
                    tax_state,
                    user_created,
                    to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                    user_modified,
                    to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                    user_deleted,
                    to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_tax 
                WHERE tax_id = %s
            """

            # Usar DataBaseHandle.getRecords para obtener un solo registro
            response = DataBaseHandle.getRecords(query, 1, (tax_id,))  # 1 = un solo registro

            if not response['result']:
                HandleLogs.write_error(f"Error al obtener impuesto: {response['message']}")
                return None

            row = response['data']

            if row:
                # Convertir Decimal a float si es necesario
                if isinstance(row.get('tax_percentage'), Decimal):
                    row['tax_percentage'] = float(row['tax_percentage'])
                
                HandleLogs.write_log(f"Impuesto encontrado: {row['tax_name']}")
                return row
            else:
                HandleLogs.write_log(f"Impuesto no encontrado: {tax_id}")
                return None

        except Exception as e:
            HandleLogs.write_error(f"Error en get_admin_tax_by_id: {e}")
            return None

    @staticmethod
    def check_tax_name_exists(tax_name, exclude_id=None):
        """Verificar si existe un impuesto con el mismo nombre"""
        try:
            if exclude_id:
                query = """
                    SELECT COUNT(*) as count FROM ceragen.admin_tax 
                    WHERE LOWER(TRIM(tax_name)) = LOWER(TRIM(%s)) 
                    AND tax_id != %s AND tax_state = true
                """
                response = DataBaseHandle.getRecords(query, 1, (tax_name, exclude_id))
            else:
                query = """
                    SELECT COUNT(*) as count FROM ceragen.admin_tax 
                    WHERE LOWER(TRIM(tax_name)) = LOWER(TRIM(%s)) 
                    AND tax_state = true
                """
                response = DataBaseHandle.getRecords(query, 1, (tax_name,))

            if response['result'] and response['data']:
                count = response['data']['count']
                return count > 0

            return True  # Asumir que existe para evitar duplicados

        except Exception as e:
            HandleLogs.write_error(f"Error verificando nombre de impuesto: {e}")
            return True  # Asumir que existe para evitar duplicados

    @staticmethod
    def add_admin_tax(data_to_insert):
        """Crear un nuevo impuesto (mantiene compatibilidad con versión anterior)"""
        try:
            v_message = None
            v_result = False
            v_data = None

            # Verificar si ya existe un impuesto con el mismo nombre
            if AdminTaxComponent.check_tax_name_exists(data_to_insert.get('tax_name')):
                v_message = f"Ya existe un impuesto con el nombre: {data_to_insert.get('tax_name')}"
                return internal_response(v_result, v_message, v_data)

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
    def create_admin_tax(tax_data, user_created):
        """Crear un nuevo impuesto (versión mejorada)"""
        try:
            HandleLogs.write_log(f"Creando nuevo impuesto: {tax_data.get('tax_name')}")

            # Verificar si ya existe un impuesto con el mismo nombre
            if AdminTaxComponent.check_tax_name_exists(tax_data.get('tax_name')):
                HandleLogs.write_error(f"Ya existe un impuesto con el nombre: {tax_data.get('tax_name')}")
                return False

            insert_query = """
                INSERT INTO ceragen.admin_tax 
                (tax_name, tax_percentage, tax_description, tax_state, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, NOW())
                RETURNING tax_id
            """

            # Usar DataBaseHandle.ExecuteInsert para obtener el ID del registro insertado
            response = DataBaseHandle.ExecuteInsert(insert_query, (
                tax_data.get('tax_name').strip(),
                tax_data.get('tax_percentage'),
                tax_data.get('tax_description', '').strip() if tax_data.get('tax_description') else None,
                True,
                user_created
            ))

            if response['result'] and response['data']:
                tax_id = response['data'][0]['tax_id']
                HandleLogs.write_log(f"Impuesto creado exitosamente con ID: {tax_id}")
                return tax_id
            else:
                HandleLogs.write_error(f"Error al crear impuesto: {response['message']}")
                return False

        except Exception as e:
            HandleLogs.write_error(f"Error en create_admin_tax: {e}")
            return False

    @staticmethod
    def update_admin_tax(data_to_update):
        """Actualizar un impuesto existente (mantiene compatibilidad)"""
        try:
            v_message = None
            v_result = False
            v_data = None

            # Verificar si ya existe otro impuesto con el mismo nombre
            if AdminTaxComponent.check_tax_name_exists(
                data_to_update.get('tax_name'), 
                data_to_update.get('tax_id')
            ):
                v_message = f"Ya existe otro impuesto con el nombre: {data_to_update.get('tax_name')}"
                return internal_response(v_result, v_message, v_data)

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
    def update_admin_tax_v2(tax_id, tax_data, user_modified):
        """Actualizar un impuesto existente (versión mejorada)"""
        try:
            HandleLogs.write_log(f"Actualizando impuesto ID: {tax_id}")

            # Verificar si el impuesto existe
            check_query = "SELECT COUNT(*) as count FROM ceragen.admin_tax WHERE tax_id = %s AND tax_state = true"
            check_response = DataBaseHandle.getRecords(check_query, 1, (tax_id,))

            if not check_response['result'] or not check_response['data'] or check_response['data']['count'] == 0:
                HandleLogs.write_error(f"Impuesto no encontrado: {tax_id}")
                return False

            # Verificar si ya existe otro impuesto con el mismo nombre
            if AdminTaxComponent.check_tax_name_exists(tax_data.get('tax_name'), tax_id):
                HandleLogs.write_error(f"Ya existe otro impuesto con el nombre: {tax_data.get('tax_name')}")
                return False

            update_query = """
                UPDATE ceragen.admin_tax 
                SET tax_name = %s, 
                    tax_percentage = %s, 
                    tax_description = %s,
                    user_modified = %s,
                    date_modified = NOW()
                WHERE tax_id = %s
            """

            # Usar DataBaseHandle.ExecuteNonQuery para actualización
            response = DataBaseHandle.ExecuteNonQuery(update_query, (
                tax_data.get('tax_name').strip(),
                tax_data.get('tax_percentage'),
                tax_data.get('tax_description', '').strip() if tax_data.get('tax_description') else None,
                user_modified,
                tax_id
            ))

            if response['result']:
                HandleLogs.write_log(f"Impuesto actualizado exitosamente: {tax_id}")
                return True
            else:
                HandleLogs.write_error(f"Error al actualizar impuesto: {response['message']}")
                return False

        except Exception as e:
            HandleLogs.write_error(f"Error en update_admin_tax_v2: {e}")
            return False

    @staticmethod
    def get_tax_usage_info(tax_id):
        """Obtener información de uso del impuesto antes de eliminarlo"""
        try:
            # Verificar uso en facturas
            usage_query = """
                SELECT COUNT(*) as count FROM ceragen.admin_invoice_tax 
                WHERE int_tax_id = %s AND int_state = true
            """

            response = DataBaseHandle.getRecords(usage_query, 1, (tax_id,))

            if response['result'] and response['data']:
                invoice_count = response['data']['count']

                if invoice_count > 0:
                    return {
                        "can_delete": False,
                        "reason": f"El impuesto está siendo usado en {invoice_count} factura(s)"
                    }

            return {"can_delete": True, "reason": None}

        except Exception as e:
            HandleLogs.write_error(f"Error verificando uso del impuesto: {e}")
            return {"can_delete": False, "reason": "Error verificando dependencias"}

    @staticmethod
    def logical_delete_admin_tax(tax_id, p_user):
        """Eliminar (desactivar) un impuesto (mantiene compatibilidad)"""
        try:
            # Verificar si se puede eliminar
            usage_info = AdminTaxComponent.get_tax_usage_info(tax_id)
            if not usage_info["can_delete"]:
                return False, usage_info['reason']

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

    @staticmethod
    def delete_admin_tax(tax_id, user_deleted):
        """Eliminar (desactivar) un impuesto (versión mejorada)"""
        try:
            HandleLogs.write_log(f"Eliminando impuesto ID: {tax_id}")

            # Verificar si se puede eliminar
            usage_info = AdminTaxComponent.get_tax_usage_info(tax_id)
            if not usage_info["can_delete"]:
                HandleLogs.write_error(f"No se puede eliminar el impuesto {tax_id}: {usage_info['reason']}")
                return False

            # Verificar si el impuesto existe
            check_query = "SELECT COUNT(*) as count FROM ceragen.admin_tax WHERE tax_id = %s AND tax_state = true"
            check_response = DataBaseHandle.getRecords(check_query, 1, (tax_id,))

            if not check_response['result'] or not check_response['data'] or check_response['data']['count'] == 0:
                HandleLogs.write_error(f"Impuesto no encontrado: {tax_id}")
                return False

            # Soft delete
            delete_query = """
                UPDATE ceragen.admin_tax 
                SET tax_state = false,
                    user_deleted = %s,
                    date_deleted = NOW()
                WHERE tax_id = %s
            """

            response = DataBaseHandle.ExecuteNonQuery(delete_query, (user_deleted, tax_id))

            if response['result']:
                HandleLogs.write_log(f"Impuesto eliminado exitosamente: {tax_id}")
                return True
            else:
                HandleLogs.write_error(f"Error al eliminar impuesto: {response['message']}")
                return False

        except Exception as e:
            HandleLogs.write_error(f"Error en delete_admin_tax: {e}")
            return False