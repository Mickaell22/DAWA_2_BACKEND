import json
from flask_restful import Resource
from ...Components.Admin.AdminInvoiceComponent import Invoice_Component
from ...Components.Admin.AdminInvoiceDetailComponent import Invoice_Detail_Component
from ...Components.Admin.AdminInvoicePaymentComponent import Invoice_Payment_Component
from ...Components.Admin.AdminInvoiceTaxComponent import Invoice_Tax_Component
from ....utils.general.logs import HandleLogs
from flask import jsonify, request
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize
from ...Model.Request.Admin.InvoiceFullRequest import InvoiceFullRequest
from ...Components.Security.TokenComponent import TokenComponent
from decimal import Decimal


def _convert_decimals_to_floats(records):
    if isinstance(records, list):
        return [_convert_decimals_to_floats(r) for r in records]
    elif isinstance(records, dict):
        return {k: _convert_decimals_to_floats(v) for k, v in records.items()}
    elif isinstance(records, Decimal):
        return float(records)
    else:
        return records

def _calculate_unlocked_services(invoice_id):
    try:
        # Obtener el total pagado
        total_pagado = Invoice_Payment_Component.GetTotalPaidAmountByInvoiceId(invoice_id)
        total_pagado = float(total_pagado) if isinstance(total_pagado, Decimal) else 0.0

        # Obtener el total de la factura
        invoice = Invoice_Component.GetInvoiceById(invoice_id)
        if not invoice:
            return []

        invoice_data = invoice[0] if isinstance(invoice, list) else invoice
        total_factura = float(invoice_data.get('inv_grand_total', 0))

        # Lógica simple: desbloquear servicio si se ha pagado al menos un 50%
        if total_pagado >= total_factura * 0.5:
            return [{"service": "Sesión inicial desbloqueada"}]
        else:
            return []

    except Exception as err:
        HandleLogs.write_error(f"Error al calcular servicios desbloqueados: {err}")
        return []



