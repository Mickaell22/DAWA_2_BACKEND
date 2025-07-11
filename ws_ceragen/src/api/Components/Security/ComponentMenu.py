from ....utils.database.connection_db import DataBaseHandle
from ....utils.general.logs import HandleLogs


class ComponentMenu:
    @staticmethod
    def MenuList():
        try:
            result = False
            message = None
            data = None
            sql = """SELECT m.menu_id, 
                                   m.menu_name, 
                                   m.menu_order, 
                                   m.menu_module_id, 
                                   mm.mod_name AS menu_module_name,
                                   m.menu_parent_id, 
                                   p.menu_name AS menu_parent_name,
                                   m.menu_icon_name, 
                                   m.menu_href, 
                                   m.menu_url, 
                                   m.menu_key,
                                   m.menu_state,
                                   mm.mod_order
                            FROM ceragen.segu_menu m
                            LEFT JOIN ceragen.segu_menu p ON m.menu_parent_id = p.menu_id
                            LEFT JOIN ceragen.segu_module mm ON m.menu_module_id = mm.mod_id
                            WHERE m.menu_state = true AND mm.mod_state = true
                            ORDER BY mm.mod_order, m.menu_order;"""

            resultado = DataBaseHandle.getRecords(sql, 0)

            HandleLogs.write_log("MenuList")
            HandleLogs.write_log(resultado)

            if resultado is None:
                HandleLogs.write_error("Error no Existe Menu")
                message = "Error Menú"
            else:
                if resultado.__len__() > 0:
                    result = True
                    data = resultado['data']
                else:
                    message = "No existe Menú"
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def MenuListByUser(user_id):
        """Obtener menús jerárquicos permitidos para un usuario específico"""
        try:
            result = False
            message = None
            data = None

            sql = """SELECT DISTINCT
                            m.menu_id,
                            m.menu_name,
                            m.menu_order,
                            m.menu_module_id,
                            m.menu_parent_id,
                            m.menu_icon_name,
                            m.menu_href,
                            m.menu_url,
                            m.menu_key,
                            mm.mod_name,
                            mm.mod_description,
                            mm.mod_icon_name,
                            mm.mod_order,
                            p.menu_name AS parent_menu_name
                        FROM ceragen.segu_menu m
                        INNER JOIN ceragen.segu_module mm ON m.menu_module_id = mm.mod_id
                        INNER JOIN ceragen.segu_menu_rol mr ON m.menu_id = mr.mr_menu_id
                        INNER JOIN ceragen.segu_user_rol ur ON mr.mr_rol_id = ur.id_rol
                        LEFT JOIN ceragen.segu_menu p ON m.menu_parent_id = p.menu_id
                        WHERE ur.id_user = %s 
                        AND m.menu_state = true 
                        AND mm.mod_state = true
                        AND mr.mr_state = true
                        ORDER BY mm.mod_order, m.menu_order"""

            resultado = DataBaseHandle.getRecords(sql, 0, (user_id,))

            HandleLogs.write_log("MenuListByUser")
            HandleLogs.write_log(resultado)

            if resultado is None:
                HandleLogs.write_error("Error al obtener menús del usuario")
                message = "Error al obtener menús del usuario"
            else:
                if resultado.get('result') and resultado.get('data'):
                    # Construir jerarquía de menús por módulos
                    hierarchy = ComponentMenu._build_menu_hierarchy(resultado['data'])
                    result = True
                    data = hierarchy
                else:
                    message = "No hay menús asignados para este usuario"

        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }


    @staticmethod
    def _build_menu_hierarchy(menu_data):
        """Construir jerarquía de menús organizados por módulos"""
        modules = {}

        for row in menu_data:
            menu_item = {
                'menu_id': row['menu_id'],
                'menu_name': row['menu_name'],
                'menu_order': row['menu_order'],
                'menu_module_id': row['menu_module_id'],
                'menu_parent_id': row['menu_parent_id'],
                'menu_icon_name': row['menu_icon_name'],
                'menu_href': row['menu_href'],
                'menu_url': row['menu_url'],
                'menu_key': row['menu_key'],
                'parent_menu_name': row.get('parent_menu_name'),
                'children': []
            }

            module_id = row['menu_module_id']

            if module_id not in modules:
                modules[module_id] = {
                    'mod_id': module_id,
                    'mod_name': row['mod_name'],
                    'mod_description': row['mod_description'],
                    'mod_icon_name': row['mod_icon_name'],
                    'mod_order': row['mod_order'],
                    'menus': []
                }

            modules[module_id]['menus'].append(menu_item)

        # Organizar en jerarquía dentro de cada módulo
        for module_id, module_data in modules.items():
            menus = module_data['menus']

            # Crear diccionario para búsqueda rápida
            menu_dict = {menu['menu_id']: menu for menu in menus}
            root_menus = []

            for menu in menus:
                if menu['menu_parent_id'] and menu['menu_parent_id'] in menu_dict:
                    # Es un menú hijo
                    parent = menu_dict[menu['menu_parent_id']]
                    parent['children'].append(menu)
                else:
                    # Es un menú padre
                    root_menus.append(menu)

            # Ordenar menús y submenús
            root_menus.sort(key=lambda x: x['menu_order'])
            for menu in root_menus:
                menu['children'].sort(key=lambda x: x['menu_order'])

            module_data['menus'] = root_menus

        # Convertir a lista ordenada por mod_order
        return sorted(modules.values(), key=lambda x: x['mod_order'])

    @staticmethod
    def MenuDelete(id, user_name):
        try:
            record = (user_name, id)
            result = False
            message = None
            data = None
            sql = "UPDATE ceragen.segu_menu SET menu_state = false, user_deleted = %s, date_deleted= timezone('America/Guayaquil', now()) WHERE menu_id = %s"

            resultado = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log("delete")
            HandleLogs.write_log(resultado)
            if resultado['data'] > 0:
                result = True
                data = resultado['data']
            else:
                message = "No existe el recurso con el ID: " + str(id)
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def MenuUpdate(menu_name, menu_order, menu_module_id, menu_parent_id, menu_icon_name, menu_href, menu_url,
                   user_name, menu_id):
        try:
            if menu_parent_id == 0: menu_parent_id = None
            menu_key = f"{menu_name}_{menu_order}"
            record = (menu_name, menu_order, menu_module_id, menu_parent_id, menu_icon_name, menu_href, menu_url,
                      menu_key, user_name, menu_id)
            result = False
            message = None
            data = None
            sql = """UPDATE ceragen.segu_menu
                      SET menu_name = %s, menu_order = %s, menu_module_id = %s, menu_parent_id = %s, menu_icon_name = %s, menu_href = %s, menu_url = %s, menu_key = %s, user_modified = %s, date_modified = timezone('America/Guayaquil', now())
                      WHERE menu_id = %s"""
            resultado = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log("update")
            HandleLogs.write_log(resultado)
            if resultado['data'] > 0:
                result = True
                data = resultado['data']
            else:
                message = "No existe el recurso con el ID: " + str(menu_id)
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def MenuInsert(menu_name, menu_order, menu_module_id, menu_parent_id, menu_icon_name, menu_href, menu_url,
                   user_name):
        try:
            if menu_parent_id == 0: menu_parent_id = None
            menu_key = f"{menu_name}_{menu_order}"
            record = (menu_name, menu_order, menu_module_id, menu_parent_id, menu_icon_name, menu_href, menu_url,
                      menu_key, user_name, menu_name)
            result = False
            message = None
            data = None
            sql = """INSERT INTO ceragen.segu_menu(menu_name, menu_order, menu_module_id, menu_parent_id, menu_icon_name, menu_href, menu_url, menu_key, menu_state, user_created, date_created) 
                      SELECT %s, %s, %s, %s, %s, %s, %s, %s, true, %s, timezone('America/Guayaquil', now())
                      WHERE NOT EXISTS (
                            SELECT 1
                            FROM ceragen.segu_menu 
                            WHERE menu_name = %s AND menu_state = true 
                        )
                        RETURNING menu_id"""
            resultado = DataBaseHandle.ExecuteInsert(sql, record)
            HandleLogs.write_log(resultado)

            if resultado['data']:
                result = True
                value = resultado['data'][0]
                data = list(value.values())[0]
            else:
                message = "Error: no se puede insertar el registro"

        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }