import json
from flask_restful import Resource
from ...Components.Admin.AdminInvoicePaymentComponent import Invoice_Payment_Component
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.InvoicePaymentRequest import InvoicePaymentInsertRequest, InvoicePaymentUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent


class admin_Invoice_payment_service_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de pagos de facturas")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            res = Invoice_Payment_Component.ListAllInvoicesPayments()
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_payment_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener pago de factura por id: {id}")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            res = Invoice_Payment_Component.GetInvoicePaymentById(id)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_payment_service_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            data = request.get_json()
            if not data:
                return response_error("Error en los datos para procesar")

            req = InvoicePaymentInsertRequest()
            error = req.validate(data)
            if error:
                HandleLogs.write_error("Error al validar el request -> " + str(error))
                return response_error("Error al validar el request -> " + str(error))

            result = Invoice_Payment_Component.AddInvoicePayment(data)
            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_payment_service_Update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()
            data = request.get_json()
            if not data:
                return response_error("Error en los datos para procesar")

            req = InvoicePaymentUpdateRequest()
            error = req.validate(data)
            if error:
                HandleLogs.write_error("Error al validar el request -> " + str(error))
                return response_error("Error al validar el request -> " + str(error))

            result = Invoice_Payment_Component.UpdateInvoicePayment(data)
            if result['result']:
                if result['data']['data'] == 0:
                    return response_not_found()
                else:
                    return response_success(data)
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_payment_service_Delete(Resource):
    @staticmethod
    def delete(id):
        try:
            HandleLogs.write_log(f"Eliminar pago de factura por ID: {id}")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_token = TokenComponent.User(token)
            res, msg = Invoice_Payment_Component.LogicalDeleteInvoicePayment(id, user_token)
            if res:
                return response_success(msg)
            else:
                return response_error(msg)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
