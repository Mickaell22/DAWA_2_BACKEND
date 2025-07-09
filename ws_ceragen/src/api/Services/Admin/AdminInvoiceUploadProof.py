import os
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flask import send_file
from ....utils.general.logs import HandleLogs
from ....utils.general.response import response_success, response_error, response_unauthorize
from ...Components.Security.TokenComponent import TokenComponent

# Ruta donde se almacenarán las imágenes (puedes cambiarla según tu estructura)
UPLOAD_FOLDER = 'static/uploads/payment_proofs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class admin_Invoice_Upload_Proof(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if not token or not TokenComponent.Token_Validate(token):
                return response_unauthorize()

            if 'file' not in request.files:
                return response_error("No se encontró el archivo")

            file = request.files['file']
            if file.filename == '':
                return response_error("Nombre de archivo vacío")

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                # Retornar la ruta relativa (ej: /static/uploads/payment_proofs/imagen.png)
                ruta_relativa = f"/{filepath.replace(os.sep, '/')}"
                return response_success({"ruta": ruta_relativa})
            else:
                return response_error("Formato de archivo no permitido")

        except Exception as err:
            HandleLogs.write_error(f"Error al subir comprobante: {err}")
            return response_error("Error al procesar la imagen")


class admin_Invoice_Proof_Image(Resource):
    @staticmethod
    def get(nombre_archivo):
        try:
            ruta = os.path.join(UPLOAD_FOLDER, nombre_archivo)
            if not os.path.exists(ruta):
                return response_error("Imagen no encontrada")
            return send_file(ruta, mimetype='image/jpeg')
        except Exception as err:
            HandleLogs.write_error(f"Error al obtener imagen: {err}")
            return response_error("Error al servir la imagen")
