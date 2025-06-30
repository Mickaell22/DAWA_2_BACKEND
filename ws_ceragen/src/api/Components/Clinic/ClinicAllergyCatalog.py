from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.response import internal_response

class ClinicAllergyCatalog_Component:
    @staticmethod
    def ListAllAllergyCatalog():
        try:
            query = (
                "SELECT alc_id, alc_name, alc_description, alc_type_id, alc_state, user_created, "
                "to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.clinic_allergy_catalog WHERE alc_state = true"
            )
            res = DataBaseHandle.getRecords(query, 0)
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetByIdAllergyCatalog(id):
        try:
            query = (
                "SELECT alc_id, alc_name, alc_description, alc_type_id, alc_state, user_created, "
                "to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.clinic_allergy_catalog WHERE alc_id = %s"
            )
            record = (id,)
            return DataBaseHandle.getRecords(query, 1, record)
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def AddAllergyCatalog(data_to_insert):
        try:
            sql = (
                "INSERT INTO ceragen.clinic_allergy_catalog "
                "(alc_name, alc_description, alc_type_id, alc_state, user_created, date_created) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            record = (
                data_to_insert['alc_name'],
                data_to_insert['alc_description'],
                data_to_insert['alc_type_id'],
                True,
                data_to_insert['user_process'],
                datetime.now()
            )
            result = DataBaseHandle.ExecuteNonQuery(sql, record)
            return internal_response(result is not None, None if result else "Error al insertar", result)
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, str(err), None)

    @staticmethod
    def UpdateAllergyCatalog(data_to_update):
        try:
            sql = (
                "UPDATE ceragen.clinic_allergy_catalog SET "
                "alc_name = %s, alc_description = %s, alc_type_id = %s, "
                "user_modified = %s, date_modified = %s "
                "WHERE alc_id = %s"
            )
            record = (
                data_to_update['alc_name'],
                data_to_update['alc_description'],
                data_to_update['alc_type_id'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['alc_id']
            )
            result = DataBaseHandle.ExecuteNonQuery(sql, record)
            return internal_response(result is not None, None if result else "Error al actualizar", result)
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, str(err), None)

    @staticmethod
    def LogicalDeleteAllergyCatalog(id, user):
        try:
            query = (
                "UPDATE ceragen.clinic_allergy_catalog SET "
                "alc_state = false, user_deleted = %s, date_deleted = %s "
                "WHERE alc_id = %s"
            )
            record = (user, datetime.now(), id)
            result = DataBaseHandle.ExecuteNonQuery(query, record)
            if not result['result']:
                return False, result['message']
            elif result['data'] == 0:
                return False, "Registro no encontrado o ya eliminado"
            return True, f"Registro con ID {id} eliminado exitosamente."
        except Exception as err:
            HandleLogs.write_error(err)
            return False, str(err)
