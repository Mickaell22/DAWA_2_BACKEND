import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from .connection_db import DataBaseHandle
from ..general.logs import HandleLogs


class SimpleAppointmentTableInit:
    """Clase para inicializar la tabla simplificada de citas"""

    @staticmethod
    def check_and_create_table():
        """
        Verifica si existe la tabla clinic_session_control1, si no la crea
        """
        try:
            HandleLogs.write_log("Verificando tabla clinic_session_control1...")

            # DEBUG: Verificar conexión de base de datos
            try:
                HandleLogs.write_log("DEBUG: Probando conexion a base de datos...")
                test_query = "SELECT 1 as test;"
                test_response = DataBaseHandle.getRecords(test_query, 0)

                if test_response['result']:
                    HandleLogs.write_log(f"DEBUG: Conexion exitosa, resultado: {test_response['data']}")
                else:
                    HandleLogs.write_error(f"ERROR DE CONEXION DB: {test_response['message']}")
                    return False

            except Exception as db_err:
                HandleLogs.write_error(f"ERROR DE CONEXION DB: {str(db_err)}")
                return False

            # Verificar si la tabla existe
            HandleLogs.write_log("DEBUG: Verificando si tabla existe...")
            check_table_sql = """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'ceragen' 
                    AND table_name = 'clinic_session_control1'
                );
            """

            try:
                response = DataBaseHandle.getRecords(check_table_sql, 0)
                HandleLogs.write_log(
                    f"DEBUG: Response verificacion tabla: result={response['result']}, data={response['data']}")

                if not response['result']:
                    HandleLogs.write_error(f"ERROR: La consulta fallo: {response['message']}")
                    return False

                if not response['data'] or len(response['data']) == 0:
                    HandleLogs.write_error("ERROR: La consulta no devolvio resultados")
                    return False

                table_exists = response['data'][0]['exists']
                HandleLogs.write_log(f"DEBUG: Tabla existe: {table_exists}")

            except Exception as check_err:
                HandleLogs.write_error(f"ERROR al verificar tabla: {str(check_err)}")
                return False

            if table_exists:
                HandleLogs.write_log("Tabla clinic_session_control1 ya existe")
                return True

            HandleLogs.write_log("Tabla clinic_session_control1 no existe, creando...")

            # Verificar si el schema 'ceragen' existe
            HandleLogs.write_log("DEBUG: Verificando schema ceragen...")
            schema_check_sql = """
                SELECT EXISTS (
                    SELECT FROM information_schema.schemata 
                    WHERE schema_name = 'ceragen'
                );
            """

            try:
                schema_response = DataBaseHandle.getRecords(schema_check_sql, 0)

                if schema_response['result'] and schema_response['data']:
                    schema_exists = schema_response['data'][0]['exists']
                    HandleLogs.write_log(f"DEBUG: Schema ceragen existe: {schema_exists}")

                    if not schema_exists:
                        HandleLogs.write_log("Creando schema ceragen...")
                        create_schema_response = DataBaseHandle.ExecuteNonQuery("CREATE SCHEMA IF NOT EXISTS ceragen;",
                                                                                ())

                        if create_schema_response['result']:
                            HandleLogs.write_log("Schema ceragen creado")
                        else:
                            HandleLogs.write_error(f"ERROR creando schema: {create_schema_response['message']}")
                            return False
                else:
                    HandleLogs.write_error(f"ERROR verificando schema: {schema_response['message']}")
                    return False

            except Exception as schema_err:
                HandleLogs.write_error(f"ERROR con schema: {str(schema_err)}")
                return False

            # SQL para crear la tabla
            HandleLogs.write_log("DEBUG: Creando tabla...")
            create_table_sql = """
                CREATE TABLE IF NOT EXISTS ceragen.clinic_session_control1 (
                    sec_id SERIAL PRIMARY KEY,
                    -- Información básica del paciente (sin FK compleja)
                    patient_name VARCHAR(200) NOT NULL,
                    patient_phone VARCHAR(20),
                    patient_email VARCHAR(100),
                    patient_id INTEGER,

                    -- Información de la sesión (simplificada)
                    sec_ses_number INTEGER NOT NULL DEFAULT 1,
                    sec_ses_agend_date TIMESTAMP NOT NULL,
                    sec_ses_exec_date TIMESTAMP,

                    -- Información de terapia (como texto libre)
                    therapy_name VARCHAR(200),
                    therapy_type VARCHAR(100),

                    -- Personal médico (como texto libre)
                    therapist_name VARCHAR(200),
                    therapist_specialty VARCHAR(100),

                    -- Estados simples
                    ses_consumed BOOLEAN DEFAULT FALSE,
                    ses_state BOOLEAN DEFAULT TRUE,
                    status VARCHAR(20) DEFAULT 'scheduled',

                    -- Información adicional
                    duration_minutes INTEGER DEFAULT 60,
                    notes TEXT,
                    price DECIMAL(10,2),

                    -- Auditoría básica
                    user_created VARCHAR(100) NOT NULL,
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_modified VARCHAR(100),
                    date_modified TIMESTAMP,
                    user_deleted VARCHAR(100),
                    date_deleted TIMESTAMP
                );
            """

            try:
                # Crear la tabla
                table_response = DataBaseHandle.ExecuteNonQuery(create_table_sql, ())

                if table_response['result']:
                    HandleLogs.write_log(f"DEBUG: Tabla creada exitosamente, resultado: {table_response['data']}")
                else:
                    HandleLogs.write_error(f"ERROR al crear tabla: {table_response['message']}")
                    return False

            except Exception as table_err:
                HandleLogs.write_error(f"ERROR al crear tabla: {str(table_err)}")
                return False

            # Crear índices
            HandleLogs.write_log("DEBUG: Creando indices...")
            indexes_sql = [
                "CREATE INDEX IF NOT EXISTS idx_clinic_session_control1_date ON ceragen.clinic_session_control1(sec_ses_agend_date);",
                "CREATE INDEX IF NOT EXISTS idx_clinic_session_control1_patient ON ceragen.clinic_session_control1(patient_name);",
                "CREATE INDEX IF NOT EXISTS idx_clinic_session_control1_status ON ceragen.clinic_session_control1(status);",
                "CREATE INDEX IF NOT EXISTS idx_clinic_session_control1_state ON ceragen.clinic_session_control1(ses_state);"
            ]

            for i, index_sql in enumerate(indexes_sql):
                try:
                    index_response = DataBaseHandle.ExecuteNonQuery(index_sql, ())

                    if index_response['result']:
                        HandleLogs.write_log(f"DEBUG: Indice {i + 1} creado exitosamente")
                    else:
                        HandleLogs.write_error(f"ERROR creando indice {i + 1}: {index_response['message']}")

                except Exception as idx_err:
                    HandleLogs.write_error(f"ERROR creando indice {i + 1}: {str(idx_err)}")

            # Crear función de trigger para date_modified
            HandleLogs.write_log("DEBUG: Creando trigger function...")
            trigger_function_sql = """
                CREATE OR REPLACE FUNCTION ceragen.update_modified_time_clinic_session_control1()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.date_modified = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
            """

            try:
                func_response = DataBaseHandle.ExecuteNonQuery(trigger_function_sql, ())

                if func_response['result']:
                    HandleLogs.write_log("DEBUG: Trigger function creada exitosamente")
                else:
                    HandleLogs.write_error(f"ERROR creando trigger function: {func_response['message']}")

            except Exception as func_err:
                HandleLogs.write_error(f"ERROR creando trigger function: {str(func_err)}")

            # Crear trigger
            HandleLogs.write_log("DEBUG: Creando trigger...")
            trigger_sql = """
                DROP TRIGGER IF EXISTS trigger_update_modified_clinic_session_control1 ON ceragen.clinic_session_control1;
                CREATE TRIGGER trigger_update_modified_clinic_session_control1
                    BEFORE UPDATE ON ceragen.clinic_session_control1
                    FOR EACH ROW
                    EXECUTE FUNCTION ceragen.update_modified_time_clinic_session_control1();
            """

            try:
                trigger_response = DataBaseHandle.ExecuteNonQuery(trigger_sql, ())

                if trigger_response['result']:
                    HandleLogs.write_log("DEBUG: Trigger creado exitosamente")
                else:
                    HandleLogs.write_error(f"ERROR creando trigger: {trigger_response['message']}")

            except Exception as trig_err:
                HandleLogs.write_error(f"ERROR creando trigger: {str(trig_err)}")

            HandleLogs.write_log("Tabla clinic_session_control1 creada exitosamente con indices y triggers")

            # Insertar datos de ejemplo (opcional)
            SimpleAppointmentTableInit.insert_sample_data()

            return True

        except Exception as err:
            HandleLogs.write_error(f"ERROR GENERAL al verificar/crear tabla: {str(err)}")
            HandleLogs.write_error(f"TIPO DE ERROR: {type(err).__name__}")
            return False

    @staticmethod
    def insert_sample_data():
        """Insertar algunos datos de ejemplo para testing"""
        try:
            HandleLogs.write_log("DEBUG: Insertando datos de ejemplo...")

            sample_data_sql = """
                INSERT INTO ceragen.clinic_session_control1 
                (patient_name, patient_phone, patient_email, sec_ses_agend_date, 
                 therapy_name, therapy_type, therapist_name, therapist_specialty, 
                 duration_minutes, price, user_created) 
                VALUES 
                ('Juan Perez', '0999123456', 'juan@email.com', 
                 CURRENT_TIMESTAMP + INTERVAL '1 day', 
                 'Fisioterapia General', 'Rehabilitacion', 
                 'Dr. Maria Gonzalez', 'Fisioterapeuta', 
                 60, 25.00, 'system'),

                ('Ana Garcia', '0987654321', 'ana@email.com', 
                 CURRENT_TIMESTAMP + INTERVAL '2 days', 
                 'Masoterapia', 'Relajacion', 
                 'Lic. Pedro Silva', 'Masajista', 
                 45, 20.00, 'system'),

                ('Carlos Lopez', '0912345678', 'carlos@email.com', 
                 CURRENT_TIMESTAMP + INTERVAL '3 days', 
                 'Acupuntura', 'Medicina Alternativa', 
                 'Dr. Luis Castro', 'Acupunturista', 
                 30, 30.00, 'system')
                ON CONFLICT DO NOTHING;
            """

            response = DataBaseHandle.ExecuteNonQuery(sample_data_sql, ())

            if response['result']:
                HandleLogs.write_log(
                    f"DEBUG: Datos de ejemplo insertados exitosamente, filas afectadas: {response['data']}")
            else:
                HandleLogs.write_log(f"Los datos de ejemplo ya existen o hubo un error: {response['message']}")

        except Exception as err:
            HandleLogs.write_error(f"Error al insertar datos de ejemplo: {str(err)}")

    @staticmethod
    def migrate_existing_data():
        """
        Migrar datos existentes de clinic_session_control a clinic_session_control1
        (Solo si se requiere)
        """
        try:
            HandleLogs.write_log("Iniciando migracion de datos existentes...")

            # Verificar si hay datos en la tabla original
            check_data_sql = """
                SELECT COUNT(*) as total FROM ceragen.clinic_session_control 
                WHERE ses_state = true;
            """

            response = DataBaseHandle.getRecords(check_data_sql, 0)

            if response['result'] and response['data']:
                total_records = response['data'][0]['total']
            else:
                total_records = 0

            if total_records == 0:
                HandleLogs.write_log("No hay datos para migrar")
                return True

            HandleLogs.write_log(f"Encontrados {total_records} registros para migrar")

            # Migración simplificada - solo los campos básicos
            migration_sql = """
                INSERT INTO ceragen.clinic_session_control1 
                (patient_name, sec_ses_number, sec_ses_agend_date, sec_ses_exec_date,
                 ses_consumed, ses_state, user_created, date_created)
                SELECT 
                    CONCAT('Paciente ID: ', sc.sec_inv_id) as patient_name,
                    sc.sec_ses_number,
                    sc.sec_ses_agend_date,
                    sc.sec_ses_exec_date,
                    sc.ses_consumed,
                    sc.ses_state,
                    sc.user_created,
                    sc.date_created
                FROM ceragen.clinic_session_control sc
                WHERE sc.ses_state = true
                AND NOT EXISTS (
                    SELECT 1 FROM ceragen.clinic_session_control1 sc1 
                    WHERE sc1.sec_ses_agend_date = sc.sec_ses_agend_date 
                    AND sc1.user_created = sc.user_created
                );
            """

            migration_response = DataBaseHandle.ExecuteNonQuery(migration_sql, ())

            if migration_response['result']:
                HandleLogs.write_log(f"Migracion completada: {migration_response['data']} registros migrados")
            else:
                HandleLogs.write_error(f"Error en migracion: {migration_response['message']}")

            return True

        except Exception as err:
            HandleLogs.write_error(f"Error en migracion: {str(err)}")
            return False


# Función para ejecutar al inicio del backend
def initialize_simple_appointments():
    """
    Función principal que se ejecuta al iniciar el backend
    """
    try:
        HandleLogs.write_log("Inicializando sistema de citas simplificado...")

        # Verificar y crear tabla
        if not SimpleAppointmentTableInit.check_and_create_table():
            HandleLogs.write_error("Fallo la inicializacion de la tabla")
            return False

        HandleLogs.write_log("Sistema de citas simplificado inicializado correctamente")
        return True

    except Exception as err:
        HandleLogs.write_error(f"Error en inicializacion: {str(err)}")
        return False


# Para ejecutar directamente desde línea de comandos
if __name__ == "__main__":
    initialize_simple_appointments()