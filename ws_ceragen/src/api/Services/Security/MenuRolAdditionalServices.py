from flask import request
from flask_restful import Resource
from ....utils.general.logs import HandleLogs
from ....utils.general.response import response_success, response_error, response_unauthorize
from ....api.Components.Security.TokenComponent import TokenComponent
from ....api.Components.Security.MenuRolComponent import MenuRolComponent
from marshmallow import Schema, fields


class MenuRolsByMenuSchema(Schema):
    menu_id = fields.Integer(required=True)


class MenuRolsByRoleSchema(Schema):
    rol_id = fields.Integer(required=True)


class MenuRolBulkAssignSchema(Schema):
    rol_id = fields.Integer(required=True)
    menu_ids = fields.List(fields.Integer(), required=True)


class MenuRolsByMenu(Resource):
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Obtener roles por menú")
            token = request.headers.get('tokenapp')
            rq_json = request.get_json()

            # Validar request
            schema = MenuRolsByMenuSchema()
            errors = schema.validate(rq_json)
            if errors:
                return response_error(f"Error de validación: {errors}")

            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            answer = MenuRolComponent.MenuRolsByMenu(rq_json['menu_id'])

            if answer['result']:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class MenuRolsByRole(Resource):
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Obtener menús por rol")
            token = request.headers.get('tokenapp')
            rq_json = request.get_json()

            # Validar request
            schema = MenuRolsByRoleSchema()
            errors = schema.validate(rq_json)
            if errors:
                return response_error(f"Error de validación: {errors}")

            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            answer = MenuRolComponent.MenuRolsByRole(rq_json['rol_id'])

            if answer['result']:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class MenuRolBulkAssign(Resource):
    @staticmethod
    def post():
        try:
            HandleLogs.write_log("Asignación masiva de menús a rol")
            token = request.headers.get('tokenapp')
            rq_json = request.get_json()

            # Validar request
            schema = MenuRolBulkAssignSchema()
            errors = schema.validate(rq_json)
            if errors:
                return response_error(f"Error de validación: {errors}")

            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_name = TokenComponent.User(token)
            answer = MenuRolComponent.MenuRolBulkAssign(
                rq_json['rol_id'],
                rq_json['menu_ids'],
                user_name
            )

            if answer['result']:
                return response_success(answer['data'])
            else:
                return response_error(answer['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))