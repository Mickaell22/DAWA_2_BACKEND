from flask import request
from flask_restful import Resource
from ....utils.general.logs import HandleLogs
from ....utils.general.response import response_success, response_error, response_unauthorize
from ....api.Components.Security.TokenComponent import TokenComponent
from ....api.Components.Security.ComponentMenu import ComponentMenu


class UserMenuPermissions(Resource):
    @staticmethod
    def get():
        """Obtener permisos de menú del usuario actual"""
        try:
            HandleLogs.write_log("Verificando permisos de menú del usuario")

            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            user_id = TokenComponent.UserId(token)
            if not user_id:
                return response_error("No se pudo obtener ID del usuario")

            # Obtener menús del usuario
            answer = ComponentMenu.MenuListByUser(user_id)

            if answer['result']:
                # Extraer solo los permisos como lista plana para validación rápida
                permissions = []
                for module in answer['data']:
                    for menu in module['menus']:
                        permissions.append({
                            'menu_id': menu['menu_id'],
                            'menu_key': menu['menu_key'],
                            'menu_href': menu['menu_href'],
                            'menu_url': menu['menu_url']
                        })
                        # Agregar submenús
                        for submenu in menu.get('children', []):
                            permissions.append({
                                'menu_id': submenu['menu_id'],
                                'menu_key': submenu['menu_key'],
                                'menu_href': submenu['menu_href'],
                                'menu_url': submenu['menu_url']
                            })

                return response_success({
                    'permissions': permissions,
                    'full_structure': answer['data']
                })
            else:
                return response_error(answer['message'])

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class ValidateMenuAccess(Resource):
    @staticmethod
    def post():
        """Validar si usuario tiene acceso a un menú específico"""
        try:
            HandleLogs.write_log("Validando acceso a menú")

            token = request.headers.get('tokenapp')
            rq_json = request.get_json()

            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            if not rq_json or not rq_json.get('menu_key'):
                return response_error("menu_key requerido")

            user_id = TokenComponent.UserId(token)
            menu_key = rq_json['menu_key']

            # Verificar acceso específico
            check_sql = """
                SELECT COUNT(*) as has_access
                FROM ceragen.segu_menu m
                INNER JOIN ceragen.segu_menu_rol mr ON m.menu_id = mr.mr_menu_id
                INNER JOIN ceragen.segu_user_rol ur ON mr.mr_rol_id = ur.id_rol
                WHERE ur.id_user = %s 
                AND m.menu_key = %s
                AND m.menu_state = true
                AND mr.mr_state = true
                AND ur.ur_state = true
            """

            from ....utils.database.connection_db import DataBaseHandle
            result = DataBaseHandle.getRecords(check_sql, 1, (user_id, menu_key))

            if result.get('result') and result.get('data'):
                has_access = result['data']['has_access'] > 0
                return response_success({
                    'has_access': has_access,
                    'menu_key': menu_key,
                    'user_id': user_id
                })
            else:
                return response_error("Error al verificar acceso")

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))