from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.response import internal_response

class MedicPersonType_Component:
    @staticmethod
    def ListAllMedicPersonType():
        try:
            query = (
                "SELECT mpt_id, mpt_name, mpt_description, mpt_state, user_created, "
                "to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_medic_person_type WHERE mpt_state = true"
            )
            res = DataBaseHandle.getRecords(query, 0)
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetByIdMedicPersonType(id):
        try:
            query = (
                "SELECT mpt_id, mpt_name, mpt_description, mpt_state, user_created, "
                "to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_medic_person_type WHERE mpt_id = %s"
            )
            record = (id,)
            return DataBaseHandle.getRecords(query, 1, record)
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def AddMedicPersonType(data_to_insert):
        try:
            sql = (
                "INSERT INTO ceragen.admin_medic_person_type "
                "(mpt_name, mpt_description, mpt_state, user_created, date_created) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            record = (
                data_to_insert['mpt_name'],
                data_to_insert['mpt_description'],
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
    def UpdateMedicPersonType(data_to_update):
        try:
            sql = (
                "UPDATE ceragen.admin_medic_person_type SET "
                "mpt_name = %s, mpt_description = %s, "
                "user_modified = %s, date_modified = %s "
                "WHERE mpt_id = %s"
            )
            record = (
                data_to_update['mpt_name'],
                data_to_update['mpt_description'],
                data_to_update['user_process'],
                datetime.now(),
                data_to_update['mpt_id']
            )
            result = DataBaseHandle.ExecuteNonQuery(sql, record)
            return internal_response(result is not None, None if result else "Error al actualizar", result)
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, str(err), None)

    @staticmethod
    def LogicalDeleteMedicPersonType(id, user):
        try:
            query = (
                "UPDATE ceragen.admin_medic_person_type SET "
                "mpt_state = false, user_deleted = %s, date_deleted = %s "
                "WHERE mpt_id = %s"
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
