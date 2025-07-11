#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Menu Controller - Sistema CERAGEN
Controlador para gestión de menús con control multirol
"""

from flask import Blueprint, request, jsonify
from ...Services.Security.menu_service import MenuService
from ....utils.general.response import build_response
from ....utils.general.logs import HandleLogs
from ....utils.middleware.middleware_auth import token_required

menu_bp = Blueprint('menu', __name__)


@menu_bp.route('/Menu/get', methods=['GET'])
@token_required
def get_menus(current_user):
    """Obtener todos los menús activos"""
    try:
        result = MenuService.get_menus()

        if result['result']:
            return build_response(True, "Menús obtenidos exitosamente", result['data'])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.get_menus - {e}")
        return build_response(False, "Error interno del servidor", [])


@menu_bp.route('/Menu/getUserMenus/<int:user_id>', methods=['GET'])
@token_required
def get_user_menus(current_user, user_id):
    """Obtener menús específicos de un usuario"""
    try:
        result = MenuService.get_user_menus(user_id)

        if result['result']:
            return build_response(True, "Menús del usuario obtenidos exitosamente", result['data'])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.get_user_menus - {e}")
        return build_response(False, "Error interno del servidor", [])


@menu_bp.route('/Menu/getMyMenus', methods=['GET'])
@token_required
def get_my_menus(current_user):
    """Obtener menús del usuario actual"""
    try:
        user_id = current_user['user_id']
        result = MenuService.get_user_menus(user_id)

        if result['result']:
            return build_response(True, "Sus menús obtenidos exitosamente", result['data'])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.get_my_menus - {e}")
        return build_response(False, "Error interno del servidor", [])


@menu_bp.route('/Menu/insert', methods=['POST'])
@token_required
def create_menu(current_user):
    """Crear nuevo menú"""
    try:
        data = request.get_json()

        if not data:
            return build_response(False, "Datos requeridos", [])

        # Validaciones básicas
        required_fields = ['menu_name', 'menu_module_id']
        for field in required_fields:
            if not data.get(field):
                return build_response(False, f"Campo {field} es requerido", [])

        user_created = current_user.get('user_name', 'system')
        result = MenuService.create_menu(data, user_created)

        if result['result']:
            return build_response(True, result['message'], result['data'])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.create_menu - {e}")
        return build_response(False, "Error interno del servidor", [])


@menu_bp.route('/Menu/update/<int:menu_id>', methods=['PUT'])
@token_required
def update_menu(current_user, menu_id):
    """Actualizar menú existente"""
    try:
        data = request.get_json()

        if not data:
            return build_response(False, "Datos requeridos", [])

        user_modified = current_user.get('user_name', 'system')
        result = MenuService.update_menu(menu_id, data, user_modified)

        if result['result']:
            return build_response(True, result['message'], [])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.update_menu - {e}")
        return build_response(False, "Error interno del servidor", [])


@menu_bp.route('/Menu/delete/<int:menu_id>', methods=['DELETE'])
@token_required
def delete_menu(current_user, menu_id):
    """Eliminar menú (soft delete)"""
    try:
        user_deleted = current_user.get('user_name', 'system')
        result = MenuService.delete_menu(menu_id, user_deleted)

        if result['result']:
            return build_response(True, result['message'], [])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.delete_menu - {e}")
        return build_response(False, "Error interno del servidor", [])


@menu_bp.route('/Menu/toggle/<int:menu_id>', methods=['PATCH'])
@token_required
def toggle_menu_state(current_user, menu_id):
    """Cambiar estado activo/inactivo del menú"""
    try:
        data = request.get_json()
        menu_state = data.get('menu_state', True)

        update_data = {'menu_state': menu_state}
        user_modified = current_user.get('user_name', 'system')

        result = MenuService.update_menu(menu_id, update_data, user_modified)

        if result['result']:
            status_text = "activado" if menu_state else "desactivado"
            return build_response(True, f"Menú {status_text} exitosamente", [])
        else:
            return build_response(False, result['message'], [])

    except Exception as e:
        HandleLogs.write_error(f"menu_controller.toggle_menu_state - {e}")
        return build_response(False, "Error interno del servidor", [])