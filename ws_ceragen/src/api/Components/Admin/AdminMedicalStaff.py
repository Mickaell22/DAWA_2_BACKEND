from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from datetime import datetime
from flask import Flask, jsonify, request
from ....utils.general.response import internal_response

class Medical_staff_Component:
    @staticmethod
    def ListAllMedicalStaff():
        try:
            query = (
                "SELECT med_id, med_person_id, med_type_id, med_registration_number, med_specialty, "
                "med_state, user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, "
                "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, "
                "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted "
                "FROM ceragen.admin_medical_staff WHERE med_state = true"
            )
            res = DataBaseHandle.getRecords(query, 0)
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def GetPersonalStaffById(id):
        try:
            query = "SELECT med_id, med_person_id, med_type_id, med_registration_number, med_specialty, " \
                    "med_state, user_created, to_char(date_created, 'DD/MM/YYYY HH24:MI:SS') as date_created, " \
                    "user_modified, to_char(date_modified, 'DD/MM/YYYY HH24:MI:SS') as date_modified, " \
                    "user_deleted, to_char(date_deleted, 'DD/MM/YYYY HH24:MI:SS') as date_deleted " \
                    "FROM ceragen.admin_medical_staff where med_id = %s"
            record = (id,)
            res = DataBaseHandle.getRecords(query, 1, record)
            return res
        except Exception as err:
            HandleLogs.write_error(err)
            return None

    @staticmethod
    def AddMedicalStaff(data_to_insert):
        try:
            v_message = None
            v_result = False
            v_data = None
            #fk med_person_id : conectada a la tabla admin_person
            #fk med_type_id : 1 es enfermero, 2 es quiropractico
            sql = "INSERT INTO ceragen.admin_medical_staff( med_person_id, med_type_id, " \
                   "med_registration_number, med_specialty, med_state, user_created, date_created) " \
	              "VALUES (%s,%s,%s,%s,%s,%s,%s) "

            record = (data_to_insert['med_person_id'], data_to_insert['med_type_id'],
                      data_to_insert['med_registration_number'], data_to_insert['med_specialty'], True,
                      data_to_insert['user_process'], datetime.now())

            # Execute the UPDATE query
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al agregar un personal medico: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def UpdateMedicalStaff(data_to_update):
        try:
            v_message = None
            v_result = False
            v_data = None
            sql = "UPDATE ceragen.admin_medical_staff " \
                  "SET med_person_id=%s, med_type_id=%s, med_registration_number=%s, med_specialty=%s, " \
                   " user_modified=%s, date_modified=%s " \
                  "WHERE med_id = %s"

            record = (data_to_update['med_person_id'], data_to_update['med_type_id'],
                      data_to_update['med_registration_number'], data_to_update['med_specialty'],
                      data_to_update['user_process'], datetime.now(), data_to_update['med_id'])

            # Execute the UPDATE query
            v_data = DataBaseHandle.ExecuteNonQuery(sql, record)
            if v_data is not None:
                v_result = True

        except Exception as err:
            HandleLogs.write_error(err)
            v_message = "Error al Actualizar el personal medico: " + str(err)
        finally:
            return internal_response(v_result, v_message, v_data)

    @staticmethod
    def LogicalDeleteMedicalStaff(id, p_user):
        try:
            query = "UPDATE ceragen.admin_medical_staff " \
                    "SET med_state = false, user_deleted = %s, date_deleted = %s WHERE med_id = %s"

            record = (p_user, datetime.now(), id)
            res = DataBaseHandle.ExecuteNonQuery(query, record)

            # Verificamos si la operación fue exitosa
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
#CITA FRONT DATOS
    @staticmethod
    def list_full_medical_staff():
        try:
            query = """
                    SELECT
                        ams.med_id,
                        ams.med_person_id,
                        ams.med_type_id,
                        ams.med_registration_number,
                        ams.med_specialty,
                        ams.med_state,
                        per.per_names,
                        per.per_surnames,
                        pergen.genre_name as per_genre,
                        mastatus.status_name as marital_status
                    FROM ceragen.admin_medical_staff ams
                    INNER JOIN ceragen.admin_person per ON ams.med_person_id = per.per_id
                    LEFT JOIN ceragen.admin_person_genre pergen ON per.per_genre_id = pergen.id
                    LEFT JOIN ceragen.admin_marital_status mastatus ON per.per_marital_status_id = mastatus.id
                    WHERE ams.med_state = TRUE AND per.per_state = TRUE
                """
            return DataBaseHandle.getRecords(query, 0)
        except Exception as err:
            HandleLogs.write_error(err)
            return None