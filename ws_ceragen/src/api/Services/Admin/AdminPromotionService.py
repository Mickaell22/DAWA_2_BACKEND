from flask_restful import Resource
from ...Components.Admin.AdminPromotionComponent import AdminPromotionComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
)
from ...Model.Request.Admin.PromotionRequest import PromotionInsertRequest, PromotionUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

class AdminPromotionService_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de promociones admin")
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize()
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPromotionComponent.list_all_promotions()
            return response_success(res)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPromotionService_getbyid(Resource):
    @staticmethod
    def get(ppr_id):
        try:
            HandleLogs.write_log(f"Obtener promoción admin por ID: {ppr_id}")
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            res = AdminPromotionComponent.get_promotion_by_id(ppr_id)
            if res:
                return response_success(res)
            else:
                return response_not_found("No se encontró la promoción")
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPromotionService_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                print("DEBUG - Token no recibido")
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                print("DEBUG - Token inválido")
                return response_unauthorize("Token inválido")
            data_to_insert = request.get_json()
            print("DEBUG - Datos recibidos en endpoint add:", data_to_insert)
            if not data_to_insert:
                return response_error("Datos requeridos")
            new_request = PromotionInsertRequest()
            error = new_request.validate(data_to_insert)
            print("DEBUG - Resultado validación:", error)
            if error:
                return response_error(error)
            result = AdminPromotionComponent.add_promotion(data_to_insert)
            print("DEBUG - Resultado add_promotion:", result)
            if result['result']:
                return response_success(result)
            else:
                return response_error(result['message'])
        except Exception as err:
            import traceback
            print("DEBUG - Error en AdminPromotionService_add.post:", err)
            traceback.print_exc()
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPromotionService_update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Datos requeridos")
            new_request = PromotionUpdateRequest()
            error = new_request.validate(data_to_update)
            if error:
                return response_error(error)
            result = AdminPromotionComponent.update_promotion(data_to_update)
            if result['result']:
                return response_success(result)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminPromotionService_delete(Resource):
    @staticmethod
    def delete(ppr_id, user):
        try:
            HandleLogs.write_log(f"Eliminar promoción por ID: {ppr_id}")
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            user_token = TokenComponent.User(token)
            res = AdminPromotionComponent.delete_promotion(ppr_id, user_token)
            return response_success(res)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))