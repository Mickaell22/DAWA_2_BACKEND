from datetime import datetime
from decimal import Decimal
from ....utils.database.connection_db import DataBaseHandle
from ....utils.general.logs import HandleLogs
from ....utils.general.response import internal_response

class AdminProductComponent:
    @staticmethod
    def list_all_admin_products():
        try:
            query = """
                SELECT pro_id, pro_code, pro_name, pro_description, pro_price, pro_total_sessions,
                       pro_duration_days, pro_image_url, pro_therapy_type_id, pro_state, user_created,
                       to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_product
                WHERE pro_state = true
                ORDER BY pro_id DESC
            """
            result = DataBaseHandle.getRecords(query, 0)
            print("DEBUG - Resultado de la consulta:", result)
            columns = [
                'pro_id', 'pro_code', 'pro_name', 'pro_description', 'pro_price', 'pro_total_sessions',
                'pro_duration_days', 'pro_image_url', 'pro_therapy_type_id', 'pro_state', 'user_created',
                'date_created', 'user_modified', 'date_modified', 'user_deleted', 'date_deleted'
            ]
            products = []
            # Cambia esto:
            # for row in result:
            #   ...
            # Por esto:
            rows = result['data'] if isinstance(result, dict) and 'data' in result else result
            for row in rows:
                print("DEBUG - Fila:", row)
                if isinstance(row, dict):
                    product = row
                else:
                    product = dict(zip(columns, row))
                if isinstance(product.get('pro_price'), Decimal):
                    product['pro_price'] = float(product['pro_price'])
                products.append(product)
            print("DEBUG - Productos mapeados:", products)
            return products
        except Exception as err:
            HandleLogs.write_error(('list_all_admin_products', err))
            return []

    @staticmethod
    def get_admin_product_by_id(pro_id):
        try:
            query = """
                SELECT pro_id, pro_code, pro_name, pro_description, pro_price, pro_total_sessions,
                       pro_duration_days, pro_image_url, pro_therapy_type_id, pro_state, user_created,
                       to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                       user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified,
                       user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted
                FROM ceragen.admin_product
                WHERE pro_id = %s
            """
            record = (pro_id,)
            result = DataBaseHandle.getRecords(query, 1, record)
            columns = [
                'pro_id', 'pro_code', 'pro_name', 'pro_description', 'pro_price', 'pro_total_sessions',
                'pro_duration_days', 'pro_image_url', 'pro_therapy_type_id', 'pro_state', 'user_created',
                'date_created', 'user_modified', 'date_modified', 'user_deleted', 'date_deleted'
            ]
            if result:
                if isinstance(result, dict):
                    product = result
                else:
                    product = dict(zip(columns, result))
                if isinstance(product.get('pro_price'), Decimal):
                    product['pro_price'] = float(product['pro_price'])
                return product
            return None
        except Exception as err:
            HandleLogs.write_error(('get_admin_product_by_id', err))
            return None

    @staticmethod
    def add_admin_product(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
                INSERT INTO ceragen.admin_product
                (pro_code, pro_name, pro_description, pro_price, pro_total_sessions, pro_duration_days,
                 pro_image_url, pro_therapy_type_id, pro_state, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, true, %s, %s)
            """
            record = (
                data_to_insert['pro_code'],
                data_to_insert['pro_name'],
                data_to_insert.get('pro_description', ''),
                data_to_insert['pro_price'],
                data_to_insert['pro_total_sessions'],
                data_to_insert['pro_duration_days'],
                data_to_insert.get('pro_image_url', ''),
                data_to_insert['pro_therapy_type_id'],
                data_to_insert['user_process'],
                datetime.now()
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
                v_message = "Producto insertado correctamente"
        except Exception as err:
            HandleLogs.write_error(('add_admin_product', err))
            v_message = "Error al insertar producto: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_admin_product(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = """
                UPDATE ceragen.admin_product
                SET pro_code = %s, pro_name = %s, pro_description = %s, pro_price = %s,
                    pro_total_sessions = %s, pro_duration_days = %s, pro_image_url = %s,
                    pro_therapy_type_id = %s, user_modified = %s, date_modified = %s
                WHERE pro_id = %s
            """
            record = (
                data_to_update['pro_code'],
                data_to_update['pro_name'],
                data_to_update.get('pro_description', ''),
                data_to_update['pro_price'],
                data_to_update['pro_total_sessions'],
                data_to_update['pro_duration_days'],
                data_to_update.get('pro_image_url', ''),
                data_to_update['pro_therapy_type_id'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['pro_id']
            )
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True
                v_message = "Producto actualizado correctamente"
        except Exception as err:
            HandleLogs.write_error(('update_admin_product', err))
            v_message = "Error al actualizar producto: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def delete_admin_product(pro_id, p_user):
        try:
            sql = """
                UPDATE ceragen.admin_product
                SET pro_state = false, user_deleted = %s, date_deleted = %s
                WHERE pro_id = %s
            """
            record = (p_user, datetime.now(), pro_id)
            rows_affected = DataBaseHandle.ExecuteNonQuery(sql, record)
            v_result = rows_affected is not None
            v_message = "Producto eliminado correctamente" if v_result else "No se pudo eliminar el producto"
            return internal_response(v_result, v_message, rows_affected)
        except Exception as err:
            HandleLogs.write_error(('delete_admin_product', err))
            return internal_response(False, "Error al eliminar producto: " + str(err), None)