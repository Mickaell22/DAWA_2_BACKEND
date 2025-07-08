from flask_restful import Resource
from ...Components.Admin.AdminPatientComponent import AdminPatientComponent
from flask import request
from ....utils.general.response import response_success, response_error
from ....utils.general.logs import HandleLogs

class AdminPatientReportService(Resource):
    @staticmethod
    def get():
        try:
            estado = request.args.get('estado')  # Ejemplo: 'activo', 'inactivo'
            cliente = request.args.get('cliente')  # Ejemplo: id de cliente
            pacientes = AdminPatientComponent.report_patients(estado, cliente)
            return response_success(pacientes)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))