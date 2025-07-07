import decimal
import datetime
from ....utils.database.connection_db import DataBaseHandle
from ....utils.general.logs import HandleLogs

def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    if isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()
    return obj

class AdminPromotionComponent:
    @staticmethod
    def list_all_promotions():
        try:
            query = """
                SELECT * FROM ceragen.admin_product_promotion
                ORDER BY ppr_id DESC
            """
            result = DataBaseHandle.getRecords(query, 0)
            rows = result['data'] if isinstance(result, dict) and 'data' in result else result
            rows = convert_decimal(rows)
            return rows
        except Exception as err:
            import traceback
            print("DEBUG - Error en list_all_promotions:", err)
            traceback.print_exc()
            HandleLogs.write_error(('list_all_promotions', err))
            return []

    @staticmethod
    def get_promotion_by_id(ppr_id):
        try:
            query = """
                SELECT * FROM ceragen.admin_product_promotion
                WHERE ppr_id = %s
            """
            record = (ppr_id,)
            result = DataBaseHandle.getRecords(query, 1, record)
            if result:
                result = convert_decimal(result)
                return result
            return None
        except Exception as err:
            import traceback
            print("DEBUG - Error en get_promotion_by_id:", err)
            traceback.print_exc()
            HandleLogs.write_error(('get_promotion_by_id', err))
            return None

    @staticmethod
    def add_promotion(data):
        try:
            print("DEBUG - Datos recibidos en add_promotion:", data)
            sql = """
                INSERT INTO ceragen.admin_product_promotion
                (ppr_product_id, ppr_name, ppr_description, ppr_discount_percent, ppr_extra_sessions,
                 ppr_start_date, ppr_end_date, ppr_state, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, now())
                RETURNING ppr_id
            """
            params = (
                data['ppr_product_id'], data['ppr_name'], data.get('ppr_description', ''),
                data['ppr_discount_percent'], data['ppr_extra_sessions'],
                data['ppr_start_date'], data['ppr_end_date'],
                data['ppr_state'],  # <-- AGREGADO
                data['user_created']
            )
            print("DEBUG - Insertando promoción con params:", params)
            result = DataBaseHandle.execute(sql, params)
            print("DEBUG - Resultado de execute:", result)
            if not result:
                return {'result': False, 'data': None, 'message': 'No se pudo insertar la promoción'}
            return {'result': True, 'data': result, 'message': 'Promoción insertada'}
        except Exception as err:
            import traceback
            print("DEBUG - Error en add_promotion:", err)
            traceback.print_exc()
            HandleLogs.write_error(('add_promotion', err))
            return {'result': False, 'message': str(err)}

    @staticmethod
    def update_promotion(data):
        try:
            print("DEBUG - Datos recibidos en update_promotion:", data)
            sql = """
                UPDATE ceragen.admin_product_promotion
                SET ppr_product_id=%s, ppr_name=%s, ppr_description=%s, ppr_discount_percent=%s,
                    ppr_extra_sessions=%s, ppr_start_date=%s, ppr_end_date=%s,
                    ppr_state=%s,  -- <--- AGREGADO
                    user_modified=%s, date_modified=now()
                WHERE ppr_id=%s
            """
            params = (
                data['ppr_product_id'], data['ppr_name'], data.get('ppr_description', ''),
                data['ppr_discount_percent'], data['ppr_extra_sessions'],
                data['ppr_start_date'], data['ppr_end_date'],
                data['ppr_state'],  # <--- AGREGADO
                data['user_modified'], data['ppr_id']
            )
            print("DEBUG - Actualizando promoción con params:", params)
            DataBaseHandle.execute(sql, params)
            return {'result': True, 'message': 'Promoción actualizada'}
        except Exception as err:
            import traceback
            print("DEBUG - Error en update_promotion:", err)
            traceback.print_exc()
            HandleLogs.write_error(('update_promotion', err))
            return {'result': False, 'message': str(err)}

    @staticmethod
    def delete_promotion(ppr_id, user):
        try:
            print("DEBUG - Eliminando promoción:", ppr_id, "por usuario:", user)
            sql = """
                UPDATE ceragen.admin_product_promotion
                SET ppr_state=false, user_deleted=%s, date_deleted=now()
                WHERE ppr_id=%s
            """
            params = (user, ppr_id)
            DataBaseHandle.execute(sql, params)
            return {'result': True, 'message': 'Promoción eliminada'}
        except Exception as err:
            import traceback
            print("DEBUG - Error en delete_promotion:", err)
            traceback.print_exc()
            HandleLogs.write_error(('delete_promotion', err))
            return {'result': False, 'message': str(err)}