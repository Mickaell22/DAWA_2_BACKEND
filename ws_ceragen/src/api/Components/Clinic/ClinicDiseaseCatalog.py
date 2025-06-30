from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from ....utils.general.response import internal_response

class ClinicDiseaseCatalog_Component:
    @staticmethod
    def ListAllDiseaseCatalog():
        try:
            query = (
                "SELECT dis_id, dis_name, dis_description, dis_type_id, dis_state, user_created, "
                "to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.clinic_disease_catalog WHERE dis_state = true"
            )
            return DataBaseHandle.getRecords(query, 0)
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetByIdDiseaseCatalog(id):
        try:
            query = (
                "SELECT dis_id, dis_name, dis_description, dis_type_id, dis_state, user_created, "
                "to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.clinic_disease_catalog WHERE dis_id = %s"
            )
            return DataBaseHandle.getRecords(query, 1, (id,))
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def AddDiseaseCatalog(data):
        try:
            query = (
                "INSERT INTO ceragen.clinic_disease_catalog "
                "(dis_name, dis_description, dis_type_id, dis_state, user_created, date_created) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            record = (
                data['dis_name'],
                data['dis_description'],
                data['dis_type_id'],
                True,
                data['user_process'],
                datetime.now()
            )
            result = DataBaseHandle.ExecuteNonQuery(query, record)
            return internal_response(result is not None, None if result else "Error al insertar", result)
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, str(err), None)

    @staticmethod
    def UpdateDiseaseCatalog(data):
        try:
            query = (
                "UPDATE ceragen.clinic_disease_catalog SET "
                "dis_name = %s, dis_description = %s, dis_type_id = %s, "
                "user_modified = %s, date_modified = %s "
                "WHERE dis_id = %s"
            )
            record = (
                data['dis_name'],
                data['dis_description'],
                data['dis_type_id'],
                data['user_process'],
                datetime.now(),
                data['dis_id']
            )
            result = DataBaseHandle.ExecuteNonQuery(query, record)
            return internal_response(result is not None, None if result else "Error al actualizar", result)
        except Exception as err:
            HandleLogs.write_error(err)
            return internal_response(False, str(err), None)

    @staticmethod
    def LogicalDeleteDiseaseCatalog(id, user):
        try:
            query = (
                "UPDATE ceragen.clinic_disease_catalog SET "
                "dis_state = false, user_deleted = %s, date_deleted = %s "
                "WHERE dis_id = %s"
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
