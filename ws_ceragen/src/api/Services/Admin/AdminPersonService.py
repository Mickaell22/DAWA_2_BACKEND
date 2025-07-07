from flask_restful import Resource
from ...Components.Admin.AdminPersonComponent import AdminPersonComponent
from ....utils.general.logs import HandleLogs
from flask import jsonify, request
from ....utils.general.response import response_success,response_not_found,response_error, response_unauthorize
from ...Model.Request.Admin.PersonRequest import PersonInsertRequest, PersonUpdateRequest
from ...Components.Security.TokenComponent import TokenComponent

class AdminPersonService_get(Resource):
    #obtener
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de personas admin")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPersonComponent.list_all_admin_persons()
            if res:
                return response_success(res)
            else:
                return response_not_found() #devuelve mensaje de error
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

    #obtener
class AdminPersonService_getbyid(Resource):
    @staticmethod
    def get(id):
        try:
            HandleLogs.write_log(f"Obtener persona admin por ID: {id}")
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            res = AdminPersonComponent.get_admin_person_by_id(id)
            if res:
                return response_success(res)
            else:
                return response_not_found()
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

    #crear
class admin_Person_service_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            # Get data from request body
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Error en loda datos para procesar")
            # Validar ese Request con mi modelo
            new_request = PersonInsertRequest()
            error = new_request.validate(data_to_update)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))

            # Update the academy unit
            result = AdminPersonComponent.add_admin_person(data_to_update)

            if result['result']:
                return response_success("Id de Registro -> " + str(result['data']))
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

    #actualizar
class admin_Person_service_Update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            # Get data from request body
            data_to_update = request.get_json()
            if not data_to_update:
                return response_error("Error en loda datos para procesar")
            # Validar ese Request con mi modelo
            new_request = PersonUpdateRequest()
            error = new_request.validate(data_to_update)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))

            # Update the academy unit
            result = AdminPersonComponent.update_admin_person(data_to_update)
            HandleLogs.write_log(result)

            if result['result']:
                if result['data']['data'] < 0:
                    return response_error("Ocurrió un error al actualizar el registro")
                else:
                    if result['data']['data'] == 0:
                        return response_not_found()
                    else:
                        return response_success(data_to_update)
            else:
                return response_error(result['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())

    #eliminar


class admin_person_service_Delete(Resource):
    @staticmethod
    def delete(per_id, user):
        try:
            HandleLogs.write_log(f"🗑️ Eliminando persona con ID: {per_id}")

            # 🔐 Validar token
            token = request.headers['tokenapp']
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # 🔍 Obtener usuario del token
            user_token = TokenComponent.User(token)
            HandleLogs.write_log(f"Usuario que elimina: {user_token}")

            # 🗑️ Llamar al componente para eliminar
            success, message = AdminPersonComponent.delete_admin_person(per_id, user_token)
            HandleLogs.write_log(f"Resultado eliminación: success={success}, message={message}")

            if success:
                return response_success({"message": message, "per_id": per_id})
            else:
                return response_not_found()

        except Exception as err:
            HandleLogs.write_error(f"❌ Error en eliminación de persona: {err}")
            return response_error(str(err))

class AdminPersonService_statistics(Resource):
    @staticmethod
    def get():
        try:
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            stats = AdminPersonComponent.get_person_statistics()
            print("TYPE OF stats:", type(stats), stats)
            print(type(stats), stats)
            print("DEBUG STATS TYPE:", type(stats), stats)
            if stats:
                return response_success(stats)
            else:
                return response_error("No se pudieron calcular las estadísticas")
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))