class admin_Invoice_service_get(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de facturas")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = Invoice_Component.ListAllInvoicesByStateTrue()
            if res:
                res = _convert_decimals_to_floats(res)
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener factura por id: {id}")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            invoice = Invoice_Component.GetInvoiceById(id)
            if not invoice:
                return response_not_found()

            invoice_data = invoice[0] if isinstance(invoice, list) else invoice

            details = Invoice_Detail_Component.GetInvoiceDetailsByInvoiceId(id)
            payments = Invoice_Payment_Component.GetInvoicePaymentByInvoiceId(id)
            taxes = Invoice_Tax_Component.GetInvoiceTaxByInvoiceId(id)

            total_pagado = Invoice_Payment_Component.GetTotalPaidAmountByInvoiceId(id)
            total_pagado = float(total_pagado) if isinstance(total_pagado, Decimal) else total_pagado
            total_factura = float(invoice_data['inv_grand_total'])

            invoice_data['total_pagado'] = round(total_pagado, 2)
            invoice_data['pendiente'] = round(total_factura - total_pagado, 2)
            invoice_data['estado_pago'] = "Pagado" if total_pagado >= total_factura else "Pendiente"

            unlocked_services = _calculate_unlocked_services(id)

            full_invoice = {
                "invoice": invoice_data,
                "details": details,
                "payments": payments,
                "taxes": taxes,
                "unlocked_services": unlocked_services
            }

            full_invoice = _convert_decimals_to_floats(full_invoice)
            return response_success(full_invoice)

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_service_add(Resource):
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Agregar factura")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_token = TokenComponent.User(token)
            # Asegurarse de que user_token sea string
            if isinstance(user_token, dict):
                user_token = user_token.get("username") or str(user_token)

            data = request.get_json()
            if not data:
                return response_error("Error en los datos para procesar")

            invoice_req = InvoiceFullRequest()
            errors = invoice_req.validate(data)
            if errors:
                HandleLogs.write_error(f"Error al validar Invoice completo: {errors}")
                return response_error(f"Error al validar Invoice completo: {errors}")

            data["user_process"] = user_token

            # Crear cabecera
            result_invoice = Invoice_Component.AddInvoice(data)
            if not result_invoice['result']:
                return response_error(result_invoice["message"])

            invoice_id = result_invoice['data']
            if isinstance(invoice_id, dict):
                invoice_id = invoice_id.get('data')
            #HandleLogs.write_log(f"Invoice_id: {result_invoice['data'] , invoice_id}")
            #{'result': True, 'message': None, 'data': 7}

            # Insertar detalles
            for d in data.get("details", []):
                ind_invoice_id = invoice_id
                ind_product_id = d.get("ind_product_id")
                ind_quantity = d.get("ind_quantity")
                ind_unit_price = d.get("ind_unit_price")
                ind_total = d.get("ind_total")
                user_process = user_token

                detalle_data = {
                    "ind_invoice_id": ind_invoice_id,
                    "ind_product_id": ind_product_id,
                    "ind_quantity": ind_quantity,
                    "ind_unit_price": ind_unit_price,
                    "ind_total": ind_total,
                    "user_process": user_process
                }

                HandleLogs.write_log(f"Insertando detalle: {detalle_data}")
                Invoice_Detail_Component.AddInvoiceDetail(detalle_data)

            # Insertar pagos
            for p in data.get("payments", []):
                inp_invoice_id = invoice_id
                inp_payment_method_id = p.get("inp_payment_method_id")
                inp_amount = p.get("inp_amount")
                inp_reference = p.get("inp_reference")
                inp_proof_image_path = p.get("inp_proof_image_path")
                user_process = user_token

                pago_data = {
                    "inp_invoice_id": inp_invoice_id,
                    "inp_payment_method_id": inp_payment_method_id,
                    "inp_amount": inp_amount,
                    "inp_reference": inp_reference,
                    "inp_proof_image_path": inp_proof_image_path,
                    "user_process": user_process
                }

                HandleLogs.write_log(f"Insertando pago: {pago_data}")
                Invoice_Payment_Component.AddInvoicePayment(pago_data)

            # Insertar impuestos
            for t in data.get("taxes", []):
                int_invoice_id = invoice_id
                int_tax_id = t.get("int_tax_id") or t.get("tax_id")
                int_tax_amount = t.get("int_tax_amount")
                user_process = user_token

                impuesto_data = {
                    "int_invoice_id": int_invoice_id,
                    "int_tax_id": int_tax_id,
                    "int_tax_amount": int_tax_amount,
                    "user_process": user_process
                }

                HandleLogs.write_log(f"Insertando impuesto: {impuesto_data}")
                Invoice_Tax_Component.AddInvoiceTax(impuesto_data)

            return response_success({"invoice_id": invoice_id})

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_service_Update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_token = TokenComponent.User(token)
            data = request.get_json()
            if not data:
                return response_error("Error en los datos para procesar")

            invoice_req = InvoiceFullRequest()
            errors = invoice_req.validate(data)
            if errors:
                HandleLogs.write_error(f"Error al validar Invoice completo: {errors}")
                return response_error(f"Error al validar Invoice completo: {errors}")

            data["user_process"] = user_token
            result_invoice = Invoice_Component.UpdateInvoice(data)
            if not result_invoice["result"]:
                return response_error(result_invoice["message"])

            invoice_id = data.get("inv_id")

            for d in data.get("details", []):
                d["user_process"] = user_token
                Invoice_Detail_Component.UpdateInvoiceDetail(d)

            for p in data.get("payments", []):
                p["user_process"] = user_token
                Invoice_Payment_Component.UpdateInvoicePayment(p)

            for t in data.get("taxes", []):
                t["user_process"] = user_token
                if "tax_id" in t:
                    t["int_tax_id"] = t.pop("tax_id")
                Invoice_Tax_Component.UpdateInvoiceTax(t)

            return response_success({"invoice_id": invoice_id})
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class admin_Invoice_service_Delete(Resource):
    @staticmethod
    def delete(id):
        try:
            HandleLogs.write_log(f"Eliminar factura por ID: {id}")
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_token = TokenComponent.User(token)

            Invoice_Detail_Component.LogicalDeleteInvoiceDetailsByInvoiceId(id, user_token)
            Invoice_Payment_Component.LogicalDeleteInvoicePaymentByInvoiceId(id, user_token)
            Invoice_Tax_Component.LogicalDeleteInvoiceTaxByInvoiceId(id, user_token)
            res = Invoice_Component.LogicalDeleteInvoice(id, user_token)

            if res:
                return response_success(res)
            else:
                return response_not_found()

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
