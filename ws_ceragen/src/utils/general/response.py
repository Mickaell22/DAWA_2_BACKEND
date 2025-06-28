
def response_inserted(datos):
    return {
        'result': True,
        'message': "Registro Insertado con éxito",
        'data': datos,
        'status_code': 201,
    }, 201

def response_not_found(message="No encontrado"):
    return {
        'result': False,
        'message': message,
        'data': []
    }, 404

def response_success(datos):
    return {
        'result': True,
        'message': "Exitoso",
        'data': datos,
        'status_code': 200,
    }, 200

def response_error(mensaje):
    return {
        'result': False,
        'message': mensaje,
        'data': {},
        'status_code': 500,
    }, 500


def response_unauthorize():
    return {
        'result': False,
        'message': "Acceso No autorizado",
        'data': {},
        'status_code': 401,
    }, 401

def internal_response(result, message, data):
    return{
        'result': result,
        'message': message,
        'data': data
    }
def response_success_personal(result, message,data):
    return {
        'result': result,
        'message': message,
        'data': data,
        'status_code': 200,
    }, 200
