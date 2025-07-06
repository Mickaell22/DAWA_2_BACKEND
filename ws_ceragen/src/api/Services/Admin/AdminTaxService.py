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
from ...Model.Request.Admin.TaxRequest import TaxInsertRequest, TaxUpdateRequest, TaxValidation
from ...Components.Security.TokenComponent import TokenComponent


class AdminTaxService(Resource):
    """
    Servicio unificado para gestión de impuestos
    GET /admin/taxes - Listar todos los impuestos
    POST /admin/taxes - Crear nuevo impuesto
    GET /admin/taxes/<id> - Obtener impuesto por ID
    PUT /admin/taxes/<id> - Actualizar impuesto
    DELETE /admin/taxes/<id> - Eliminar impuesto
    """

    def get(self, tax_id=None):
        """GET - Listar todos los impuestos o obtener uno por ID"""
        try:
            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")

            if tax_id is None:
                # Listar todos los impuestos
                HandleLogs.write_log("Listando todos los impuestos")
                res = AdminTaxComponent.list_all_admin_taxes()
                if res is not None:
                    return response_success(res)  # ✅ Solo 1 parámetro
                else:
                    return response_not_found("No se encontraron impuestos")
            else:
                # Obtener impuesto por ID
                HandleLogs.write_log(f"Obteniendo impuesto ID: {tax_id}")

                # Validar ID
                if not TaxValidation.validate_tax_id(tax_id):
                    return response_error("ID de impuesto inválido")

                res = AdminTaxComponent.get_admin_tax_by_id(tax_id)
                if res:
                    return response_success(res)  # ✅ Solo 1 parámetro
                else:
                    return response_not_found("Impuesto no encontrado")

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxService.get: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")

    def post(self):
        """POST - Crear nuevo impuesto"""
        try:
            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")

            HandleLogs.write_log("Creando nuevo impuesto")

            # Obtener y validar datos del request
            data_to_insert = request.get_json()
            if not data_to_insert:
                return response_error("No se recibieron datos")

            # Log de datos recibidos para debug
            HandleLogs.write_log(f"Datos recibidos para crear impuesto: {data_to_insert}")

            # Limpiar datos
            cleaned_data = TaxValidation.clean_tax_data(data_to_insert)
            HandleLogs.write_log(f"Datos limpiados: {cleaned_data}")

            # Validar usando el modelo de request
            validation_result = TaxInsertRequest.validate_tax_insert(cleaned_data)
            if not validation_result["valid"]:
                error_msg = "; ".join(validation_result['errors'])
                HandleLogs.write_error(f"Datos inválidos: {error_msg}")
                return response_error(f"Datos inválidos: {error_msg}")

            # Obtener usuario del token
            user_created = self._get_user_from_token(token)

            # Crear impuesto
            result = AdminTaxComponent.create_admin_tax(cleaned_data, user_created)
            if result:
                response_data = {"tax_id": result}
                HandleLogs.write_log(f"Impuesto creado exitosamente: {response_data}")
                return response_success(response_data)  # ✅ Solo 1 parámetro
            else:
                return response_error("No se pudo crear el impuesto")

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxService.post: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")

    def put(self, tax_id):
        """PUT - Actualizar impuesto existente"""
        try:
            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")

            HandleLogs.write_log(f"Actualizando impuesto ID: {tax_id}")

            # Validar ID
            if not TaxValidation.validate_tax_id(tax_id):
                return response_error("ID de impuesto inválido")

            # Obtener y validar datos del request
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("No se recibieron datos")

            # Log de datos recibidos para debug
            HandleLogs.write_log(f"Datos recibidos para actualizar impuesto {tax_id}: {data_to_update}")

            # Limpiar datos
            cleaned_data = TaxValidation.clean_tax_data(data_to_update)

            # Validar usando el modelo de request
            validation_result = TaxUpdateRequest.validate_tax_update(cleaned_data)
            if not validation_result["valid"]:
                error_msg = "; ".join(validation_result['errors'])
                return response_error(f"Datos inválidos: {error_msg}")

            # Obtener usuario del token
            user_modified = self._get_user_from_token(token)

            # Actualizar impuesto
            result = AdminTaxComponent.update_admin_tax(tax_id, cleaned_data, user_modified)
            if result:
                response_data = {"updated": True}
                return response_success(response_data)  # ✅ Solo 1 parámetro
            else:
                return response_error("No se pudo actualizar el impuesto")

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxService.put: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")

    def delete(self, tax_id):
        """DELETE - Eliminar (desactivar) impuesto"""
        try:
            # Validar token
            token = request.headers.get('tokenapp')
            if not token:
                return response_unauthorize("Token requerido")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize("Token inválido")

            HandleLogs.write_log(f"Eliminando impuesto ID: {tax_id}")

            # Validar ID
            if not TaxValidation.validate_tax_id(tax_id):
                return response_error("ID de impuesto inválido")

            # Obtener usuario del token
            user_deleted = self._get_user_from_token(token)

            # Eliminar impuesto
            result = AdminTaxComponent.delete_admin_tax(tax_id, user_deleted)
            if result:
                response_data = {"deleted": True}
                return response_success(response_data)  # ✅ Solo 1 parámetro
            else:
                return response_error("No se pudo eliminar el impuesto")

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxService.delete: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")

    def _get_user_from_token(self, token):
        """
        Extraer usuario del token
        TODO: Implementar según tu sistema de tokens
        """
        try:
            # Por ahora retorno un valor por defecto
            # Puedes implementar la lógica para extraer el usuario del JWT
            return "system"
        except Exception:
            return "system"