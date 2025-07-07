from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from ...Components.Admin.AdminTaxComponent import AdminTaxComponent
from ...Components.Security.TokenComponent import TokenComponent
from ....utils.general.logs import HandleLogs
from ....utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
)
from ...Model.Request.Admin.TaxRequest import (
    admin_tax_insert_schema,
    admin_tax_update_schema,
    admin_tax_delete_schema,
    admin_tax_response_schema,
    admin_tax_list_response_schema
)


class AdminTaxServiceGet(Resource):
    """Servicio para obtener lista de todos los impuestos"""
    
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listando todos los impuestos")
            
            # Validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Obtener lista de impuestos
            taxes = AdminTaxComponent.list_all_admin_taxes()
            
            if taxes:
                # Serializar respuesta
                result = admin_tax_list_response_schema.dump(taxes)
                return response_success(result)
            else:
                return response_success([])  # Lista vacía en lugar de not_found
                
        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxServiceGet: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")


class AdminTaxServiceGetById(Resource):
    """Servicio para obtener un impuesto por ID"""
    
    @staticmethod
    def get(tax_id):
        try:
            HandleLogs.write_log(f"Obteniendo impuesto por ID: {tax_id}")
            
            # Validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Validar ID
            if not isinstance(tax_id, int) or tax_id <= 0:
                return response_error("ID de impuesto inválido")

            # Obtener impuesto
            tax = AdminTaxComponent.get_admin_tax_by_id(tax_id)
            
            if tax:
                # Serializar respuesta
                result = admin_tax_response_schema.dump(tax)
                return response_success(result)
            else:
                return response_not_found(f"Impuesto con ID {tax_id} no encontrado")
                
        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxServiceGetById: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")


class AdminTaxServiceAdd(Resource):
    """Servicio para crear un nuevo impuesto"""
    
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Creando nuevo impuesto")
            
            # Validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Obtener datos JSON
            json_data = request.get_json()
            if not json_data:
                return response_error("No se han enviado datos para procesar")

            # Validar datos con Marshmallow
            try:
                validated_data = admin_tax_insert_schema.load(json_data)
            except ValidationError as err:
                HandleLogs.write_error(f"Error de validación: {err.messages}")
                return response_error("Errores de validación", err.messages)

            # Crear impuesto
            result = AdminTaxComponent.add_admin_tax(validated_data)

            if result['result']:
                # Obtener el impuesto creado para retornarlo
                if result['data'] and 'data' in result['data']:
                    new_tax_id = result['data']['data']
                    created_tax = AdminTaxComponent.get_admin_tax_by_id(new_tax_id)
                    if created_tax:
                        serialized_tax = admin_tax_response_schema.dump(created_tax)
                        return response_success(serialized_tax, "Impuesto creado exitosamente")
                
                return response_success(
                    {"tax_id": result['data']}, 
                    "Impuesto creado exitosamente"
                )
            else:
                return response_error(result['message'] or "Error al crear el impuesto")

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxServiceAdd: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")


class AdminTaxServiceUpdate(Resource):
    """Servicio para actualizar un impuesto existente"""
    
    @staticmethod
    def put(tax_id):
        try:
            HandleLogs.write_log(f"Actualizando impuesto ID: {tax_id}")
            
            # Validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Obtener datos JSON
            json_data = request.get_json()
            if not json_data:
                return response_error("No se han enviado datos para procesar")

            # Agregar tax_id a los datos
            json_data['tax_id'] = tax_id

            # Validar datos con Marshmallow
            try:
                validated_data = admin_tax_update_schema.load(json_data)
            except ValidationError as err:
                HandleLogs.write_error(f"Error de validación: {err.messages}")
                return response_error("Errores de validación", err.messages)

            # Verificar que el impuesto existe antes de actualizar
            existing_tax = AdminTaxComponent.get_admin_tax_by_id(tax_id)
            if not existing_tax:
                return response_not_found(f"Impuesto con ID {tax_id} no encontrado")

            # Actualizar impuesto
            result = AdminTaxComponent.update_admin_tax(validated_data)

            if result['result']:
                # Obtener el impuesto actualizado
                updated_tax = AdminTaxComponent.get_admin_tax_by_id(tax_id)
                if updated_tax:
                    serialized_tax = admin_tax_response_schema.dump(updated_tax)
                    return response_success(serialized_tax, "Impuesto actualizado exitosamente")
                else:
                    return response_success(validated_data, "Impuesto actualizado exitosamente")
            else:
                return response_error(result['message'] or "Error al actualizar el impuesto")

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxServiceUpdate: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")

    @staticmethod
    def patch(tax_id):
        """Método PATCH para actualizaciones parciales (redirige a PUT)"""
        return AdminTaxServiceUpdate.put(tax_id)


