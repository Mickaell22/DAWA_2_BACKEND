from flask_restful import Resource
from flask import request
from .SimpleAppointmentService import (
    SimpleAppointmentServiceV2_get,
    SimpleAppointmentServiceV2_getbyid,
    SimpleAppointmentServiceV2_schedule,
    SimpleAppointmentServiceV2_update,
    SimpleAppointmentServiceV2_cancel,
    SimpleAppointmentServiceV2_execute
)

class SimpleAppointmentFrontendList(Resource):
    """Adaptador para GET /admin/simple-appointments"""
    
    def get(self):
        service = SimpleAppointmentServiceV2_get()
        return service.get()

class SimpleAppointmentFrontendById(Resource):
    """Adaptador para operaciones por ID en /admin/simple-appointments/{id}"""
    
    def get(self, appointment_id):
        service = SimpleAppointmentServiceV2_getbyid()
        return service.get(appointment_id)
    
    def put(self, appointment_id):
        service = SimpleAppointmentServiceV2_update()
        return service.put(appointment_id)
    
    def delete(self, appointment_id):
        service = SimpleAppointmentServiceV2_cancel()
        return service.delete(appointment_id)

class SimpleAppointmentFrontendSchedule(Resource):
    """Adaptador para POST /admin/simple-appointments/schedule"""
    
    def post(self):
        service = SimpleAppointmentServiceV2_schedule()
        return service.post()

class SimpleAppointmentFrontendExecute(Resource):
    """Adaptador para PATCH /admin/simple-appointments/execute/{id}"""
    
    def patch(self, appointment_id):
        service = SimpleAppointmentServiceV2_execute()
        return service.patch(appointment_id)