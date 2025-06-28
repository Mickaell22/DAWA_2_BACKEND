from flask_restful import Resource
from ...Components.Admin.AdminProductComponent import AdminProductComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
)
from ...Model.Request.Admin.ProductRequest import ProductInsertRequest, ProductUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

class AdminProductService_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de productos admin")
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize()
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminProductComponent.list_all_admin_products()
            return response_success(res)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminProductService_getbyid(Resource):
    @staticmethod
    def get(pro_id):
        try:
            HandleLogs.write_log(f"Obtener producto admin por ID: {pro_id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            res = AdminProductComponent.get_admin_product_by_id(pro_id)
            if res:
                return response_success(res)
            else:
                return response_not_found("No se encontró el producto")
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminProductService_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("Datos requeridos")
            new_request = ProductInsertRequest()
            error = new_request.validate(data_to_insert)
            if error:
                return response_error(error)
            result = AdminProductComponent.add_admin_product(data_to_insert)
            if result['result']:
                return response_success(result)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminProductService_update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Datos requeridos")
            new_request = ProductUpdateRequest()
            error = new_request.validate(data_to_update)
            if error:
                return response_error(error)
            result = AdminProductComponent.update_admin_product(data_to_update)
            if result['result']:
                return response_success(result)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

class AdminProductService_delete(Resource):
    @staticmethod
    def delete(pro_id, user):
        try:
            HandleLogs.write_log(f"Eliminar producto por ID: {pro_id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_unauthorize("Token requerido")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")
            user_token = TokenComponent.User(token)
            res = AdminProductComponent.delete_admin_product(pro_id, user_token)
            return response_success(res)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())