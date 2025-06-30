from flask_restful import Resource
from ...Components.Admin.AdminPatientComponent import AdminPatientComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.PatientRequest import PatientInsertRequest, PatientUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

def serialize_datetime(obj):
    """
    Convierte cualquier campo datetime en string ISO para evitar errores de serialización JSON.
    """
    if isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(i) for i in obj]
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj

class AdminPatientService_get(Resource):
    @staticmethod
    def get():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPatientComponent.list_all_patients()
            print("DEBUG: Resultado de list_all_patients:", res)
            res = serialize_datetime(res)
            print("DEBUG: Resultado serializado:", res)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            print("DEBUG: Error en AdminPatientService_get:", err)
            return response_error(str(err))

class AdminPatientService_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPatientComponent.get_patient_by_id(id)
            res = serialize_datetime(res)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPatientService_add(Resource):
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
            schema = PatientInsertRequest()
            error = schema.validate(data)
            if error:
                return response_error("Error al validar el request -> " + str(error))
            result = AdminPatientComponent.add_patient(data)
            result = serialize_datetime(result)
            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPatientService_update(Resource):
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
            print("JSON recibido PATCH:", data)
            if not data:
                return response_error("Error en los datos para procesar")
            schema = PatientUpdateRequest()
            error = schema.validate(data)
            print("VALIDACIÓN PATCH:", error)
            if error:
                return response_error("Error al validar el request -> " + str(error))
            result = AdminPatientComponent.update_patient(data)
            result = serialize_datetime(result)
            if result['result']:
                return response_success(data)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPatientService_delete(Resource):
    @staticmethod
    def delete(pat_id, user):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_token = TokenComponent.User(token)
            res = AdminPatientComponent.delete_patient(pat_id, user_token)
            res = serialize_datetime(res)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))