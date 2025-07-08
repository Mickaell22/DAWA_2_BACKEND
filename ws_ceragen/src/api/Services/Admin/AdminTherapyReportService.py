from flask_restful import Resource
from ...Components.Admin.AdminTherapyComponent import AdminTherapyComponent
from flask import request
from ....utils.general.response import response_success, response_error
from ....utils.general.logs import HandleLogs

class AdminTherapyReportService(Resource):
    @staticmethod
    def get():
        try:
            nombre = request.args.get('nombre')    # filtrar por nombre parcial
            estado = request.args.get('estado')    # activo / inactivo
            terapias = AdminTherapyComponent.report_therapy_types(nombre, estado)
            return response_success(terapias)
        except Exception as err:
            HandleLogs.write_error(err)
            return response_error(str(err))
