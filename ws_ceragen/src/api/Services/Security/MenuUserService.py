from flask import request
from flask_restful import Resource
from ....utils.general.logs import HandleLogs
from ....utils.general.response import response_success, response_error, response_unauthorize
from ....api.Components.Security.TokenComponent import TokenComponent
from ....api.Components.Security.ComponentMenu import ComponentMenu
from ....utils.database.connection_db import DataBaseHandle


class MenuUserService(Resource):
    @staticmethod
    def get(user_id):
        try:
            HandleLogs.write_log(f"Listado de Menús para Usuario ID: {user_id}")

            # Obtener y validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Verificar que el usuario tenga roles asignados
            role_check = DataBaseHandle.getRecords(
                "SELECT COUNT(*) as role_count FROM ceragen.segu_user_rol WHERE id_user = %s",
                1, (user_id,)
            )

            if not role_check.get('result') or role_check['data']['role_count'] == 0:
                return response_success([])  # Usuario sin roles, retornar array vacío

            # Llamar al método del componente
            answer = ComponentMenu.MenuListByUser(user_id)

            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())


class MenuCurrentUserService(Resource):
    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Listado de Menús para Usuario Actual")

            # Obtener y validar token
            token = request.headers.get('tokenapp')
            if token is None:
                return response_error("Error: No se ha podido obtener el Token")

            # Validar el Token
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()

            # Obtener username del token y buscar user_id
            username = TokenComponent.User(token)
            if not username:
                return response_error("Error: No se pudo obtener el usuario del token")

            # Buscar user_id por username
            user_query = "SELECT user_id FROM ceragen.segu_user WHERE user_login_id = %s AND user_state = true"
            user_result = DataBaseHandle.getRecords(user_query, 1, (username,))

            if not user_result.get('result') or not user_result.get('data'):
                return response_error("Usuario no encontrado")

            user_id = user_result['data']['user_id']

            # Verificar que el usuario tenga roles asignados
            role_check = DataBaseHandle.getRecords(
                "SELECT COUNT(*) as role_count FROM ceragen.segu_user_rol WHERE id_user = %s",
                1, (user_id,)
            )

            if not role_check.get('result') or role_check['data']['role_count'] == 0:
                return response_success([])  # Usuario sin roles, retornar array vacío

            # Llamar al método del componente
            answer = ComponentMenu.MenuListByUser(user_id)

            if answer['result'] is True:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(err.__str__())