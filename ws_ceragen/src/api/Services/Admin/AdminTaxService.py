from flask_restful import Resource
from flask import request
from marshmallow import ValidationError
from src.api.Components.Admin.AdminTaxComponent import AdminTaxComponent
from src.api.Components.Security.TokenComponent import TokenComponent
from src.utils.general.logs import HandleLogs
from src.utils.general.response import (
    response_success,
    response_not_found,
    response_error,
    response_unauthorize,
    response_inserted,
    response_success_personal # Importamos esta para respuestas con datos y mensaje
)
from src.api.Model.Request.Admin.TaxRequest import (
    admin_tax_insert_schema,
    admin_tax_update_schema,
    admin_tax_delete_schema,
    admin_tax_response_schema,
    admin_tax_list_response_schema
)
from src.api.Model.Admin.AdminTaxModel import AdminTaxModel


class AdminTaxServiceGet(Resource):
    @staticmethod
    def get():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token no proporcionado", status_code=400)
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = AdminTaxComponent.list_all_admin_taxes()
            if res['result']:
                serialized_data = admin_tax_list_response_schema.dump(res['data'])
                return response_success(serialized_data)
            else:
                return response_error(res['message'])
        except Exception as e:
            HandleLogs.write_error(f"Error en AdminTaxServiceGet: {e}")
            return response_error("Error interno al obtener la lista de impuestos.")


class AdminTaxServiceGetById(Resource):
    @staticmethod
    def get(tax_id):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token no proporcionado", status_code=400)
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            res = AdminTaxComponent.get_admin_tax_by_id(tax_id)
            if res['result']:
                if res['data']:
                    serialized_data = admin_tax_response_schema.dump(res['data'])
                    return response_success(serialized_data)
                else:
                    return response_not_found(res['message'])
            else:
                return response_error(res['message'])
        except Exception as e:
            HandleLogs.write_error(f"Error en AdminTaxServiceGetById: {e}")
            return response_error("Error interno al obtener el impuesto por ID.")


class AdminTaxServiceAdd(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token no proporcionado", status_code=400)
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            json_data = request.get_json()
            if not json_data:
                return response_error("Datos JSON no proporcionados", status_code=400)

            validated_data = admin_tax_insert_schema.load(json_data)

            res = AdminTaxComponent.insert_admin_tax(validated_data)
            if res['result']:
                return response_inserted(res['data'])
            else:
                return response_error(res['message'])
        except ValidationError as err:
            HandleLogs.write_error(f"Error de validación en AdminTaxServiceAdd: {err.messages}")
            return response_error(f"Error de validación: {err.messages}", status_code=400)
        except Exception as e:
            HandleLogs.write_error(f"Error en AdminTaxServiceAdd: {e}")
            return response_error("Error interno al agregar impuesto.")


class AdminTaxServiceUpdate(Resource):
    @staticmethod
    def put(tax_id): # <--- CORREGIDO: AHORA ESPERA tax_id COMO ARGUMENTO DE LA URL
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token no proporcionado", status_code=400)
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            json_data = request.get_json()
            if not json_data:
                return response_error("Datos JSON no proporcionados", status_code=400)

            # Aseguramos que el tax_id de la URL esté en los datos para la validación y el componente
            # Esto es crucial porque el esquema de actualización espera 'tax_id' en los datos
            json_data['tax_id'] = tax_id

            try:
                validated_data = admin_tax_update_schema.load(json_data)
            except ValidationError as err:
                HandleLogs.write_error(f"Error de validación en AdminTaxServiceUpdate: {err.messages}")
                return response_error(f"Error de validación: {err.messages}", status_code=400)

            res = AdminTaxComponent.update_admin_tax(validated_data)
            if res['result']:
                # Obtenemos el impuesto actualizado para devolverlo en la respuesta
                updated_tax = AdminTaxComponent.get_admin_tax_by_id(tax_id)
                serialized_tax = admin_tax_response_schema.dump(updated_tax)
                # Usamos response_success_personal para devolver datos y mensaje
                return response_success_personal(True, "Impuesto actualizado exitosamente", serialized_tax)
            elif res['message'].startswith("El impuesto con ID"):
                return response_not_found(res['message'])
            else:
                return response_error(res['message'])
        except Exception as e:
            HandleLogs.write_error(f"Error en AdminTaxServiceUpdate: {e}")
            return response_error("Error interno al actualizar impuesto.")

    @staticmethod
    def patch(tax_id): # <--- CORREGIDO: AHORA ESPERA tax_id COMO ARGUMENTO DE LA URL
        # Redirige al método put, pasándole el tax_id que recibe de la URL
        return AdminTaxServiceUpdate.put(tax_id)


class AdminTaxServiceDelete(Resource):
    @staticmethod
    def delete(tax_id):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token no proporcionado", status_code=400)
            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # tax_id ya está disponible como argumento de la URL

            json_data = request.get_json()
            if not json_data or 'user_process' not in json_data:
                return response_error("El campo 'user_process' es requerido en el cuerpo de la petición.",
                                      status_code=400)

            # Cargamos los datos para validación, incluyendo el tax_id de la URL y user_process del JSON
            validated_data = admin_tax_delete_schema.load({'tax_id': tax_id, 'user_process': json_data['user_process']})
            user_process = validated_data['user_process']

            res = AdminTaxComponent.delete_admin_tax(tax_id, user_process)
            if res['result']:
                # Usamos response_success_personal para incluir datos y mensaje
                return response_success_personal(True, res['message'], {"tax_id": tax_id})
            elif res['message'].startswith("El impuesto con ID"):
                return response_not_found(res['message'])
            else:
                return response_error(res['message'])
        except ValidationError as err:
            HandleLogs.write_error(f"Error de validación en AdminTaxServiceDelete: {err.messages}")
            return response_error(f"Error de validación: {err.messages}", status_code=400)
        except Exception as e:
            HandleLogs.write_error(f"Error en AdminTaxServiceDelete: {e}")
            return response_error("Error interno al eliminar impuesto.")


# Clases de compatibilidad
class admin_Tax_service_get(AdminTaxServiceGet): pass
class admin_Tax_getbyid(AdminTaxServiceGetById): pass
class admin_Tax_service_add(AdminTaxServiceAdd): pass
class admin_Tax_service_Update(AdminTaxServiceUpdate): pass
class admin_Tax_service_Delete(AdminTaxServiceDelete): pass