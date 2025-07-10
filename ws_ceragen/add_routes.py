#!/usr/bin/env python3

# Script para agregar las rutas de citas simplificadas al archivo api_routes.py

import os

# Contenido a agregar en imports
imports_to_add = """
# 🎯 SERVICIOS ADAPTADORES PARA CITAS SIMPLIFICADAS (FRONTEND)
from ..Services.Admin.SimpleAppointmentFrontendAdapter import (
    SimpleAppointmentFrontendList,
    SimpleAppointmentFrontendById,
    SimpleAppointmentFrontendSchedule,
    SimpleAppointmentFrontendExecute
)
"""

# Contenido a agregar en rutas
routes_to_add = """
    # ===============================================================================
    # 🎯 RUTAS DE CITAS SIMPLIFICADAS - COMPATIBILIDAD CON FRONTEND
    # ===============================================================================
    
    # Ruta que espera el frontend para listar citas
    api.add_resource(SimpleAppointmentFrontendList, '/admin/simple-appointments')
    
    # Ruta que espera el frontend para agendar citas
    api.add_resource(SimpleAppointmentFrontendSchedule, '/admin/simple-appointments/schedule')
    
    # Rutas que espera el frontend para operaciones por ID
    api.add_resource(SimpleAppointmentFrontendById, '/admin/simple-appointments/<int:appointment_id>')
    
    # Ruta que espera el frontend para ejecutar citas
    api.add_resource(SimpleAppointmentFrontendExecute, '/admin/simple-appointments/execute/<int:appointment_id>')
"""

# Ruta del archivo api_routes.py
api_routes_path = "/home/kali/Desktop/DAWA_2/BACKEND/WS_CERAGEN/ws_ceragen/src/api/Routes/api_routes.py"

print("Agregando rutas de citas simplificadas...")

# Leer el archivo actual
with open(api_routes_path, 'r') as f:
    content = f.read()

# Buscar donde agregar imports (después de AdminPatientReportService)
import_position = content.find("from ..Services.Admin.AdminPatientReportService import AdminPatientReportService")
if import_position != -1:
    # Encontrar el final de esa línea
    end_of_line = content.find('\n', import_position)
    if end_of_line != -1:
        # Insertar los imports después de esa línea
        new_content = content[:end_of_line] + imports_to_add + content[end_of_line:]
        content = new_content
        print("✅ Imports agregados correctamente")
    else:
        print("❌ No se pudo encontrar el final de la línea de imports")
else:
    print("❌ No se pudo encontrar la línea de AdminPatientReportService")

# Buscar donde agregar las rutas (al final del archivo, antes del último comentario)
if content.endswith("# No newline at end of file"):
    # Eliminar el comentario
    content = content.replace("# No newline at end of file", "")

# Agregar las rutas al final
content += routes_to_add

# Escribir el archivo modificado
with open(api_routes_path, 'w') as f:
    f.write(content)

print("✅ Rutas agregadas correctamente")
print("📋 Rutas agregadas:")
print("   - GET /admin/simple-appointments")
print("   - POST /admin/simple-appointments/schedule")
print("   - GET/PUT/DELETE /admin/simple-appointments/<id>")
print("   - PATCH /admin/simple-appointments/execute/<id>")