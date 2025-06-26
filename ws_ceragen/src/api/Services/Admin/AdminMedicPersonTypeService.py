import json
from flask_restful import Resource
from ...Components.Admin.AdminMedicPersonType import MedicPersonType_Component
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
)
from ...Model.Request.Admin.MedicPersonTypeRequest import (
    MedicPersonTypeInsertRequest,
    MedicPersonTypeUpdateRequest,
)
from ...Components.Security.TokenComponent import TokenComponent

class admin_MedicPersonType_service_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de Tipos de Personal Médico")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            res = MedicPersonType_Component.ListAllMedicPersonType()
            return response_success(res) if res else response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_MedicPersonType_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener tipo de personal médico por ID: {id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            res = MedicPersonType_Component.GetByIdMedicPersonType(id)
            return response_success(res) if res else response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_MedicPersonType_service_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            data = request.get_json()
            if not data:
                return response_error("Datos vacíos o inválidos")
            schema = MedicPersonTypeInsertRequest()
            errors = schema.validate(data)
            if errors:
                return response_error("Error al validar datos: " + str(errors))
            result = MedicPersonType_Component.AddMedicPersonType(data)
            return response_success("ID de registro -> " + str(result['data'])) if result['result'] else response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_MedicPersonType_service_Update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            data = request.get_json()
            if not data:
                return response_error("Datos vacíos o inválidos")
            schema = MedicPersonTypeUpdateRequest()
            errors = schema.validate(data)
            if errors:
                return response_error("Error al validar datos: " + str(errors))
            result = MedicPersonType_Component.UpdateMedicPersonType(data)
            if result['result']:
                if result['data']['data'] == 0:
                    return response_not_found()
                return response_success(data)
            return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_MedicPersonType_service_Delete(Resource):
    @staticmethod
    def delete(id, user):
        try:
            HandleLogs.write_log(f"Eliminar tipo de personal médico ID: {id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            user_token = TokenComponent.User(token)
            success, msg = MedicPersonType_Component.LogicalDeleteMedicPersonType(id, user_token)
            return response_success(msg) if success else response_error(msg)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
