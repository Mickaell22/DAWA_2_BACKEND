from flask_restful import Resource
from flask import request
from ....utils.general.logs import HandleLogs
from ....utils.general.response import response_success, response_error, response_unauthorize
from ...Components.Security.TokenComponent import TokenComponent
from ....utils.database.connection_db import DataBaseHandle

def serialize_datetime(obj):
    """
    Convierte cualquier campo datetime en string ISO para evitar errores de serialización JSON.
    """
    if isinstance(obj, dict):
        return {k: serialize_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_datetime(i) for i in obj]
    elif hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        return obj

class AdminClientService_list(Resource):
    @staticmethod
    def get():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            # Solo selecciona los campos necesarios para el frontend
            query = """
                SELECT cli_id, cli_name, cli_identification, cli_state
                FROM ceragen.admin_client
                WHERE cli_state = TRUE
            """
            clients = DataBaseHandle.getRecords(query, 0)
            clients = serialize_datetime(clients)
            return response_success(clients)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminClientService_getbyid(Resource):
    @staticmethod
    def get(cli_id):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            query = """
                SELECT cli_id, cli_name, cli_identification, cli_state
                FROM ceragen.admin_client
                WHERE cli_id = %s
            """
            client = DataBaseHandle.getRecord(query, (cli_id,))
            client = serialize_datetime(client)
            if client:
                return response_success(client)
            else:
                return response_error("Cliente no encontrado")
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminClientService_add(Resource):
    @staticmethod
    def post():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            data = request.get_json()
            query = """
                INSERT INTO ceragen.admin_client
                (cli_person_id, cli_identification, cli_name, cli_address_bill, cli_mail_bill, cli_state, user_created, date_created)
                VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                RETURNING cli_id
            """
            params = (
                data.get('cli_person_id'),
                data.get('cli_identification'),
                data.get('cli_name'),
                data.get('cli_address_bill'),
                data.get('cli_mail_bill'),
                data.get('cli_state', True),
                data.get('user_created')
            )
            new_id = DataBaseHandle.insertRecord(query, params)
            return response_success({'cli_id': new_id})
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminClientService_update(Resource):
    @staticmethod
    def patch():
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            data = request.get_json()
            query = """
                UPDATE ceragen.admin_client
                SET cli_person_id=%s, cli_identification=%s, cli_name=%s, cli_address_bill=%s, cli_mail_bill=%s, cli_state=%s, user_modified=%s, date_modified=NOW()
                WHERE cli_id=%s
            """
            params = (
                data.get('cli_person_id'),
                data.get('cli_identification'),
                data.get('cli_name'),
                data.get('cli_address_bill'),
                data.get('cli_mail_bill'),
                data.get('cli_state', True),
                data.get('user_modified'),
                data.get('cli_id')
            )
            DataBaseHandle.updateRecord(query, params)
            return response_success("Cliente actualizado correctamente")
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))

class AdminClientService_delete(Resource):
    @staticmethod
    def delete(cli_id, user):
        try:
            token = request.headers.get('tokenapp')
            if not token:
                return response_error("Error: No se ha podido Obtener el Token")
            token_valido = TokenComponent.Token_Validate(token)
            if not token_valido:
                return response_unauthorize()
            query = """
                UPDATE ceragen.admin_client
                SET cli_state=FALSE, user_deleted=%s, date_deleted=NOW()
                WHERE cli_id=%s
            """
            params = (user, cli_id)
            DataBaseHandle.updateRecord(query, params)
            return response_success("Cliente eliminado correctamente")
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))