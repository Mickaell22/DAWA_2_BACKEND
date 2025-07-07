import json
from flask_restful import Resource
from ...Components.Admin.AdminPaymentMethodComponent import PaymentMethodComponent
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.PaymentMethodRequest import PaymentMethodInsertRequest, PaymentMethodUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

class admin_PaymentMethod_service_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de Métodos de Pago")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            res = PaymentMethodComponent.list_all_payment_methods()
            if res:
                return response_success(res)
            return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_PaymentMethod_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener método de pago por id: {id}")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            res = PaymentMethodComponent.get_payment_method_by_id(id)
            if res:
                return response_success(res)
            return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_PaymentMethod_service_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("Error en los datos para procesar")

            new_request = PaymentMethodInsertRequest()
            error = new_request.validate(data_to_insert)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))

            result = PaymentMethodComponent.add_payment_method(data_to_insert)
            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_PaymentMethod_service_Update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Error en los datos para procesar")

            new_request = PaymentMethodUpdateRequest()
            error = new_request.validate(data_to_update)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))

            result = PaymentMethodComponent.update_payment_method(data_to_update)
            HandleLogs.write_log(result)

            if result['result']:
                if result['data']['data'] < 0:
                    return response_error("Ocurrió un error al actualizar el registro")
                elif result['data']['data'] == 0:
                    return response_not_found()
                else:
                    return response_success(data_to_update)
            return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_PaymentMethod_service_Delete(Resource):
    @staticmethod
    def delete(id):
        try:
            HandleLogs.write_log(f"Eliminar método de pago por ID: {id}")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            user_token = TokenComponent.User(token)
            res = PaymentMethodComponent.logical_delete_payment_method(id, user_token)
            if res:
                return response_success(res)
            return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
