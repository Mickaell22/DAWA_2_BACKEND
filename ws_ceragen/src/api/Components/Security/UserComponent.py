from ....utils.general.logs import HandleLogs
from ....utils.database.connection_db import DataBaseHandle
from .UserRolComponent import UserRolComponent
from ....api.Components.Security.rolComponent import RolComponent
from ....api.Components.Security.moduleComponent import ModuleComponent
from ....api.Components.Security.menuComponent import MenuComponent
from datetime import datetime
from ....utils.smpt.smpt_officeUG import send_password_recovery_email



class UserComponent:

    @staticmethod
    def ListAllUsers():
        try:
            result = False
            message = None
            data = None
            sql = """SELECT u.user_id,
                            u.user_person_id,
                            u.user_login_id,
                            u.user_mail,
                            u.user_state,
                            ur.id_rol as user_rol_id
                     FROM ceragen.segu_user u
                              LEFT JOIN ceragen.segu_user_rol ur ON u.user_id = ur.id_user AND ur.state = true
                     WHERE u.user_state = true;"""
            resultado = DataBaseHandle.getRecords(sql, 0)
            HandleLogs.write_log(resultado)
            if resultado['data'] is None:
                result = False
                message = "Error al Busar Datos"

                HandleLogs.write_error("Error al Busar Datos")
            else:
                result = True
                data = resultado['data']

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
    def ListUserId(user_token):
        try:
            def convert_datetime_to_string(data):
                for key, value in data.items():
                    if isinstance(value, datetime):
                        data[key] = value.isoformat()
                return data

            result = False
            message = None
            data = None
            sql = "select us.user_id, us.user_login_id,us.user_mail , per_names, per_surnames, user_locked, user_last_login " \
                  "from ceragen.segu_user us " \
                  "inner join ceragen.admin_person pe on us.user_person_id = pe.per_id " \
                  "where user_login_id = %s " \
                  "and user_state = true and user_locked = false;"
            record = (user_token,)

            resultado = DataBaseHandle.getRecords(sql, 1, record)
            HandleLogs.write_log(resultado)
            message = resultado['message']
            if resultado['data'] is None:
                if resultado['message'] is not None: message = resultado['message']
                message = "Usuario " + str(user_token) + " no encontrado"
                HandleLogs.write_error(message)
            else:
                v_user_id = resultado['data']['user_id']
                call_rol = RolComponent.getUserRol(v_user_id)

                if call_rol['result']:
                    for rol in call_rol['data']:
                        call_modules = ModuleComponent.getModuleRol(rol['rol_id'])
                        if call_modules['result']:
                            rol['modules'] = call_modules['data']
                            for module in call_modules['data']:
                                call_menu = MenuComponent.getMenuRolModule(rol['rol_id'], module['mod_id'])
                                if call_menu['result']:
                                    module['menu'] = call_menu['data']
                                else:
                                    message = call_menu['message']
                                    exit()
                        else:
                            message = call_modules['message']
                            exit()
                        # Get Carrer Periods
                        call_carrer_period = RolComponent.getCarrerPeriodRol(rol['rol_id'], v_user_id)
                        if call_carrer_period['result']:
                            rol['carrera_periodo'] = call_carrer_period['data']
                        else:
                            message = call_carrer_period['message']
                            exit()

                    data = {
                        'user': convert_datetime_to_string(resultado['data']),
                        'rols': call_rol['data']
                    }
                    result = True
                    HandleLogs.write_log("Login Exitoso para usuario: " + user_token)
                else:
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

    @staticmethod
    def UserInsert(person_id, person_ci, person_password, person_mail, user_id, rol_id, id_career_period):
        try:
            import hashlib

            # 🔧 HASHEAR LA CONTRASEÑA CON MD5 (mismo método que usa Login)
            hashed_password = hashlib.md5(person_password.encode()).hexdigest()

            HandleLogs.write_log(f"UserInsert iniciado con:")
            HandleLogs.write_log(f"  - person_id: {person_id}")
            HandleLogs.write_log(f"  - person_ci: {person_ci}")
            HandleLogs.write_log(f"  - person_mail: {person_mail}")
            HandleLogs.write_log(f"  - password original: {person_password}")
            HandleLogs.write_log(f"  - password hasheado: {hashed_password}")
            HandleLogs.write_log(f"  - user_id: {user_id}")
            HandleLogs.write_log(f"  - rol_id: {rol_id}")
            HandleLogs.write_log(f"  - id_career_period: {id_career_period}")

            # 🔧 USAR LA CONTRASEÑA HASHEADA EN LUGAR DE LA ORIGINAL
            record = (person_id, person_ci, person_mail, hashed_password, user_id, user_id)

            data = None
            sql = """
                  INSERT INTO ceragen.segu_user(user_person_id, user_login_id, user_mail, user_password, user_created, \
                                                date_created, login_attempts)
                  VALUES (%s, %s, %s, %s, %s, timezone('America/Guayaquil', now()), 0) ON CONFLICT (user_login_id)
                    DO \
                  UPDATE SET
                      user_state = TRUE, \
                      user_modified = %s, \
                      date_modified = timezone('America/Guayaquil', now()) \
                      RETURNING user_id \
                  """

            HandleLogs.write_log(f"SQL de inserción: {sql}")
            HandleLogs.write_log(f"Parámetros: {record}")

            resultado = DataBaseHandle.ExecuteInsert(sql, record)
            result = resultado['result']
            message = resultado['message']

            HandleLogs.write_log(f"Resultado de inserción de usuario: {resultado}")

            if resultado['data'] is not None:
                value = resultado['data'][0]
                result = True
                data = list(value.values())[0]
                HandleLogs.write_log(f"Usuario insertado con ID: {data}")

                # Insertar rol si se proporcionó
                if rol_id > 0:
                    HandleLogs.write_log(f"Insertando rol {rol_id} para usuario {data}")
                    response_insert_rol_period = UserRolComponent.UserRolInsert(rol_id, data, id_career_period, user_id)
                    HandleLogs.write_log(f"Resultado inserción rol: {response_insert_rol_period}")

        except Exception as err:
            HandleLogs.write_error(f"Error en UserInsert: {err}")
            message = err.__str__()
            result = False
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def UserDelete(user, user_id):
        try:
            record = (user, user_id)
            result = False
            message = None
            data = None
            sql = """UPDATE ceragen.segu_user
                     SET user_state= False,
                         user_deleted=%s,
                         date_deleted=timezone('America/Guayaquil', now())
                     WHERE user_id = %s;"""
            answer = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log(answer)
            if answer['result'] is True:
                result = True
                data = answer['data']

        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def UserUpdate(user_name, user_id, person_ci=None, person_mail=None,
                   person_password=None, rol_id=None, person_id=None):
        """
        Método actualizado para soportar todos los campos de edición
        Mantiene compatibilidad con llamadas que solo pasan user_name y user_id
        """
        try:
            HandleLogs.write_log(f"UserUpdate iniciado con parámetros:")
            HandleLogs.write_log(f"  - user_name: {user_name}")
            HandleLogs.write_log(f"  - user_id: {user_id}")
            HandleLogs.write_log(f"  - person_ci: {person_ci}")
            HandleLogs.write_log(f"  - person_mail: {person_mail}")
            HandleLogs.write_log(f"  - person_password: {'***' if person_password else None}")
            HandleLogs.write_log(f"  - rol_id: {rol_id}")
            HandleLogs.write_log(f"  - person_id: {person_id}")

            result = False
            message = None
            data = None

            # Si no se proporcionan campos adicionales, usar comportamiento legacy
            if all(param is None for param in [person_ci, person_mail, person_password, rol_id, person_id]):
                HandleLogs.write_log("Usando comportamiento legacy (solo toggle user_locked)")
                record = (user_name, user_id)
                sql = """UPDATE ceragen.segu_user
                         SET user_locked    = CASE WHEN user_locked = FALSE THEN TRUE ELSE FALSE END,
                             login_attempts = CASE WHEN user_locked = FALSE THEN 3 ELSE 0 END,
                             user_modified  = %s,
                             date_modified  = timezone('America/Guayaquil', now())
                         WHERE user_id = %s; \
                      """
                answer = DataBaseHandle.ExecuteNonQuery(sql, record)

            else:
                # Nuevo comportamiento: actualizar campos específicos
                HandleLogs.write_log("Usando nuevo comportamiento (actualizar campos específicos)")

                # Construir query dinámicamente
                update_fields = []
                update_values = []

                if person_ci is not None and str(person_ci).strip():
                    update_fields.append("user_login_id = %s")
                    update_values.append(str(person_ci).strip())
                    HandleLogs.write_log(f"Actualizando user_login_id a: {person_ci}")

                if person_mail is not None:
                    update_fields.append("user_mail = %s")
                    update_values.append(str(person_mail).strip() if person_mail else "")
                    HandleLogs.write_log(f"Actualizando user_mail a: {person_mail}")

                if person_password is not None and str(person_password).strip():
                    # Usar el mismo método de encriptación que usas en el sistema
                    import hashlib
                    encrypted_password = hashlib.sha256(str(person_password).encode()).hexdigest()
                    update_fields.append("user_password = %s")
                    update_values.append(encrypted_password)
                    HandleLogs.write_log("Actualizando user_password (encriptada)")

                if person_id is not None:
                    update_fields.append("user_person_id = %s")
                    update_values.append(int(person_id))
                    HandleLogs.write_log(f"Actualizando user_person_id a: {person_id}")

                # Agregar campos de auditoría
                update_fields.append("user_modified = %s")
                update_fields.append("date_modified = timezone('America/Guayaquil', now())")
                update_values.append(user_name)

                # Agregar user_id para la cláusula WHERE
                update_values.append(user_id)

                if len(update_fields) <= 2:  # Solo campos de auditoría
                    HandleLogs.write_log("No hay campos reales para actualizar")
                    result = True
                    data = 0
                    message = "No se proporcionaron campos para actualizar"
                else:
                    # Construir y ejecutar la query
                    sql = f"""
                        UPDATE ceragen.segu_user 
                        SET {', '.join(update_fields)}
                        WHERE user_id = %s AND user_state = true
                    """

                    HandleLogs.write_log(f"SQL generada: {sql}")
                    HandleLogs.write_log(f"Valores: {update_values}")

                    answer = DataBaseHandle.ExecuteNonQuery(sql, update_values)

                    # 🔧 ACTUALIZAR ROL SI SE PROPORCIONÓ
                    if rol_id is not None and answer.get('result') and answer.get('data', 0) > 0:
                        HandleLogs.write_log(f"Actualizando rol del usuario a rol_id: {rol_id}")

                        try:
                            # Verificar si ya existe un rol activo
                            sql_check = """
                                        SELECT id_user_rol
                                        FROM ceragen.segu_user_rol
                                        WHERE id_user = %s \
                                          AND state = true LIMIT 1 \
                                        """

                            check_result = DataBaseHandle.getRecords(sql_check, 1, (user_id,))
                            HandleLogs.write_log(f"Verificación de rol existente: {check_result}")

                            if check_result.get('data') and len(check_result['data']) > 0:
                                # Actualizar rol existente
                                existing_user_rol_id = check_result['data'][0]['id_user_rol']
                                sql_update_rol = """
                                                 UPDATE ceragen.segu_user_rol
                                                 SET id_rol        = %s,
                                                     user_modified = %s,
                                                     date_modified = timezone('America/Guayaquil', now())
                                                 WHERE id_user_rol = %s \
                                                 """
                                rol_values = (rol_id, user_name, existing_user_rol_id)
                                rol_result = DataBaseHandle.ExecuteNonQuery(sql_update_rol, rol_values)
                                HandleLogs.write_log(f"Resultado actualización rol: {rol_result}")

                            else:
                                # Crear nuevo rol
                                sql_insert_rol = """
                                                 INSERT INTO ceragen.segu_user_rol
                                                     (id_user, id_rol, state, user_created, date_created)
                                                 VALUES (%s, %s, true, %s, timezone('America/Guayaquil', now())) \
                                                 """
                                rol_values = (user_id, rol_id, user_name)
                                rol_result = DataBaseHandle.ExecuteNonQuery(sql_insert_rol, rol_values)
                                HandleLogs.write_log(f"Resultado inserción rol: {rol_result}")

                        except Exception as rol_err:
                            HandleLogs.write_error(f"Error actualizando rol: {rol_err}")
                            # No fallar la operación completa por un error de rol

            # Procesar resultado
            HandleLogs.write_log(f"Resultado de ExecuteNonQuery: {answer}")

            if answer.get('result') is True:
                result = True
                data = answer.get('data', 0)
                if data > 0:
                    message = f"Usuario actualizado correctamente. Filas afectadas: {data}"
                else:
                    message = "No se encontraron cambios para realizar"
            else:
                message = answer.get('message', "Error al actualizar usuario")

        except Exception as err:
            HandleLogs.write_error(f"Error en UserUpdate: {err}")
            message = err.__str__()
            data = None

        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def UserUpdate_time_login(user_id):
        try:
            result = False
            message = None
            data = None
            sql = "UPDATE ceragen.segu_user SET user_last_login = timezone('America/Guayaquil', now() ), login_attempts =  0 WHERE user_login_id = %s"
            record = (user_id,)
            answer = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log(answer)
            if answer['result'] is True:
                result = True
                data = answer['data']

        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def UserPasswordUpdate(new_password, user, user_id, old_password):
        try:
            HandleLogs.write_log('new_password' + new_password)
            HandleLogs.write_log('user' + user)
            HandleLogs.write_log('user_id' + str(user_id))
            HandleLogs.write_log('old' + old_password)
            record = (new_password, user, user_id, old_password)
            result = False
            message = None
            data = None
            sql = """UPDATE ceragen.segu_user
                     SET user_password=%s,
                         user_modified=%s,
                         date_modified=timezone('America/Guayaquil', now())
                     WHERE user_id = %s
                       AND user_password = %s
                       AND user_locked = false
                       AND user_state = true; \
                  """
            answer = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log(answer)
            if answer['result'] is True:
                result = True
                data = answer['data']
            else:
                message = answer['message']
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def UserMailPassword(email):
        try:
            HandleLogs.write_log('email: ' + email)
            result = False
            message = None
            data = None
            record = (email,)
            sql = """ SELECT user_login_id
                      FROM ceragen.segu_user
                      WHERE user_mail = %s; \
                  """
            answer = DataBaseHandle.getRecords(sql, 1, record)
            HandleLogs.write_log(answer)
            if answer['result'] is True and answer['data'] is not None:
                answer_to_send = send_password_recovery_email(email)
                result = answer_to_send['result']
                data = answer_to_send['data']
                message = answer_to_send['message']
            else:
                HandleLogs.write_log(answer['message'])
                message = (
                    f"El correo {email} no se encuentra registrado" if answer['message'] is None else answer['message']
                )
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def UsePaswoedUpdateMail(user_id, new_password, user_mail):
        try:

            record = (new_password, user_id, user_id, user_mail)
            result = False
            message = None
            data = None
            sql = """UPDATE ceragen.segu_user
                     SET user_password = %s,
                         user_modified = %s,
                         date_modified = timezone('America/Guayaquil', now())
                     WHERE user_login_id = %s
                       AND user_mail = %s; \
                  """
            answer = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log(answer)
            if answer['result'] is True:
                result = True
                data = answer['data']
            else:
                message = answer['message']
        except Exception as err:
            HandleLogs.write_error(err)
            message = err.__str__()
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }
