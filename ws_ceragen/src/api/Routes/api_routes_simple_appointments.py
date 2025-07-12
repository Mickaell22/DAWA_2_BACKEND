# Rutas específicas para citas simplificadas que coinciden con las esperadas por el frontend
from ..Services.Admin.SimpleAppointmentService import (
    SimpleAppointmentServiceV2_get,
    SimpleAppointmentServiceV2_getbyid,
    SimpleAppointmentServiceV2_schedule,
    SimpleAppointmentServiceV2_reschedule,
    SimpleAppointmentServiceV2_update,
    SimpleAppointmentServiceV2_cancel,
    SimpleAppointmentServiceV2_execute,
    SimpleAppointmentServiceV2_statistics,
    SimpleAppointmentServiceV2_by_therapist,
    SimpleAppointmentServiceV2_patients,
    SimpleAppointmentServiceV2_therapies,
    SimpleAppointmentServiceV2_therapists,
    SimpleAppointmentServiceV2_register_session,
)

def load_simple_appointments_routes(api):
    """
    Cargar rutas específicas para citas simplificadas que coinciden con el frontend
    """
    
    # ===============================================================================
    # 🎯 RUTAS EXACTAS QUE ESPERA EL FRONTEND
    # ===============================================================================
    
    # Ruta principal para listar citas (GET /admin/simple-appointments)
    api.add_resource(SimpleAppointmentServiceV2_get, '/admin/simple-appointments')
    
    # Ruta para agendar citas (POST /admin/simple-appointments/schedule)
    api.add_resource(SimpleAppointmentServiceV2_schedule, '/admin/simple-appointments/schedule')
    
    # Ruta para obtener cita específica (GET /admin/simple-appointments/{id})
    api.add_resource(SimpleAppointmentServiceV2_getbyid, '/admin/simple-appointments/<int:appointment_id>')
    
    # Ruta para actualizar cita (PUT /admin/simple-appointments/{id})
    api.add_resource(SimpleAppointmentServiceV2_update, '/admin/simple-appointments/<int:appointment_id>')
    
    # Ruta para cancelar cita (DELETE /admin/simple-appointments/{id})
    api.add_resource(SimpleAppointmentServiceV2_cancel, '/admin/simple-appointments/<int:appointment_id>')
    
    # Ruta para ejecutar cita (PATCH /admin/simple-appointments/execute/{id})
    api.add_resource(SimpleAppointmentServiceV2_execute, '/admin/simple-appointments/execute/<int:appointment_id>')
    
    # ===============================================================================
    # 🔧 RUTAS AUXILIARES ADICIONALES
    # ===============================================================================
    
    # Rutas auxiliares para formularios
    api.add_resource(SimpleAppointmentServiceV2_statistics, '/admin/simple-appointments/statistics')
    api.add_resource(SimpleAppointmentServiceV2_by_therapist, '/admin/simple-appointments/by-therapist/<string:therapist_name>')
    api.add_resource(SimpleAppointmentServiceV2_patients, '/admin/simple-appointments/patients')
    api.add_resource(SimpleAppointmentServiceV2_therapies, '/admin/simple-appointments/therapies')
    api.add_resource(SimpleAppointmentServiceV2_therapists, '/admin/simple-appointments/therapists')
    
    # Ruta para reagendar (PATCH /admin/simple-appointments/reschedule)
    api.add_resource(SimpleAppointmentServiceV2_reschedule, '/admin/simple-appointments/reschedule')
    api.add_resource(SimpleAppointmentServiceV2_register_session,
                     '/admin/simple-appointments/register-session/<int:appointment_id>')
