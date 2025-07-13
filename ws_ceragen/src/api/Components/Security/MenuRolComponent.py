from ....utils.database.connection_db import DataBaseHandle
from ....utils.general.logs import HandleLogs


class MenuRolComponent:
    @staticmethod
    def MenuRolList():
        try:
            result = False
            message = None
            data = None
            sql = """SELECT 
                        mr.mr_id as registro_id,
                        mr.mr_menu_id as menu_id,
                        mr.mr_rol_id as rol_id,
                        mr.mr_state,
                        m.menu_name,
                        r.rol_name,
                        mod.mod_name,
                        mod.mod_order,
                        m.menu_order
                    FROM ceragen.segu_menu_rol mr
                    INNER JOIN ceragen.segu_menu m ON mr.mr_menu_id = m.menu_id
                    INNER JOIN ceragen.segu_rol r ON mr.mr_rol_id = r.rol_id
                    INNER JOIN ceragen.segu_module mod ON m.menu_module_id = mod.mod_id
                    WHERE mr.mr_state = true
                    ORDER BY mod.mod_order, m.menu_order, r.rol_name"""

            resultado = DataBaseHandle.getRecords(sql, 0)
            HandleLogs.write_log("MenuRolList")
            HandleLogs.write_log(resultado)

            if resultado is None:
                HandleLogs.write_error("Error no existen asignaciones Menu-Rol")
                message = "Error asignaciones Menu-Rol"
            else:
                if resultado.__len__() > 0:
                    result = True
                    data = resultado['data']
                else:
                    message = "No existen asignaciones Menu-Rol"
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
    def MenuRolsByMenu(menu_id):
        """Obtener roles asignados a un menú específico"""
        try:
            result = False
            message = None
            data = None
            sql = """SELECT 
                        mr.mr_id as registro_id,
                        mr.mr_rol_id as rol_id,
                        r.rol_name,
                        r.rol_description
                    FROM ceragen.segu_menu_rol mr
                    INNER JOIN ceragen.segu_rol r ON mr.mr_rol_id = r.rol_id
                    WHERE mr.mr_menu_id = %s 
                    AND mr.mr_state = true
                    AND r.rol_state = true
                    ORDER BY r.rol_name"""

            resultado = DataBaseHandle.getRecords(sql, 0, (menu_id,))
            HandleLogs.write_log(f"MenuRolsByMenu - Menu ID: {menu_id}")
            HandleLogs.write_log(resultado)

            if resultado is None:
                message = "Error al obtener roles del menú"
            else:
                if resultado.get('result') and resultado.get('data'):
                    result = True
                    data = resultado['data']
                else:
                    message = "No hay roles asignados a este menú"
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
    def MenuRolsByRole(rol_id):
        """Obtener menús asignados a un rol específico"""
        try:
            result = False
            message = None
            data = None
            sql = """SELECT 
                        mr.mr_id as registro_id,
                        mr.mr_menu_id as menu_id,
                        m.menu_name,
                        m.menu_icon_name,
                        m.menu_href,
                        mod.mod_name
                    FROM ceragen.segu_menu_rol mr
                    INNER JOIN ceragen.segu_menu m ON mr.mr_menu_id = m.menu_id
                    INNER JOIN ceragen.segu_module mod ON m.menu_module_id = mod.mod_id
                    WHERE mr.mr_rol_id = %s 
                    AND mr.mr_state = true
                    AND m.menu_state = true
                    ORDER BY mod.mod_order, m.menu_order"""

            resultado = DataBaseHandle.getRecords(sql, 0, (rol_id,))
            HandleLogs.write_log(f"MenuRolsByRole - Rol ID: {rol_id}")
            HandleLogs.write_log(resultado)

            if resultado is None:
                message = "Error al obtener menús del rol"
            else:
                if resultado.get('result') and resultado.get('data'):
                    result = True
                    data = resultado['data']
                else:
                    message = "No hay menús asignados a este rol"
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
    def MenuRolInsert(menu_id, rol_id, user_name):
        try:
            result = False
            message = None
            data = None

            # Verificar si ya existe la asignación
            check_sql = """SELECT mr_id FROM ceragen.segu_menu_rol 
                          WHERE mr_menu_id = %s AND mr_rol_id = %s"""

            existing = DataBaseHandle.getRecords(check_sql, 1, (menu_id, rol_id))

            if existing.get('result') and existing.get('data'):
                # Si existe pero está inactiva, reactivarla
                update_sql = """UPDATE ceragen.segu_menu_rol 
                               SET mr_state = true, user_modified = %s, date_modified = timezone('America/Guayaquil', now())
                               WHERE mr_menu_id = %s AND mr_rol_id = %s"""
                resultado = DataBaseHandle.ExecuteNonQuery(update_sql, (user_name, menu_id, rol_id))

                if resultado.get('result') and resultado.get('data', 0) > 0:
                    result = True
                    data = "Asignación reactivada"
                    message = "Asignación reactivada exitosamente"
                else:
                    message = "Error al reactivar la asignación"
            else:
                # Crear nueva asignación
                insert_sql = """INSERT INTO ceragen.segu_menu_rol (mr_menu_id, mr_rol_id, mr_state, user_created, date_created)
                               VALUES (%s, %s, true, %s, timezone('America/Guayaquil', now()))
                               RETURNING mr_id"""

                record = (menu_id, rol_id, user_name)
                resultado = DataBaseHandle.ExecuteInsert(insert_sql, record)

                HandleLogs.write_log("MenuRolInsert")
                HandleLogs.write_log(resultado)

                if resultado.get('result') and resultado.get('data'):
                    result = True
                    value = resultado['data'][0]
                    data = list(value.values())[0]
                    message = "Asignación creada exitosamente"
                else:
                    message = "Error: no se puede insertar la asignación"

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
    def MenuRolDelete(del_id, user_name):
        try:
            result = False
            message = None
            data = None

            # Verificar que existe la asignación
            check_sql = """SELECT mr_id FROM ceragen.segu_menu_rol 
                          WHERE mr_id = %s AND mr_state = true"""

            existing = DataBaseHandle.getRecords(check_sql, 1, (del_id,))

            if not existing.get('result') or not existing.get('data'):
                message = "Asignación no encontrada o ya eliminada"
            else:
                # Soft delete
                delete_sql = """UPDATE ceragen.segu_menu_rol 
                               SET mr_state = false, user_deleted = %s, date_deleted = timezone('America/Guayaquil', now())
                               WHERE mr_id = %s"""

                record = (user_name, del_id)
                resultado = DataBaseHandle.ExecuteNonQuery(delete_sql, record)

                HandleLogs.write_log("MenuRolDelete")
                HandleLogs.write_log(resultado)

                if resultado.get('result') and resultado.get('data', 0) > 0:
                    result = True
                    data = resultado['data']
                    message = "Asignación eliminada exitosamente"
                else:
                    message = "No se pudo eliminar la asignación"

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
    def MenuRolUpdate(registro_id, rol_id, menu_id, user_name):
        try:
            result = False
            message = None
            data = None

            # Verificar que existe el registro
            check_sql = """SELECT mr_id FROM ceragen.segu_menu_rol WHERE mr_id = %s"""
            existing = DataBaseHandle.getRecords(check_sql, 1, (registro_id,))

            if not existing.get('result') or not existing.get('data'):
                message = "Registro no encontrado"
            else:
                update_sql = """UPDATE ceragen.segu_menu_rol 
                               SET mr_rol_id = %s, mr_menu_id = %s, user_modified = %s, date_modified = timezone('America/Guayaquil', now())
                               WHERE mr_id = %s"""

                record = (rol_id, menu_id, user_name, registro_id)
                resultado = DataBaseHandle.ExecuteNonQuery(update_sql, record)

                HandleLogs.write_log("MenuRolUpdate")
                HandleLogs.write_log(resultado)

                if resultado.get('result') and resultado.get('data', 0) > 0:
                    result = True
                    data = resultado['data']
                    message = "Asignación actualizada exitosamente"
                else:
                    message = "No se pudo actualizar la asignación"

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
    def MenuRolBulkAssign(rol_id, menu_ids, user_name):
        """Asignar múltiples menús a un rol"""
        try:
            success_count = 0
            error_count = 0
            errors = []

            for menu_id in menu_ids:
                result = MenuRolComponent.MenuRolInsert(menu_id, rol_id, user_name)
                if result['result']:
                    success_count += 1
                else:
                    error_count += 1
                    errors.append(f"Menú {menu_id}: {result['message']}")

            if error_count == 0:
                return {
                    'result': True,
                    'message': f"Todos los menús ({success_count}) asignados exitosamente",
                    'data': {'success': success_count, 'errors': 0}
                }
            elif success_count > 0:
                return {
                    'result': True,
                    'message': f"{success_count} menús asignados, {error_count} fallaron",
                    'data': {'success': success_count, 'errors': error_count, 'error_details': errors}
                }
            else:
                return {
                    'result': False,
                    'message': "No se pudo asignar ningún menú",
                    'data': {'errors': errors}
                }

        except Exception as err:
            HandleLogs.write_error(err)
            return {
                'result': False,
                'message': err.__str__(),
                'data': None
            }