class AdminTaxServiceDelete(Resource):
    """Servicio para eliminar (desactivar) un impuesto"""
    
    @staticmethod
    def delete(tax_id):
        try:
            HandleLogs.write_log(f"Eliminando impuesto ID: {tax_id}")
            
            # Validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Obtener usuario del token
            user_token = TokenComponent.User(token)
            if not user_token:
                return response_error("No se pudo obtener el usuario del token")

            # Validar ID
            if not isinstance(tax_id, int) or tax_id <= 0:
                return response_error("ID de impuesto inválido")

            # Verificar que el impuesto existe
            existing_tax = AdminTaxComponent.get_admin_tax_by_id(tax_id)
            if not existing_tax:
                return response_not_found(f"Impuesto con ID {tax_id} no encontrado")

            # Verificar si se puede eliminar
            usage_info = AdminTaxComponent.get_tax_usage_info(tax_id)
            if not usage_info["can_delete"]:
                return response_error(usage_info["reason"])

            # Eliminar impuesto
            success, message = AdminTaxComponent.logical_delete_admin_tax(tax_id, user_token)

            if success:
                return response_success(
                    {"tax_id": tax_id, "deleted": True}, 
                    message
                )
            else:
                return response_error(message)

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxServiceDelete: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")


class AdminTaxServiceCheck(Resource):
    """Servicio para verificar si un impuesto se puede eliminar"""
    
    @staticmethod
    def get(tax_id):
        try:
            HandleLogs.write_log(f"Verificando si se puede eliminar impuesto ID: {tax_id}")
            
            # Validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Validar ID
            if not isinstance(tax_id, int) or tax_id <= 0:
                return response_error("ID de impuesto inválido")

            # Verificar que el impuesto existe
            existing_tax = AdminTaxComponent.get_admin_tax_by_id(tax_id)
            if not existing_tax:
                return response_not_found(f"Impuesto con ID {tax_id} no encontrado")

            # Obtener información de uso
            usage_info = AdminTaxComponent.get_tax_usage_info(tax_id)
            
            return response_success(usage_info)

        except Exception as err:
            HandleLogs.write_error(f"Error en AdminTaxServiceCheck: {err}")
            return response_error(f"Error interno del servidor: {str(err)}")


# Clases adicionales para mantener compatibilidad con nombres anteriores
class admin_Tax_service_get(AdminTaxServiceGet):
    """Clase de compatibilidad - usar AdminTaxServiceGet"""
    pass

class admin_Tax_getbyid(AdminTaxServiceGetById):
    """Clase de compatibilidad - usar AdminTaxServiceGetById"""
    pass

class admin_Tax_service_add(AdminTaxServiceAdd):
    """Clase de compatibilidad - usar AdminTaxServiceAdd"""
    pass

class admin_Tax_service_Update(AdminTaxServiceUpdate):
    """Clase de compatibilidad - usar AdminTaxServiceUpdate"""
    pass

class admin_Tax_service_Delete(AdminTaxServiceDelete):
    """Clase de compatibilidad - usar AdminTaxServiceDelete"""
    pass