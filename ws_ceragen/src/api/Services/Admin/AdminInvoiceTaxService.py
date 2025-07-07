import json
from flask_restful import Resource
from ...Components.Admin.AdminInvoiceTaxComponent import Invoice_Tax_Component
from ....utils.general.logs import HandleLogs
from flask import request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.InvoiceTaxRequest import InvoiceTaxInsertRequest, InvoiceTaxUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

class admin_Invoice_tax_service_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de impuestos de factura")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = Invoice_Tax_Component.ListAllInvoicesTaxesByStateTrue()
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_Invoice_tax_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener impuesto de factura por id: {id}")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = Invoice_Tax_Component.GetInvoiceTaxById(id)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_Invoice_tax_service_add(Resource):
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

            req = InvoiceTaxInsertRequest()
            error = req.validate(data)
            if error:
                HandleLogs.write_error("Error al validar el request -> " + str(error))
                return response_error("Error al validar el request -> " + str(error))

            result = Invoice_Tax_Component.AddInvoiceTax(data)
            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class admin_Invoice_tax_service_Update(Resource):
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

            req = InvoiceTaxUpdateRequest()
            error = req.validate(data)
            if error:
                HandleLogs.write_error("Error al validar el request -> " + str(error))
                return response_error("Error al validar el request -> " + str(error))

            result = Invoice_Tax_Component.UpdateInvoiceTax(data)
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

class admin_Invoice_tax_service_Delete(Resource):
    @staticmethod
    def delete(id):
        try:
            HandleLogs.write_log(f"Eliminar impuesto de factura por ID: {id}")
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_token = TokenComponent.User(token)
            res = Invoice_Tax_Component.LogicalDeleteInvoiceTax(id, user_token)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
