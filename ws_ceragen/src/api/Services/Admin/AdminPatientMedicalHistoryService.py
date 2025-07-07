from flask_restful import Resource
from ...Components.Admin.AdminPatientMedicalHistoryComponent import AdminPatientMedicalHistoryComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.PatientMedicalHistoryRequest import PatientMedicalHistoryInsertRequest, PatientMedicalHistoryUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

def serialize_datetime(obj):
    if isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(i) for i in obj]
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj

class AdminPatientMedicalHistoryService_get(Resource):
    @staticmethod
    def get():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPatientMedicalHistoryComponent.list_all_histories()
            print("DEBUG: Resultado de list_all_histories:", res)
            res = serialize_datetime(res)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            print("DEBUG: Error en AdminPatientMedicalHistoryService_get:", err)
            return response_error(str(err))

class AdminPatientMedicalHistoryService_getbyid(Resource):
    @staticmethod
    def get(hist_id):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPatientMedicalHistoryComponent.get_history_by_id(hist_id)
            res = serialize_datetime(res)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            print("DEBUG: Error en AdminPatientMedicalHistoryService_getbyid:", err)
            return response_error(str(err))

class AdminPatientMedicalHistoryService_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            data = request.get_json()
            if not data:
                return response_error("Error en los datos para procesar")
            schema = PatientMedicalHistoryInsertRequest()
            error = schema.validate(data)
            if error:
                return response_error("Error al validar el request -> " + str(error))
            result = AdminPatientMedicalHistoryComponent.add_history(data)
            result = serialize_datetime(result)
            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            print("DEBUG: Error en AdminPatientMedicalHistoryService_add:", err)
            return response_error(str(err))

class AdminPatientMedicalHistoryService_update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            data = request.get_json()
            print("JSON recibido PATCH historial médico:", data)
            if not data:
                return response_error("Error en los datos para procesar")
            schema = PatientMedicalHistoryUpdateRequest()
            error = schema.validate(data)
            print("VALIDACIÓN PATCH historial médico:", error)
            if error:
                return response_error("Error al validar el request -> " + str(error))
            result = AdminPatientMedicalHistoryComponent.update_history(data)
            result = serialize_datetime(result)
            if result['result']:
                return response_success(data)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            print("DEBUG: Error en AdminPatientMedicalHistoryService_update:", err)
            return response_error(str(err))

class AdminPatientMedicalHistoryService_delete(Resource):
    @staticmethod
    def delete(hist_id, user):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_token = TokenComponent.User(token)
            res = AdminPatientMedicalHistoryComponent.delete_history(hist_id, user_token)
            res = serialize_datetime(res)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            print("DEBUG: Error en AdminPatientMedicalHistoryService_delete:", err)
            return response_error(str(err))