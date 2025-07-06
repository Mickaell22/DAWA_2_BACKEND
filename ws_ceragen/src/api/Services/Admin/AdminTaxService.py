from flask_restful import Resource
from ...Components.Admin.AdminTaxComponent import AdminTaxComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
)
from ...Model.Request.Admin.TaxRequest import AdminTaxInsertRequest, AdminTaxUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent


class admin_Tax_service_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de Impuestos")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = AdminTaxComponent.list_all_admin_taxes()
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Tax_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener impuesto por ID: {id}")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = AdminTaxComponent.get_admin_tax_by_id(id)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Tax_service_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("Error en los datos para procesar")

            new_request = AdminTaxInsertRequest()
            error = new_request.validate(data_to_insert)
            if error:
                HandleLogs.write_error("Error al validar el Request -> " + str(error))
                return response_error("Error al validar el Request -> " + str(error))

            result = AdminTaxComponent.add_admin_tax(data_to_insert)

            if result['result']:
                return response_success("ID de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Tax_service_Update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Error en los datos para procesar")

            new_request = AdminTaxUpdateRequest()
            error = new_request.validate(data_to_update)
            if error:
                HandleLogs.write_error("Error al validar el Request -> " + str(error))
                return response_error("Error al validar el Request -> " + str(error))

            result = AdminTaxComponent.update_admin_tax(data_to_update)

            if result['result']:
                if result['data']['data'] == 0:
                    return response_not_found()
                else:
                    return response_success(data_to_update)
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Tax_service_Delete(Resource):
    @staticmethod
    def delete(id):
        try:
            HandleLogs.write_log(f"Eliminar impuesto por ID: {id}")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_token = TokenComponent.User(token)
            res = AdminTaxComponent.logical_delete_admin_tax(id, user_token)

            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
