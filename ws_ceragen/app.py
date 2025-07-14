import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from src.utils.general.logs import HandleLogs
from src.api.Routes.api_routes import load_routes

# IMPORTACIÓN PARA SISTEMA DE CITAS SIMPLIFICADO
from src.utils.database.simple_appointments import initialize_simple_appointments

app = Flask(__name__)
CORS(app)
api = Api(app)
load_routes(api)

# definiciones del swagger
SWAGGER_URL = '/ws/secoed/'
API_URL = '/static/swagger.json'

SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(SWAGGER_URL, API_URL,
                                              config={
                                                  'app_name': 'secoed-ws-restfulapi'
                                              })


@app.route('/health')
def health():
    return "OK", 200


app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def initialize_backend_systems():
    """
    Inicializar todos los sistemas del backend
    """
    try:
        HandleLogs.write_log("Inicializando sistemas del backend...")

        # Inicializar sistema de citas simplificado
        HandleLogs.write_log("Verificando sistema de citas simplificado...")
        if not initialize_simple_appointments():
            HandleLogs.write_error("ERROR CRITICO: Fallo la inicializacion del sistema de citas")
            return False

        HandleLogs.write_log("Todos los sistemas del backend inicializados correctamente")
        return True

    except Exception as err:
        HandleLogs.write_error(f"Error critico en inicializacion del backend: {str(err)}")
        return False


if __name__ == '__main__':
    try:
        HandleLogs.write_log("Servicio Iniciado")

        # Inicializar sistemas antes de arrancar el servidor
        HandleLogs.write_log("Inicializando sistemas del backend...")
        if not initialize_backend_systems():
            HandleLogs.write_error("Error critico en inicializacion. Cerrando aplicacion.")
            exit(1)

        HandleLogs.write_log("Arrancando servidor Flask...")
        port = int(os.environ.get('PORT', 8000))
        app.run(debug=True, host='0.0.0.0', port=port, threaded=True)
    except Exception as err:
        HandleLogs.write_error(err)
    finally:
        HandleLogs.write_log("Servicio Finalizado")