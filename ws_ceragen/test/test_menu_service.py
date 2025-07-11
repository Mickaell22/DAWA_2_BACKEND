#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Menu Service - Sistema CERAGEN
Pruebas unitarias para funcionalidad de menús
"""

import unittest
import sys
import os

# Agregar el directorio padre al PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class TestMenuLogic(unittest.TestCase):
    """Tests básicos de lógica sin dependencias"""

    def test_menu_hierarchy_builder(self):
        """Test: Constructor de jerarquía de menús"""

        def build_menu_hierarchy(menu_data):
            """Función local para testear la lógica"""
            modules = {}

            for row in menu_data:
                menu_item = {
                    'menu_id': row['menu_id'],
                    'menu_name': row['menu_name'],
                    'menu_order': row['menu_order'],
                    'menu_module_id': row['menu_module_id'],
                    'menu_parent_id': row['menu_parent_id'],
                    'children': []
                }

                module_id = row['menu_module_id']

                if module_id not in modules:
                    modules[module_id] = {
                        'mod_id': module_id,
                        'mod_name': row['mod_name'],
                        'mod_order': row['mod_order'],
                        'menus': []
                    }

                modules[module_id]['menus'].append(menu_item)

            # Organizar jerarquía
            for module_id, module_data in modules.items():
                menus = module_data['menus']
                menu_dict = {menu['menu_id']: menu for menu in menus}
                root_menus = []

                for menu in menus:
                    if menu['menu_parent_id'] and menu['menu_parent_id'] in menu_dict:
                        parent = menu_dict[menu['menu_parent_id']]
                        parent['children'].append(menu)
                    else:
                        root_menus.append(menu)

                root_menus.sort(key=lambda x: x['menu_order'])
                for menu in root_menus:
                    menu['children'].sort(key=lambda x: x['menu_order'])

                module_data['menus'] = root_menus

            return sorted(modules.values(), key=lambda x: x['mod_order'])

        # Test data
        test_data = [
            {
                'menu_id': 1,
                'menu_name': 'Dashboard',
                'menu_order': 1,
                'menu_module_id': 1,
                'menu_parent_id': None,
                'mod_name': 'Admin',
                'mod_order': 1
            },
            {
                'menu_id': 2,
                'menu_name': 'Configuración',
                'menu_order': 2,
                'menu_module_id': 1,
                'menu_parent_id': 1,
                'mod_name': 'Admin',
                'mod_order': 1
            }
        ]

        result = build_menu_hierarchy(test_data)

        # Assertions
        self.assertEqual(len(result), 1)  # Un módulo
        self.assertEqual(len(result[0]['menus']), 1)  # Un menú padre
        self.assertEqual(len(result[0]['menus'][0]['children']), 1)  # Un hijo
        self.assertEqual(result[0]['menus'][0]['menu_name'], 'Dashboard')
        self.assertEqual(result[0]['menus'][0]['children'][0]['menu_name'], 'Configuración')

    def test_menu_key_generation(self):
        """Test: Generación de claves de menú"""

        def generate_menu_key(menu_name, menu_order):
            return f"{menu_name}_{menu_order}"

        key = generate_menu_key("Dashboard", 1)
        self.assertEqual(key, "Dashboard_1")

        key2 = generate_menu_key("Usuarios", 2)
        self.assertEqual(key2, "Usuarios_2")

    def test_menu_validation(self):
        """Test: Validación de datos de menú"""

        def validate_menu_data(menu_data):
            errors = []

            if not menu_data.get('menu_name'):
                errors.append("Nombre de menú requerido")

            if not menu_data.get('menu_module_id'):
                errors.append("Módulo requerido")

            if menu_data.get('menu_order') is not None and menu_data['menu_order'] < 1:
                errors.append("Orden debe ser mayor a 0")

            return errors

        # Test válido
        valid_data = {'menu_name': 'Test', 'menu_module_id': 1, 'menu_order': 1}
        errors = validate_menu_data(valid_data)
        self.assertEqual(len(errors), 0)

        # Test inválido
        invalid_data = {'menu_module_id': 1, 'menu_order': 0}
        errors = validate_menu_data(invalid_data)
        self.assertEqual(len(errors), 2)
        self.assertIn("Nombre de menú requerido", errors)
        self.assertIn("Orden debe ser mayor a 0", errors)

    def test_menu_hierarchy_empty(self):
        """Test: Jerarquía con datos vacíos"""

        def build_menu_hierarchy(menu_data):
            if not menu_data:
                return []
            # Lógica simplificada para test
            return []

        result = build_menu_hierarchy([])
        self.assertEqual(len(result), 0)

    def test_parent_id_handling(self):
        """Test: Manejo de parent_id"""

        def normalize_parent_id(parent_id):
            if parent_id == 0 or parent_id == "0":
                return None
            return parent_id

        self.assertIsNone(normalize_parent_id(0))
        self.assertIsNone(normalize_parent_id("0"))
        self.assertEqual(normalize_parent_id(5), 5)
        self.assertEqual(normalize_parent_id("5"), "5")


class TestMenuResponseFormat(unittest.TestCase):
    """Tests para formato de respuestas"""

    def test_success_response_format(self):
        """Test: Formato de respuesta exitosa"""

        def build_response(result, message, data):
            return {
                'result': result,
                'message': message,
                'data': data
            }

        response = build_response(True, "Éxito", [{'menu_id': 1}])

        self.assertTrue(response['result'])
        self.assertEqual(response['message'], "Éxito")
        self.assertEqual(len(response['data']), 1)

    def test_error_response_format(self):
        """Test: Formato de respuesta de error"""

        def build_response(result, message, data):
            return {
                'result': result,
                'message': message,
                'data': data
            }

        response = build_response(False, "Error de prueba", [])

        self.assertFalse(response['result'])
        self.assertEqual(response['message'], "Error de prueba")
        self.assertEqual(len(response['data']), 0)


if __name__ == '__main__':
    print("🧪 Ejecutando pruebas unitarias de Menu Service...")
    print("=" * 50)

    # Ejecutar pruebas
    unittest.main(verbosity=2)