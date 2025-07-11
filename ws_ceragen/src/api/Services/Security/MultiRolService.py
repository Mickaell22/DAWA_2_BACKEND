from flask import request
from flask_restful import Resource
from ....utils.general.logs import HandleLogs
from ....utils.general.response import response_success, response_error, response_unauthorize
from ....api.Components.Security.TokenComponent import TokenComponent
from ....api.Components.Security.ComponentMenu import ComponentMenu
from ....utils.database.connection_db import DataBaseHandle


class UserRolesService(Resource):
    """Obtener todos los roles disponibles del usuario actual"""

    @staticmethod
    def get():
        try:
            HandleLogs.write_log("Obteniendo roles del usuario actual")

            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Obtener usuario del token
            username = TokenComponent.User(token)

            # Obtener user_id
            user_query = """
            SELECT user_id 
            FROM ceragen.segu_user 
            WHERE user_login_id = %s AND user_state = true
            """
            user_result = DataBaseHandle.getRecords(user_query, 1, (username,))

            if not user_result.get('result') or not user_result.get('data'):
                return response_error("Usuario no encontrado")

            user_id = user_result['data']['user_id']

            # Obtener todos los roles del usuario
            roles_query = """
            SELECT 
                ur.id_user_rol,
                r.rol_id,
                r.rol_name,
                r.rol_description,
                r.is_admin_rol
            FROM ceragen.segu_user_rol ur
            INNER JOIN ceragen.segu_rol r ON ur.id_rol = r.rol_id
            WHERE ur.id_user = %s 
                AND ur.state = true 
                AND r.rol_state = true
            ORDER BY r.rol_name
            """

            roles_result = DataBaseHandle.getRecords(roles_query, 0, (user_id,))

            if roles_result.get('result'):
                return response_success({
                    'user_id': user_id,
                    'roles': roles_result['data']
                })
            else:
                return response_success({
                    'user_id': user_id,
                    'roles': []
                })

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))


class MenuByRoleService(Resource):
    """Obtener menús específicos de un rol para el usuario actual"""

    @staticmethod
    def get(rol_id):
        try:
            HandleLogs.write_log(f"Obteniendo menús del rol {rol_id}")

            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Token requerido")

            if not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            # Verificar que el usuario tenga asignado este rol
            username = TokenComponent.User(token)

            verify_query = """
            SELECT COUNT(*) as has_role
            FROM ceragen.segu_user u
            INNER JOIN ceragen.segu_user_rol ur ON u.user_id = ur.id_user
            WHERE u.user_login_id = %s 
                AND ur.id_rol = %s
                AND u.user_state = true
                AND ur.state = true
            """

            verify_result = DataBaseHandle.getRecords(verify_query, 1, (username, rol_id))

            if not verify_result.get('result') or verify_result['data']['has_role'] == 0:
                return response_error("No tiene permisos para acceder a este rol")

            # Obtener menús del rol específico
            menu_query = """
            WITH RECURSIVE menu_tree AS (
                -- Menús raíz
                SELECT 
                    m.menu_id,
                    m.menu_name,
                    m.menu_order,
                    m.menu_module_id,
                    m.menu_parent_id,
                    m.menu_icon_name,
                    m.menu_href,
                    m.menu_url,
                    m.menu_key,
                    0 as level
                FROM ceragen.segu_menu m
                INNER JOIN ceragen.segu_menu_rol mr ON m.menu_id = mr.mr_menu_id
                WHERE mr.mr_rol_id = %s
                    AND m.menu_state = true
                    AND m.menu_parent_id IS NULL

                UNION ALL

                -- Submenús
                SELECT 
                    m.menu_id,
                    m.menu_name,
                    m.menu_order,
                    m.menu_module_id,
                    m.menu_parent_id,
                    m.menu_icon_name,
                    m.menu_href,
                    m.menu_url,
                    m.menu_key,
                    mt.level + 1
                FROM ceragen.segu_menu m
                INNER JOIN menu_tree mt ON m.menu_parent_id = mt.menu_id
                WHERE m.menu_state = true
            )
            SELECT 
                mt.*,
                md.mod_name,
                md.mod_icon_name,
                md.mod_order
            FROM menu_tree mt
            INNER JOIN ceragen.segu_module md ON mt.menu_module_id = md.mod_id
            WHERE md.mod_state = true
            ORDER BY md.mod_order, mt.level, mt.menu_order
            """

            menu_result = DataBaseHandle.getRecords(menu_query, 0, (rol_id,))

            if not menu_result.get('result'):
                return response_error("Error al obtener menús")

            # Organizar menús por módulos
            modules = {}
            menus_by_id = {}

            # Primera pasada: crear todos los menús
            for menu in menu_result['data']:
                menu_item = {
                    'menu_id': menu['menu_id'],
                    'menu_name': menu['menu_name'],
                    'menu_icon_name': menu['menu_icon_name'],
                    'menu_href': menu['menu_href'],
                    'menu_url': menu['menu_url'],
                    'menu_key': menu['menu_key'],
                    'menu_parent_id': menu['menu_parent_id'],
                    'children': []
                }
                menus_by_id[menu['menu_id']] = menu_item

                # Crear módulo si no existe
                mod_id = menu['menu_module_id']
                if mod_id not in modules:
                    modules[mod_id] = {
                        'mod_id': mod_id,
                        'mod_name': menu['mod_name'],
                        'mod_icon_name': menu['mod_icon_name'],
                        'mod_order': menu['mod_order'],
                        'menus': []
                    }

            # Segunda pasada: organizar jerarquía
            for menu_id, menu_item in menus_by_id.items():
                if menu_item['menu_parent_id'] is None:
                    # Es menú raíz, agregarlo al módulo
                    for menu in menu_result['data']:
                        if menu['menu_id'] == menu_id:
                            modules[menu['menu_module_id']]['menus'].append(menu_item)
                            break
                else:
                    # Es submenú, agregarlo a su padre
                    parent_id = menu_item['menu_parent_id']
                    if parent_id in menus_by_id:
                        menus_by_id[parent_id]['children'].append(menu_item)

            # Convertir a lista y ordenar
            modules_list = sorted(modules.values(), key=lambda x: x['mod_order'])

            return response_success({
                'rol_id': rol_id,
                'modules': modules_list
            })

        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))