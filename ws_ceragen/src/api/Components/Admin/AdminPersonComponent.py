from flask import jsonify
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.logs import HandleLogs
from ....utils.general.response import internal_response
from datetime import datetime, timedelta

class AdminPersonComponent:
    @staticmethod
    def list_all_admin_persons():
        try:
            query = """
            SELECT pers.per_id, pers.per_identification, pers.per_names, pers.per_surnames, pergen.genre_name as per_genre_id, mastatus.status_name as name_marital_status,
                   pers.per_country, pers.per_city, pers.per_address, pers.per_phone, pers.per_mail,
                    to_char(pers.per_birth_date, 'DD/MM/YYYY HH24:MI:SS') as per_birth_date,
                    pers.per_state, pers.user_created, to_char(pers.date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created,
                    pers.user_modified, to_char(pers.date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, pers.user_deleted, pers.date_deleted,
                    pergen.genre_name as genre_name, mastatus.status_name as name_marital_status
            FROM ceragen.admin_person pers
            INNER JOIN ceragen.admin_person_genre pergen on pergen.id = pers.per_genre_id
            INNER JOIN ceragen.admin_marital_status mastatus on mastatus.id = pers.per_marital_status_id
            WHERE pers.per_state= True
            """
            result = DataBaseHandle.getRecords(query, 0)
            return result  # Devuelve una lista de objetos de personas
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def get_admin_person_by_id(per_id):
        try:
            query = "SELECT per_id, per_identification, per_names, per_surnames, per_genre_id, per_marital_status_id,"\
                    "per_country, per_city, per_address, per_phone, per_mail, to_char(per_birth_date, 'DD/MM/YYYY HH24:MI:SS') as per_birth_date, "\
                    "per_state, user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, user_modified, date_modified, "\
                    "user_deleted, date_deleted "\
                    "FROM ceragen.admin_person WHERE per_id = %s"
            record = (per_id,)
            result = DataBaseHandle.getRecords(query, 1, record)
            DataBaseHandle.getRecords(query, 1, record)
            return result
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def add_admin_person(data_to_insert):
            try:
                v_message = None
                v_result = False
                v_data = None
                sql = "INSERT INTO ceragen.admin_person(per_identification, per_names, per_surnames, per_genre_id, " \
                      "per_marital_status_id, per_country, per_city, per_address, per_phone, per_mail, per_birth_date, " \
                      "per_state, user_created, date_created) " \
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                record = (
                    data_to_insert['per_identification'], data_to_insert['per_names'], data_to_insert['per_surnames'],
                    data_to_insert['per_genre_id'], data_to_insert['per_marital_status_id'], data_to_insert['per_country'],
                    data_to_insert['per_city'], data_to_insert['per_address'], data_to_insert['per_phone'],
                    data_to_insert['per_mail'], datetime.now(), True,
                    data_to_insert['user_process'], datetime.now())

                # Execute the UPDATE query
                v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
                if v_data is not None:
                    v_result = True

            except Exception as err:
                HandleLogs.write_error(err)
                v_message = "Error al Actualizar registro: " + str(err)
            finally:
                return internal_response(v_result, v_message, v_data)

    @staticmethod
    def update_admin_person(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None
            HandleLogs.write_log(data_to_update['per_city'])
            sql = "UPDATE ceragen.admin_person " \
                  "SET per_identification=%s, per_names=%s, per_surnames=%s, per_genre_id=%s, " \
                  "per_marital_status_id=%s, per_country=%s, per_city=%s, per_address=%s, " \
                  "per_phone=%s, per_mail=%s, per_birth_date=%s, " \
                  "user_modified=%s, date_modified=%s " \
                  "WHERE per_id = %s"

            record = (data_to_update['per_identification'], data_to_update['per_names'], data_to_update['per_surnames'],
                      data_to_update['per_genre_id'], data_to_update['per_marital_status_id'], data_to_update['per_country'],
                      data_to_update['per_city'], data_to_update['per_address'], data_to_update['per_phone'],
                      data_to_update['per_mail'], datetime.now(),
                      data_to_update['user_process'], datetime.now(), data_to_update['per_id'])

            # Execute the UPDATE query
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al Actualizar registro: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def delete_admin_person(per_id, p_user):
        try:
            HandleLogs.write_log(f"🗑️ Ejecutando eliminación lógica - ID: {per_id}, Usuario: {p_user}")

            query = "UPDATE ceragen.admin_person " \
                    "SET per_state = false, user_deleted = %s, date_deleted = %s WHERE per_id = %s"
            record = (p_user, datetime.now(), per_id)

            HandleLogs.write_log(f"SQL: {query}")
            HandleLogs.write_log(f"Parámetros: {record}")

            result = DataBaseHandle.ExecuteNonQuery(query, record)
            HandleLogs.write_log(f"Resultado ExecuteNonQuery: {result}")

            # 🔧 CORRECCIÓN: El método ExecuteNonQuery devuelve un dict, no un número
            if result and result.get('result', False):
                rows_affected = result.get('data', 0)
                HandleLogs.write_log(f"✅ Filas afectadas: {rows_affected}")

                if rows_affected > 0:
                    return True, f"Registro con ID {per_id} eliminado exitosamente."
                else:
                    return False, f"No se encontró ningún registro con ID {per_id}."
            else:
                error_msg = result.get('message', 'Error desconocido') if result else 'ExecuteNonQuery retornó None'
                HandleLogs.write_error(f"❌ Error en ExecuteNonQuery: {error_msg}")
                return False, f"Error al eliminar registro: {error_msg}"

        except Exception as err:
            HandleLogs.write_error(f"❌ Excepción en delete_admin_person: {err}")
            return False, f"Error interno: {str(err)}"
    @staticmethod
    def get_person_statistics():
        try:
            # Fechas límite para semana, mes y año
            today = datetime.now()
            start_week = (today - timedelta(days=today.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
            start_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            start_year = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

            query = """
                    SELECT
                        COUNT(*) FILTER (WHERE date_created >= %s) AS week,
                        COUNT(*) FILTER (WHERE date_created >= %s) AS month,
                        COUNT(*) FILTER (WHERE date_created >= %s) AS year
                    FROM ceragen.admin_person
                    WHERE per_state = TRUE;
                """

            params = (start_week, start_month, start_year)
            result = DataBaseHandle.getRecords(query, 1, params)
            if result and isinstance(result, dict):
                return {
                    "week": result.get('week', 0),
                    "month": result.get('month', 0),
                    "year": result.get('year', 0)
                }
            # Si el resultado es una lista con un dict
            elif result and isinstance(result, list) and isinstance(result[0], dict):
                d = result[0]
                return {
                    "week": d.get('week', 0),
                    "month": d.get('month', 0),
                    "year": d.get('year', 0)
                }
            else:
                return {"week": 0, "month": 0, "year": 0}
        except Exception as err:
            HandleLogs.write_error(err)
            return {"week": 0, "month": 0, "year": 0}

