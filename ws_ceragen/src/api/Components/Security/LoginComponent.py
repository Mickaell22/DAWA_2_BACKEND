from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from ...Components.Security.rolComponent import RolComponent
from ...Components.Security.moduleComponent import ModuleComponent
from ...Components.Security.menuComponent import MenuComponent
from datetime import datetime


class LoginComponent:

    @staticmethod
    def Login(user, clave):
        try:
            import hashlib

            def convert_datetime_to_string(data):
                for key, value in data.items():
                    if isinstance(value, datetime):
                        data[key] = value.isoformat()
                return data

            result = False
            message = None
            data = None

            # Hash la contraseña con MD5
            clave = hashlib.md5(clave.encode()).hexdigest()
            HandleLogs.write_log(f"Password hasheado: {clave}")
            HandleLogs.write_log(f"Buscando usuario: {user} con password hash")

            sql = "select us.user_id, us.user_login_id,us.user_mail , per_names, per_surnames, user_locked, user_last_login " \
                  "from ceragen.segu_user us " \
                  "inner join ceragen.admin_person pe on us.user_person_id = pe.per_id " \
                  "where user_login_id = %s " \
                  "and user_password = %s " \
                  "and user_state = true and user_locked = false;"
            record = (user, clave)

            resultado = DataBaseHandle.getRecords(sql, 1, record)
            HandleLogs.write_log(f"Resultado SQL usuario: {resultado}")
            # HandleLogs.write_log(resultado)
            message = resultado['message']
            if resultado['data'] is None:
                update_login_attempts = """UPDATE ceragen.segu_user
                                           SET login_attempts = CASE
                                                                    WHEN login_attempts < 3 THEN login_attempts + 1
                                                                    ELSE login_attempts \
                                               END,
                                               user_locked    = CASE \
                                                                    WHEN login_attempts + 1 >= 3 THEN TRUE \
                                                                    ELSE false
                                                   END,
                                               user_modified  = %s,
                                               date_modified  = timezone('America/Guayaquil', now())
                                           WHERE user_login_id = %s RETURNING 
                    CASE 
                        WHEN login_attempts  < 3 THEN 3 - login_attempts
                        ELSE 0
                END \
                AS intentos_restantes, 
                    user_locked,
                    user_state;"""

                update_record = (user, user)
                update_result = DataBaseHandle.ExecuteInsert(update_login_attempts, update_record)
                if update_result['data'] is None or len(update_result['data']) == 0:
                    message = update_result.get('message',
                                                f'Cuenta {user} no encontrada') or f'Cuenta {user} no encontrada'
                else:
                    data = update_result['data'][0]  # Extrae el primer elemento de la lista
                    if data['user_locked']: message = f'Cuenta {user} bloqueada, consulte con el administrador'
                    if data[
                        'intentos_restantes'] < 3: message = f'Verifique sus credenciales; intentos restantes: {data["intentos_restantes"]}'
                    if data['user_state'] is False: message = f'Cuenta  {user}  no encontrada'
            else:
                v_user_id = resultado['data']['user_id']
                HandleLogs.write_log(f"Usuario encontrado, ID: {v_user_id}")

                call_rol = RolComponent.getUserRol(v_user_id)
                HandleLogs.write_log(f"Resultado búsqueda roles: {call_rol}")
                # HandleLogs.write_log(call_rol['data'])

                if call_rol['result']:
                    HandleLogs.write_log("Procesando roles...")
                    for rol in call_rol['data']:
                        HandleLogs.write_log(f"Procesando rol: {rol['rol_id']}")
                        call_modules = ModuleComponent.getModuleRol(rol['rol_id'])
                        HandleLogs.write_log(f"Resultado módulos: {call_modules}")
                        if call_modules['result']:
                            rol['modules'] = call_modules['data']
                            for module in call_modules['data']:
                                HandleLogs.write_log(f"Procesando módulo: {module['mod_id']}")
                                call_menu = MenuComponent.getMenuRolModule(rol['rol_id'], module['mod_id'])
                                HandleLogs.write_log(f"Resultado menús: {call_menu}")
                                if call_menu['result']:
                                    module['menu'] = call_menu['data']
                                else:
                                    HandleLogs.write_log(f"Error en menús: {call_menu['message']}")
                                    message = call_menu['message']
                                    exit()
                        else:
                            HandleLogs.write_log(f"Error en módulos: {call_modules['message']}")
                            message = call_modules['message']
                            exit()
                        # Get Carrer Periods
                        call_carrer_period = RolComponent.getCarrerPeriodRol(rol['rol_id'], v_user_id)
                        HandleLogs.write_log(f"Resultado carreras: {call_carrer_period}")
                        if call_carrer_period['result']:
                            rol['carrera_periodo'] = call_carrer_period['data']
                        else:
                            HandleLogs.write_log(f"Error en carreras: {call_carrer_period['message']}")
                            message = call_carrer_period['message']
                            exit()

                    data = {
                        'user': convert_datetime_to_string(resultado['data']),
                        'rols': call_rol['data']
                    }
                    result = True
                    HandleLogs.write_log("Login Exitoso para usuario: " + user)
                else:
                    HandleLogs.write_log(f"No se encontraron roles: {call_rol['message']}")
                    message = call_rol['message']
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }