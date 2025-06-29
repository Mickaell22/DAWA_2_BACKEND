from ....utils.general.logs import HandleLogs
from flask_restful import Resource
from ....utils.general.response import response_success, response_not_found, response_error, response_unauthorize, \
    response_inserted, response_success_personal
from ....api.Components.Security.UserComponent import UserComponent
from ....api.Components.Security.TokenComponent import TokenComponent
from flask import request
from ....api.Model.Request.Security.InsertUser import InsertUserSchema
from ....api.Model.Request.Security.DeleteService import DeleteServiceSchema
from ....api.Model.Request.Security.UpdateUser import UpdateUserSchema
from ....api.Model.Request.Security.UpdateUserPassword import UpdateUserPasswordSchema
from ....api.Model.Request.Security.RecoveringPassword import RecoveringPasswordSchema, UpdatePasswordSchema


class UserService(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de Usuarios")
            # Obtengo el token
            token = request.headers['tokenapp']
            client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # LLamar al metodo del componente
            resultado = UserComponent.ListAllUsers()
            if resultado:
                return response_success(resultado['data'])
            else:
                return response_error(resultado['message'])
        except Exception as err:
            HandleLogs.write_error(err)


class UserInsert(Resource):
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Insertar Usuario")
            token = request.headers['tokenapp']
            rq_json = request.get_json()
            new_request = InsertUserSchema()
            error = new_request.validate(rq_json)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            # LLamar al metodo del componente
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_name = TokenComponent.User(token)
            # LLamar al metodo del componente
            answer = UserComponent.UserInsert(rq_json['person_id'], rq_json['person_ci'], rq_json['person_password'],
                                              rq_json['person_mail'], user_name, rq_json['rol_id'],
                                              rq_json['id_career_period'])
            if answer['result'] is True:
                return response_inserted(answer['data'])
            else:
                return response_error(answer['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())


class UserDelete(Resource):
    @staticmethod
    def patch():
        try:
            HandleLogs.write_log("Eliminar User")
            token = request.headers['tokenapp']
            rq_json = request.get_json()
            new_request = DeleteServiceSchema()
            error = new_request.validate(rq_json)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            # LLamar al metodo del componente
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_name = TokenComponent.User(token)
            # LLamar al metodo del componente
            answer = UserComponent.UserDelete(user_name, rq_json['del_id'])
            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())


class UserUpdate(Resource):
    @staticmethod
    def patch():
        try:
            HandleLogs.write_log("Actualizar User")
            token = request.headers['tokenapp']
            rq_json = request.get_json()

            # 🔧 LOG ADICIONAL PARA DEBUGGING
            HandleLogs.write_log(f"Datos recibidos para actualización: {rq_json}")

            new_request = UpdateUserSchema()
            error = new_request.validate(rq_json)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            # LLamar al metodo del componente
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_name = TokenComponent.User(token)

            # 🔧 LLAMADA CORREGIDA: Pasar todos los datos del formulario
            answer = UserComponent.UserUpdate(
                user_name=user_name,
                user_id=rq_json['id_user'],
                person_ci=rq_json.get('person_ci'),
                person_mail=rq_json.get('person_mail'),
                person_password=rq_json.get('person_password'),
                rol_id=rq_json.get('rol_id'),
                person_id=rq_json.get('person_id')
            )

            HandleLogs.write_log(f"Resultado de UserUpdate: {answer}")

            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])
        except Exception as err:
            HandleLogs.write_error(f"Error en UserUpdate: {err}")
            return response_error(err.__str__())


class UserpasswordUpdate(Resource):
    @staticmethod
    def patch():
        try:
            HandleLogs.write_log("Actualizar Password")
            token = request.headers['tokenapp']
            rq_json = request.get_json()
            new_request = UpdateUserPasswordSchema()
            error = new_request.validate(rq_json)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            # LLamar al metodo del componente
            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            user_name = TokenComponent.User(token)
            # LLamar al metodo del componente
            answer = UserComponent.UserpasswordUpdate(user_name, rq_json['id_user'], rq_json['id_password'])
            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())


class RecoveringPassword(Resource):
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Recuperar Password")
            rq_json = request.get_json()
            new_request = RecoveringPasswordSchema()
            error = new_request.validate(rq_json)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            # LLamar al metodo del componente
            answer = UserComponent.RecoverPassword(rq_json['user_mail'])
            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())


class EmailPasswordUpdate(Resource):
    @staticmethod
    def patch():
        try:
            HandleLogs.write_log("Actualizar Password por Email")
            rq_json = request.get_json()
            new_request = UpdatePasswordSchema()
            error = new_request.validate(rq_json)
            if error:
                HandleLogs.write_error("Error al Validar el Request -> " + str(error))
                return response_error("Error al Validar el Request -> " + str(error))
            # LLamar al metodo del componente
            answer = UserComponent.EmailPasswordUpdate(rq_json['user_mail'], rq_json['user_password'])
            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())


class UserListId(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Buscar ID de Usuario")
            # Obtengo el token
            token = request.headers['tokenapp']

            if token is None:
                return response_error("Error: No se ha podido Obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            user_name = TokenComponent.User(token)
            # LLamar al metodo del componente
            resultado = UserComponent.ListUserId(user_name)
            if resultado['result']:
                return response_success_personal(resultado['data'])
            else:
                return response_error(resultado['message'])
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())