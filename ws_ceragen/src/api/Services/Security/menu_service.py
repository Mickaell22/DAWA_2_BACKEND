#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Menu Service - Sistema CERAGEN
Gestión de menús dinámicos con control multirol
"""

from ....utils.database.connection_db import DataBaseHandle
from ....utils.general.response import internal_response
from ....utils.general.logs import HandleLogs


class MenuService:

    @staticmethod
    def get_menus():
        """Obtener todos los menús activos"""
        try:
            query = """
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
                    m.menu_state,
                    mod.mod_name,
                    mod.mod_description,
                    mod.mod_icon_name,
                    mod.mod_order
                FROM ceragen.segu_menu m
                INNER JOIN ceragen.segu_module mod ON m.menu_module_id = mod.mod_id
                WHERE m.menu_state = true 
                AND mod.mod_state = true
                ORDER BY mod.mod_order, m.menu_order
            """

            result = DataBaseHandle.getRecords(query, 0)

            if not result['result']:
                return internal_response(False, result['message'], [])

            # Procesar datos para jerarquía
            menus_data = []
            for row in result.get('data', []):
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
                    'menu_state': row['menu_state'],
                    'mod_name': row['mod_name'],
                    'mod_description': row['mod_description'],
                    'mod_icon_name': row['mod_icon_name'],
                    'mod_order': row['mod_order']
                }
                menus_data.append(menu_item)

            return internal_response(True, "Menús obtenidos exitosamente", menus_data)

        except Exception as e:
            HandleLogs.write_error(f"MenuService.get_menus - {e}")
            return internal_response(False, "Error interno del servidor", [])

    @staticmethod
    def get_user_menus(user_id):
        """Obtener menús permitidos para un usuario específico"""
        try:
            query = """
                SELECT DISTINCT
                    m.menu_id,
                    m.menu_name,
                    m.menu_order,
                    m.menu_module_id,
                    m.menu_parent_id,
                    m.menu_icon_name,
                    m.menu_href,
                    m.menu_url,
                    m.menu_key,
                    mod.mod_name,
                    mod.mod_description,
                    mod.mod_icon_name,
                    mod.mod_order
                FROM ceragen.segu_menu m
                INNER JOIN ceragen.segu_module mod ON m.menu_module_id = mod.mod_id
                INNER JOIN ceragen.segu_menu_rol mr ON m.menu_id = mr.mr_menu_id
                INNER JOIN ceragen.segu_user_rol ur ON mr.mr_rol_id = ur.id_rol
                WHERE ur.id_user = %s 
                AND m.menu_state = true 
                AND mod.mod_state = true
                AND mr.mr_state = true
                AND ur.ur_state = true
                ORDER BY mod.mod_order, m.menu_order
            """

            result = DataBaseHandle.getRecords(query, 0, (user_id,))

            if not result['result']:
                return internal_response(False, result['message'], [])

            # Construir estructura jerárquica
            menus_hierarchy = MenuService._build_menu_hierarchy(result.get('data', []))

            return internal_response(True, "Menús del usuario obtenidos exitosamente", menus_hierarchy)

        except Exception as e:
            HandleLogs.write_error(f"MenuService.get_user_menus - {e}")
            return internal_response(False, "Error interno del servidor", [])

    @staticmethod
    def create_menu(menu_data, user_created):
        """Crear nuevo menú"""
        try:
            # Validaciones
            if not menu_data.get('menu_name'):
                return internal_response(False, "El nombre del menú es requerido", [])

            if not menu_data.get('menu_module_id'):
                return internal_response(False, "El módulo es requerido", [])

            # Verificar que el módulo existe
            module_check = DataBaseHandle.getRecords(
                "SELECT mod_id FROM ceragen.segu_module WHERE mod_id = %s AND mod_state = true",
                1, (menu_data['menu_module_id'],)
            )

            if not module_check['result'] or not module_check.get('data'):
                return internal_response(False, "Módulo no encontrado o inactivo", [])

            # Obtener siguiente orden si no se especifica
            menu_order = menu_data.get('menu_order')
            if not menu_order:
                order_query = """
                    SELECT COALESCE(MAX(menu_order), 0) + 1 
                    FROM ceragen.segu_menu 
                    WHERE menu_module_id = %s
                """
                order_result = DataBaseHandle.getRecords(order_query, 1, (menu_data['menu_module_id'],))
                menu_order = list(order_result['data'].values())[0] if order_result['result'] and order_result.get(
                    'data') else 1

            # Insertar menú
            insert_query = """
                INSERT INTO ceragen.segu_menu (
                    menu_name, menu_order, menu_module_id, menu_parent_id,
                    menu_icon_name, menu_href, menu_url, menu_key,
                    menu_state, user_created, date_created
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING menu_id
            """

            values = (
                menu_data['menu_name'],
                menu_order,
                menu_data['menu_module_id'],
                menu_data.get('menu_parent_id'),
                menu_data.get('menu_icon_name'),
                menu_data.get('menu_href'),
                menu_data.get('menu_url'),
                menu_data.get('menu_key'),
                menu_data.get('menu_state', True),
                user_created
            )

            result = DataBaseHandle.ExecuteInsert(insert_query, values)

            if not result['result']:
                return internal_response(False, result['message'], [])

            menu_id = result['data'][0]['menu_id'] if result.get('data') else None

            return internal_response(True, "Menú creado exitosamente", {'menu_id': menu_id})

        except Exception as e:
            HandleLogs.write_error(f"MenuService.create_menu - {e}")
            return internal_response(False, "Error interno del servidor", [])

    @staticmethod
    def update_menu(menu_id, menu_data, user_modified):
        """Actualizar menú existente"""
        try:
            # Verificar que el menú existe
            menu_check = DataBaseHandle.getRecords(
                "SELECT menu_id FROM ceragen.segu_menu WHERE menu_id = %s",
                1, (menu_id,)
            )

            if not menu_check['result'] or not menu_check.get('data'):
                return internal_response(False, "Menú no encontrado", [])

            # Construir query de actualización dinámicamente
            set_clauses = []
            values = []

            updateable_fields = [
                'menu_name', 'menu_order', 'menu_module_id', 'menu_parent_id',
                'menu_icon_name', 'menu_href', 'menu_url', 'menu_key', 'menu_state'
            ]

            for field in updateable_fields:
                if field in menu_data:
                    set_clauses.append(f"{field} = %s")
                    values.append(menu_data[field])

            if not set_clauses:
                return internal_response(False, "No hay campos para actualizar", [])

            set_clauses.append("user_modified = %s")
            set_clauses.append("date_modified = NOW()")
            values.extend([user_modified, menu_id])

            update_query = f"""
                UPDATE ceragen.segu_menu 
                SET {', '.join(set_clauses)}
                WHERE menu_id = %s
            """

            result = DataBaseHandle.ExecuteNonQuery(update_query, values)

            if not result['result']:
                return internal_response(False, result['message'], [])

            return internal_response(True, "Menú actualizado exitosamente", [])

        except Exception as e:
            HandleLogs.write_error(f"MenuService.update_menu - {e}")
            return internal_response(False, "Error interno del servidor", [])

    @staticmethod
    def delete_menu(menu_id, user_deleted):
        """Eliminar menú (soft delete)"""
        try:
            # Verificar que el menú existe
            menu_check = DataBaseHandle.getRecords(
                "SELECT menu_id FROM ceragen.segu_menu WHERE menu_id = %s AND menu_state = true",
                1, (menu_id,)
            )

            if not menu_check['result'] or not menu_check.get('data'):
                return internal_response(False, "Menú no encontrado o ya eliminado", [])

            # Verificar si tiene menús hijos
            children_check = DataBaseHandle.getRecords(
                "SELECT COUNT(*) as count FROM ceragen.segu_menu WHERE menu_parent_id = %s AND menu_state = true",
                1, (menu_id,)
            )

            if children_check['result'] and children_check.get('data') and children_check['data']['count'] > 0:
                return internal_response(False, "No se puede eliminar: el menú tiene submenús activos", [])

            # Soft delete
            delete_query = """
                UPDATE ceragen.segu_menu 
                SET menu_state = false, user_deleted = %s, date_deleted = NOW()
                WHERE menu_id = %s
            """

            result = DataBaseHandle.ExecuteNonQuery(delete_query, (user_deleted, menu_id))

            if not result['result']:
                return internal_response(False, result['message'], [])

            return internal_response(True, "Menú eliminado exitosamente", [])

        except Exception as e:
            HandleLogs.write_error(f"MenuService.delete_menu - {e}")
            return internal_response(False, "Error interno del servidor", [])

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
                'children': []
            }

            module_info = {
                'mod_name': row['mod_name'],
                'mod_description': row['mod_description'],
                'mod_icon_name': row['mod_icon_name'],
                'mod_order': row['mod_order'],
                'menus': []
            }

            module_id = row['menu_module_id']

            if module_id not in modules:
                modules[module_id] = module_info

            modules[module_id]['menus'].append(menu_item)

        # Organizar en jerarquía dentro de cada módulo
        for module_id, module_data in modules.items():
            menus = module_data['menus']

            # Separar menús padre e hijos
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