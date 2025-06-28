from flask_restful import Resource
from ...Components.Admin.AdminTherapyComponent import AdminTherapyComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
)
from ...Model.Request.Admin.TherapyRequest import TherapyInsertRequest, TherapyUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

class AdminTherapyService_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de terapias admin")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminTherapyComponent.list_all_admin_therapies()
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminTherapyService_getbyid(Resource):
    @staticmethod
    def get(tht_id):
        try:
            HandleLogs.write_log(f"Obtener terapia admin por ID: {tht_id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminTherapyComponent.get_admin_therapy_by_id(tht_id)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminTherapyService_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("Error en los datos para procesar")
            new_request = TherapyInsertRequest()
            error = new_request.validate(data_to_insert)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            result = AdminTherapyComponent.add_admin_therapy(data_to_insert)
            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminTherapyService_update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Error en los datos para procesar")
            new_request = TherapyUpdateRequest()
            error = new_request.validate(data_to_update)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            result = AdminTherapyComponent.update_admin_therapy(data_to_update)
            HandleLogs.write_log(result)
            if result['result']:
                # Asegúrate de que result['data'] sea un dict o int según tu lógica
                if isinstance(result['data'], dict):
                    if result['data'].get('data', 0) < 0:
                        return response_error("Ocurrió un error al actualizar el registro")
                    elif result['data'].get('data', 0) == 0:
                        return response_not_found()
                    else:
                        return response_success(data_to_update)
                elif isinstance(result['data'], int):
                    if result['data'] < 0:
                        return response_error("Ocurrió un error al actualizar el registro")
                    elif result['data'] == 0:
                        return response_not_found()
                    else:
                        return response_success(data_to_update)
                else:
                    return response_success(data_to_update)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminTherapyService_delete(Resource):
    @staticmethod
    def delete(tht_id, user):
        try:
            HandleLogs.write_log(f"Eliminar terapia por ID: {tht_id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_token = TokenComponent.User(token)
            res = AdminTherapyComponent.delete_admin_therapy(tht_id, user_token)
            HandleLogs.write_log(f"Filas afectadas: {res}")
            # Validación robusta para dict
            if isinstance(res, dict) and res.get('result') is True and res.get('data', 0) > 0:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())