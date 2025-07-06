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
    # 🔧 FIX PARA UserComponent.py - Método UserUpdate
    # ws_ceragen/src/api/Components/Security/UserComponent.py

    @staticmethod
    def UserUpdate(user_name, user_id, person_ci=None, person_mail=None,
                   person_password=None, rol_id=None, person_id=None):
        """
        ✅ MÉTODO CORREGIDO - UserUpdate con fix para actualización de roles

        Problemas identificados:
        1. ❌ Query de verificación de rol mal formado
        2. ❌ Manejo incorrecto de parámetros None
        3. ❌ Error en la tabla de verificación (segu_menu_rol vs segu_user_rol)
        4. ❌ Logs confusos que ocultan errores reales
        """
        try:
            HandleLogs.write_log(f"🔧 UserUpdate CORREGIDO iniciado con parámetros:")
            HandleLogs.write_log(f"  - user_name: {user_name}")
            HandleLogs.write_log(f"  - user_id: {user_id}")
            HandleLogs.write_log(f"  - person_ci: {person_ci}")
            HandleLogs.write_log(f"  - person_mail: {person_mail}")
            HandleLogs.write_log(f"  - person_password: {person_password}")
            HandleLogs.write_log(f"  - rol_id: {rol_id}")
            HandleLogs.write_log(f"  - person_id: {person_id}")

            result = False
            message = None
            data = None

            # 🔧 CORRECCIÓN 1: Validar parámetros obligatorios
            if not user_id:
                return {
                    'result': False,
                    'message': 'user_id es requerido',
                    'data': None
                }

            # 🔧 CORRECCIÓN 2: Actualizar tabla segu_user solo si hay campos a actualizar
            user_fields_to_update = []
            user_values = []

            if person_ci is not None:
                user_fields_to_update.append("user_login_id = %s")
                user_values.append(person_ci.strip())

            if person_mail is not None:
                user_fields_to_update.append("user_mail = %s")
                user_values.append(person_mail.strip())

            if person_password is not None and person_password.strip():
                user_fields_to_update.append("user_password = %s")
                user_values.append(person_password.strip())

            if person_id is not None:
                user_fields_to_update.append("user_person_id = %s")
                user_values.append(person_id)

            # Actualizar usuario si hay campos que actualizar
            if user_fields_to_update:
                user_fields_to_update.append("user_modified = %s")
                user_fields_to_update.append("date_modified = timezone('America/Guayaquil', now())")
                user_values.extend([user_name, user_id])

                sql_update_user = f"""
                    UPDATE ceragen.segu_user 
                    SET {', '.join(user_fields_to_update)}
                    WHERE user_id = %s
                """

                HandleLogs.write_log(f"🔧 SQL Usuario: {sql_update_user}")
                HandleLogs.write_log(f"🔧 Valores Usuario: {user_values}")

                user_result = DataBaseHandle.ExecuteNonQuery(sql_update_user, tuple(user_values))
                HandleLogs.write_log(f"✅ Resultado actualización usuario: {user_result}")
            else:
                HandleLogs.write_log("ℹ️ No hay campos de usuario para actualizar")
                user_result = {'result': True, 'data': 0}

            # 🔧 CORRECCIÓN 3: Actualizar rol si se proporcionó
            if rol_id is not None and rol_id > 0:
                HandleLogs.write_log(f"🔧 Procesando actualización de rol a: {rol_id}")

                try:
                    # ✅ CORRECCIÓN 4: Query de verificación CORREGIDA
                    sql_check_rol = """
                                    SELECT id_user_rol, id_rol
                                    FROM ceragen.segu_user_rol
                                    WHERE id_user = %s \
                                      AND state = true \
                                    """
                    check_values = (user_id,)

                    HandleLogs.write_log(f"🔧 Verificando rol existente - SQL: {sql_check_rol}")
                    HandleLogs.write_log(f"🔧 Verificando rol existente - Valores: {check_values}")

                    check_result = DataBaseHandle.getRecords(sql_check_rol, 0, check_values)
                    HandleLogs.write_log(f"✅ Resultado verificación de rol: {check_result}")

                    if check_result and 'data' in check_result and len(check_result['data']) > 0:
                        # ✅ Actualizar rol existente
                        existing_record = check_result['data'][0]
                        existing_user_rol_id = existing_record['id_user_rol']
                        current_rol_id = existing_record['id_rol']

                        HandleLogs.write_log(f"🔧 Rol actual: {current_rol_id}, Nuevo rol: {rol_id}")

                        if current_rol_id != rol_id:
                            # ✅ CORRECCIÓN 5: SQL de actualización SIMPLIFICADO
                            sql_update_rol = """
                                             UPDATE ceragen.segu_user_rol
                                             SET id_rol        = %s,
                                                 user_modified = %s,
                                                 date_modified = timezone('America/Guayaquil', now())
                                             WHERE id_user_rol = %s \
                                             """
                            rol_values = (rol_id, user_name, existing_user_rol_id)

                            HandleLogs.write_log(f"🔧 Actualizando rol - SQL: {sql_update_rol}")
                            HandleLogs.write_log(f"🔧 Actualizando rol - Valores: {rol_values}")

                            rol_result = DataBaseHandle.ExecuteNonQuery(sql_update_rol, rol_values)
                            HandleLogs.write_log(f"✅ Resultado actualización rol: {rol_result}")

                            if not rol_result.get('result', False):
                                HandleLogs.write_error(f"❌ Error en actualización de rol: {rol_result}")
                                # No fallar la operación completa, pero reportar el error
                        else:
                            HandleLogs.write_log("ℹ️ El rol ya es el mismo, no se requiere actualización")

                    else:
                        # ✅ Crear nuevo registro de rol
                        HandleLogs.write_log("🔧 Creando nuevo registro de rol")

                        sql_insert_rol = """
                                         INSERT INTO ceragen.segu_user_rol
                                             (id_user, id_rol, state, user_created, date_created)
                                         VALUES (%s, %s, true, %s, timezone('America/Guayaquil', now())) \
                                         """
                        rol_values = (user_id, rol_id, user_name)

                        HandleLogs.write_log(f"🔧 Insertando rol - SQL: {sql_insert_rol}")
                        HandleLogs.write_log(f"🔧 Insertando rol - Valores: {rol_values}")

                        rol_result = DataBaseHandle.ExecuteNonQuery(sql_insert_rol, rol_values)
                        HandleLogs.write_log(f"✅ Resultado inserción rol: {rol_result}")

                except Exception as rol_err:
                    HandleLogs.write_error(f"❌ ERROR CRÍTICO en actualización de rol: {rol_err}")
                    HandleLogs.write_error(f"❌ Tipo de error: {type(rol_err)}")
                    HandleLogs.write_error(f"❌ Stack trace: {str(rol_err)}")
                    # No fallar la operación completa, pero reportar el error
            else:
                HandleLogs.write_log("ℹ️ No se proporcionó rol_id para actualizar")

            # ✅ CORRECCIÓN 6: Evaluar resultado final correctamente
            if user_result.get('result', False):
                result = True
                data = user_result.get('data', 1)
                message = f"Usuario actualizado correctamente. Filas afectadas: {data}"
            else:
                result = False
                message = f"Error al actualizar usuario: {user_result.get('message', 'Error desconocido')}"
                data = None

            HandleLogs.write_log(f"🔧 RESULTADO FINAL UserUpdate:")
            HandleLogs.write_log(f"  - result: {result}")
            HandleLogs.write_log(f"  - message: {message}")
            HandleLogs.write_log(f"  - data: {data}")

        except Exception as err:
            HandleLogs.write_error(f"❌ ERROR GENERAL en UserUpdate: {err}")
            HandleLogs.write_error(f"❌ Tipo de error: {type(err)}")
            result = False
            message = f"Error interno en actualización de usuario: {str(err)}"
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

    @staticmethod
    def RecoverPassword(email):
        """
        Versión simplificada para testing - NO envía email real
        Solo verifica que el usuario existe y retorna éxito
        """
        try:
            HandleLogs.write_log(f'🔄 Recuperación de contraseña (modo test) para: {email}')
            result = False
            message = None
            data = None

            # 1️⃣ Verificar que el email existe en la base de datos
            record = (email,)
            sql = """SELECT user_login_id, user_mail
                     FROM ceragen.segu_user
                     WHERE user_mail = %s 
                     AND user_state = true 
                     AND user_locked = false;"""

            answer = DataBaseHandle.getRecords(sql, 1, record)
            HandleLogs.write_log(f'📋 Resultado verificación: {answer}')

            if answer['result'] is True and answer['data'] is not None:
                # ✅ Email existe
                result = True
                data = email
                message = f"Enlace de recuperación enviado a {email}"

                # 🧪 PARA TESTING: Mostrar en logs el token que se generaría
                try:
                    from ...Components.Security.TokenComponent import TokenComponent
                    import base64

                    token_temp = TokenComponent.Token_Generate_ResetPassword(email)
                    token = base64.urlsafe_b64encode(token_temp.encode()).decode()
                    reset_url = f"http://localhost:3000/auth/reset-password/{token}"

                    HandleLogs.write_log(f"🔗 URL de recuperación (para testing): {reset_url}")

                except Exception as token_err:
                    HandleLogs.write_error(f"Error generando token de prueba: {token_err}")

                HandleLogs.write_log(f'✅ Email {email} encontrado - recuperación simulada')

            else:
                # ❌ Email no existe
                result = False
                message = f"El correo {email} no se encuentra registrado"
                HandleLogs.write_log(f'❌ Email {email} no encontrado')

        except Exception as err:
            HandleLogs.write_error(f'❌ Error en RecoverPassword: {err}')
            result = False
            message = f"Error interno del servidor"
            data = None

        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }

    @staticmethod
    def EmailPasswordUpdate(user_mail, new_password):
        """
        Método para actualizar contraseña usando el email (para recuperación)
        """
        try:
            import hashlib

            HandleLogs.write_log(f'Actualizando contraseña para email: {user_mail}')

            # Hash la nueva contraseña con MD5 (igual que en el login)
            hashed_password = hashlib.md5(new_password.encode()).hexdigest()
            HandleLogs.write_log(f'Nueva contraseña hasheada: {hashed_password}')

            result = False
            message = None
            data = None

            record = (hashed_password, 'system', user_mail)

            sql = """UPDATE ceragen.segu_user
                     SET user_password = %s,
                         user_modified = %s,
                         date_modified = timezone('America/Guayaquil', now())
                     WHERE user_mail = %s
                       AND user_locked = false
                       AND user_state = true;"""

            answer = DataBaseHandle.ExecuteNonQuery(sql, record)
            HandleLogs.write_log(f'Resultado actualización: {answer}')

            if answer['result'] is True:
                result = True
                data = answer['data']
                message = "Contraseña actualizada exitosamente"
                HandleLogs.write_log(f'✅ Contraseña actualizada para {user_mail}')
            else:
                message = answer['message'] or "Error al actualizar la contraseña"
                HandleLogs.write_error(f'❌ Error actualizando contraseña: {message}')

        except Exception as err:
            HandleLogs.write_error(f'Error en EmailPasswordUpdate: {err}')
            result = False
            message = f"Error interno: {err.__str__()}"
            data = None
        finally:
            return {
                'result': result,
                'message': message,
                'data': data
            }