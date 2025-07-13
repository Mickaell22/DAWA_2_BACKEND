# ----------- MÓDULO ADMINISTRADOR ----------------------------

# Servicios de Historial Médico
from ..Services.Admin.AdminPatientMedicalHistoryService import (
    AdminPatientMedicalHistoryService_get,
    AdminPatientMedicalHistoryService_getbyid,
    AdminPatientMedicalHistoryService_add,
    AdminPatientMedicalHistoryService_update,
    AdminPatientMedicalHistoryService_delete
)

# Servicios de menu
from ..Services.Security.MenuUserService import MenuUserService, MenuCurrentUserService
from ..Services.Security.MenuRolAdditionalServices import MenuRolsByMenu, MenuRolsByRole, MenuRolBulkAssign
from ..Services.Security.UserSecurityService import UserMenuPermissions, ValidateMenuAccess


# Servicios de Personas
from ..Services.Admin.AdminPersonService import (
    AdminPersonService_get,
    AdminPersonService_getbyid,
    admin_Person_service_add,
    admin_Person_service_Update,
    admin_person_service_Delete,
    AdminPersonService_statistics
)

# Servicios de Estado Civil
from ..Services.Admin.AdminMaritalStatusservice import (
    MaritalStatus_get,
    admin_Marital_Status_getbyid,
    admin_Marital_Satus_service_add,
    admin_Marital_Satus_service_Update,
    admin_Marital_Status_Delete
)

# Servicios de Lista de Parámetros
from ..Services.Admin.AdminParameterListservice import (
    admin_Parameter_List_service_get,
    admin_Parameter_List_add,
    admin_Parameter_List_Update,
    admin_Parameter_list_Delete
)

# Servicios de Género de Persona
from ..Services.Admin.AdminPerson_genre_service import (
    admin_Person_genre_service_get,
    admin_Person_Genre_getbyid,
    admin_Person_Genre_service_add,
    admin_Person_Genre_service_Update,
    admin_Person_Genre_service_Delete
)

# Servicios de Personal Médico
from ..Services.Admin.AdminMedicalStaffService import (
    admin_Medical_staff_service_get,
    admin_Medical_staff_getbyid,
    admin_Medical_staff_service_add,
    admin_Medical_staff_service_Update,
    admin_Medical_staff_service_Delete,
    admin_MedicalStaffFullListService  # <-- Nombre correcto de la clase nueva
)

# Servicios de Tipo de Persona Médica
from ..Services.Admin.AdminMedicPersonTypeService import (
    admin_MedicPersonType_service_get,
    admin_MedicPersonType_getbyid,
    admin_MedicPersonType_service_add,
    admin_MedicPersonType_service_Update,
    admin_MedicPersonType_service_Delete
)

# 🆕 SERVICIOS DE IMPUESTOS - VERSIÓN UNIFICADA Y MEJORADA
from ..Services.Admin.AdminTaxService import (
    AdminTaxServiceGet,
    AdminTaxServiceGetById,
    AdminTaxServiceAdd,
    AdminTaxServiceUpdate,
    AdminTaxServiceDelete
)

# Servicios de Facturación
from ..Services.Admin.AdminInvoiceFullService import (
    admin_Invoice_service_get,
    admin_Invoice_getbyid,
    admin_Invoice_service_add,
    admin_Invoice_service_Update,
    admin_Invoice_service_Delete
)

# Servicios de Impuestos de Factura
from ..Services.Admin.AdminInvoiceTaxService import (
    admin_Invoice_tax_service_get,
    admin_Invoice_tax_getbyid,
    admin_Invoice_tax_service_add,
    admin_Invoice_tax_service_Update,
    admin_Invoice_tax_service_Delete
)

# Servicios de Pagos de Factura
from ..Services.Admin.AdminInvoicePaymentService import (
    admin_Invoice_payment_service_get,
    admin_Invoice_payment_total_income,
    admin_Invoice_payment_getbyid,
    admin_Invoice_payment_service_add,
    admin_Invoice_payment_service_Update,
    admin_Invoice_payment_service_Delete,
AdminInvoicePaymentDashboardIncome
)

# Servicios de Métodos de Pago
from ..Services.Admin.AdminPaymentMethodService import (
    admin_PaymentMethod_service_get,
    admin_PaymentMethod_getbyid,
    admin_PaymentMethod_service_add,
    admin_PaymentMethod_service_Update,
    admin_PaymentMethod_service_Delete
)

# ----------- MÓDULO CLÍNICO ----------------------------

# Servicios de Tipo de Enfermedad
from ..Services.Clinic.ClinicDiseaseTypeService import (
    clinic_DiseaseType_service_get,
    clinic_DiseaseType_getbyid,
    clinic_DiseaseType_service_add,
    clinic_DiseaseType_service_Update,
    clinic_DiseaseType_service_Delete
)

# Servicios de Catálogo de Enfermedades
from ..Services.Clinic.ClinicDiseaseCatalogService import (
    clinic_DiseaseCatalog_service_get,
    clinic_DiseaseCatalog_service_getbyid,
    clinic_DiseaseCatalog_service_add,
    clinic_DiseaseCatalog_service_update,
    clinic_DiseaseCatalog_service_delete
)

# Servicios de Catálogo de Alergias
from ..Services.Clinic.ClinicAllergyCatalogService import (
    clinic_AllergyCatalog_service_get,
    clinic_AllergyCatalog_service_getbyid,
    clinic_AllergyCatalog_service_add,
    clinic_AllergyCatalog_service_Update,
    clinic_AllergyCatalog_service_Delete
)

from ..Services.Admin.AdminInvoiceUploadProof import (admin_Invoice_Upload_Proof,
                                                      admin_Invoice_Proof_Image)

# ----------- MÓDULO DE SEGURIDAD ----------------------------

# Servicios de Autenticación
from ..Services.Security.LoginService import LoginService
from ..Services.Security.LogoutService import LogoutService

# Servicios de Usuario
from ..Services.Security.UserService import (
    UserService, UserInsert, UserDelete, UserUpdate, UserpasswordUpdate,
    RecoveringPassword, EmailPasswordUpdate, UserListId
)

# Servicios de Menú
from ..Services.Security.MenuService import MenuService, DeleteMenu, UpdateMenu, InsertMenu

# Servicios de Rol del Sistema
from ..Services.Security.RolSistemService import RolSistemService, DeleteRolSistem, UpdateRolSistem, InsertRolSistem

# Servicios de Módulo
from ..Services.Security.ModuloService import ModuleService, DeleteModulo, UpdateModulo, InsertModulo

# Servicios de Rol de Usuario
from ..Services.Security.UserRolService import UserRolService, DeleteUserRol, InsertUserRol, UpdateUserRol

# Servicios de Persona
from ..Services.Security.GetPersonService import GetPersonService

# Servicios de Notificaciones
from ..Services.Security.NotificationService import (
    NotificationService, NotificationRead, NotificationDelete
)

# Servicios de Menú-Rol
from ..Services.Security.MenuRolServices import MenuRolService, InsertMenuRol, DeleteMenuRol, UpdateMenuRol

# Servicios URCP
from ..Services.Security.URCPService import urcpList, Updateurcp, Deleteurcp, Inserturcp

# ----------- SERVICIOS DE AUDITORÍA ----------------------------
from ..Services.Audit.AuditService import AuditService
from ..Services.Audit.ErrorService import ErrorService

# ----------- SERVICIOS JHOEL ----------------------------

# Servicios de Terapia
from ..Services.Admin.AdminTherapyService import (
    AdminTherapyService_get,
    AdminTherapyService_getbyid,
    AdminTherapyService_add,
    AdminTherapyService_update,
    AdminTherapyService_delete
)
from ..Services.Admin.AdminTherapyReportService import AdminTherapyReportService

# Servicios de Producto
from ..Services.Admin.AdminProductService import (
    AdminProductService_get,
    AdminProductService_getbyid,
    AdminProductService_add,
    AdminProductService_update,
    AdminProductService_delete
)

# Servicios de Paciente
from ..Services.Admin.AdminPatientService import (
    AdminPatientService_get,
    AdminPatientService_getbyid,
    AdminPatientService_add,
    AdminPatientService_update,
    AdminPatientService_delete
)

# Servicios de Promoción
from ..Services.Admin.AdminPromotionService import (
    AdminPromotionService_get,
    AdminPromotionService_getbyid,
    AdminPromotionService_add,
    AdminPromotionService_update,
    AdminPromotionService_delete
)

# Servicios de Cliente
from ..Services.Admin.AdminClientService import (
    AdminClientService_getbyid,
    AdminClientService_add,
    AdminClientService_update,
    AdminClientService_delete,
    AdminClientService_list
)

# Servicios de Citas
from ..Services.Admin.AdminAppointmentService import (
    AdminAppointmentService_get,
    AdminAppointmentService_getbyid,
    AdminAppointmentService_schedule,
    AdminAppointmentService_reschedule,
    AdminAppointmentService_cancel,
    AdminAppointmentService_execute,
    AdminAppointmentService_availability,
    AdminAppointmentService_calendar,
    AdminAppointmentService_therapy_types,
    AdminAppointmentService_medical_staff,
    AdminAppointmentService_products
)

from ..Services.Admin.AdminPatientReportService import AdminPatientReportService

# 🎯 SERVICIOS ADAPTADORES PARA CITAS SIMPLIFICADAS (FRONTEND)
from ..Services.Admin.SimpleAppointmentFrontendAdapter import (
    SimpleAppointmentFrontendList,
    SimpleAppointmentFrontendById,
    SimpleAppointmentFrontendSchedule,
    SimpleAppointmentFrontendExecute
)
from ..Services.Admin.SimpleAppointmentService import (
    SimpleAppointmentServiceV2_register_session,
)

def load_routes(api):
    """
    Función para cargar todas las rutas de la API de manera organizada
    """

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - PACIENTES
    # ===============================================================================
    api.add_resource(AdminPatientService_get, '/admin/patients/list')
    api.add_resource(AdminPatientService_getbyid, '/admin/patients/list/<int:id>')
    api.add_resource(AdminPatientService_add, '/admin/patients/add')
    api.add_resource(AdminPatientService_update, '/admin/patients/update')
    api.add_resource(AdminPatientService_delete, '/admin/patients/delete/<int:pat_id>/<string:user>')
    api.add_resource(AdminPatientReportService, '/admin/patients/report')
    api.add_resource(SimpleAppointmentServiceV2_register_session,
                     '/admin/simple-appointments/register-session/<int:appointment_id>')
    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - CLIENTES
    # ===============================================================================
    api.add_resource(AdminClientService_list, '/admin/clients/list')
    api.add_resource(AdminClientService_getbyid, '/admin/clients/<int:cli_id>')
    api.add_resource(AdminClientService_add, '/admin/clients/add')
    api.add_resource(AdminClientService_update, '/admin/clients/update')
    api.add_resource(AdminClientService_delete, '/admin/clients/delete/<int:cli_id>/<string:user>')

    # ===============================================================================
    # 🆕 RUTAS DE ADMINISTRACIÓN - IMPUESTOS (NUEVA IMPLEMENTACIÓN UNIFICADA)
    # ===============================================================================

    # Rutas principales RESTful
    api.add_resource(AdminTaxServiceGet, '/admin/taxes')  # GET - Lista todos los impuestos
    api.add_resource(AdminTaxServiceGetById, '/admin/taxes/<int:tax_id>')  # GET - Obtener por ID
    api.add_resource(AdminTaxServiceAdd, '/admin/taxes')  # POST - Crear nuevo impuesto
    api.add_resource(AdminTaxServiceUpdate, '/admin/taxes/<int:tax_id>')  # PUT/PATCH - Actualizar impuesto
    api.add_resource(AdminTaxServiceDelete, '/admin/taxes/<int:tax_id>')  # DELETE - Eliminar impuesto

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - TERAPIAS
    # ===============================================================================
    api.add_resource(AdminTherapyService_get, '/admin/therapy-type/list')
    api.add_resource(AdminTherapyService_getbyid, '/admin/therapy-type/list/<int:tht_id>')
    api.add_resource(AdminTherapyService_add, '/admin/therapy-type/add')
    api.add_resource(AdminTherapyService_update, '/admin/therapy-type/update')
    api.add_resource(AdminTherapyService_delete, '/admin/therapy-type/delete/<int:tht_id>/<string:user>')
    api.add_resource(AdminTherapyReportService, '/admin/therapy-type/report')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - PRODUCTOS
    # ===============================================================================
    api.add_resource(AdminProductService_get, '/admin/products/list')
    api.add_resource(AdminProductService_getbyid, '/admin/products/list/<int:pro_id>')
    api.add_resource(AdminProductService_add, '/admin/products/add')
    api.add_resource(AdminProductService_update, '/admin/products/update')
    api.add_resource(AdminProductService_delete, '/admin/products/delete/<int:pro_id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - PROMOCIONES
    # ===============================================================================
    api.add_resource(AdminPromotionService_get, '/admin/promotions')
    api.add_resource(AdminPromotionService_getbyid, '/admin/promotions/<int:ppr_id>')
    api.add_resource(AdminPromotionService_add, '/admin/promotions/add')
    api.add_resource(AdminPromotionService_update, '/admin/promotions/update')
    api.add_resource(AdminPromotionService_delete, '/admin/promotions/delete/<int:ppr_id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - HISTORIAL MÉDICO
    # ===============================================================================
    api.add_resource(AdminPatientMedicalHistoryService_get, '/admin/patient-medical-history/list')
    api.add_resource(AdminPatientMedicalHistoryService_getbyid, '/admin/patient-medical-history/list/<int:hist_id>')
    api.add_resource(AdminPatientMedicalHistoryService_add, '/admin/patient-medical-history/add')
    api.add_resource(AdminPatientMedicalHistoryService_update, '/admin/patient-medical-history/update')
    api.add_resource(AdminPatientMedicalHistoryService_delete,
                     '/admin/patient-medical-history/delete/<int:hist_id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - PERSONAS
    # ===============================================================================
    api.add_resource(AdminPersonService_get, '/admin/persons/list')
    api.add_resource(AdminPersonService_getbyid, '/admin/persons/list/<int:id>')
    api.add_resource(admin_Person_service_add, '/admin/persons/add')
    api.add_resource(admin_Person_service_Update, '/admin/persons/update')
    api.add_resource(admin_person_service_Delete, '/admin/persons/delete/<int:per_id>/<string:user>')
    api.add_resource(AdminPersonService_statistics, '/admin/persons/statistics')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - ESTADO CIVIL
    # ===============================================================================
    api.add_resource(MaritalStatus_get, '/admin/Marital_status/list')
    api.add_resource(admin_Marital_Status_getbyid, '/admin/Marital_status/list/<int:id>')
    api.add_resource(admin_Marital_Satus_service_add, '/admin/Marital_status/add')
    api.add_resource(admin_Marital_Satus_service_Update, '/admin/Marital_status/update')
    api.add_resource(admin_Marital_Status_Delete, '/admin/Marital_status/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - LISTA DE PARÁMETROS
    # ===============================================================================
    api.add_resource(admin_Parameter_List_service_get, '/admin/Parameter_list/list')
    api.add_resource(admin_Parameter_List_add, '/admin/Parameter_list/add')
    api.add_resource(admin_Parameter_List_Update, '/admin/Parameter_list/update')
    api.add_resource(admin_Parameter_list_Delete, '/admin/Parameter_list/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - GÉNERO DE PERSONA
    # ===============================================================================
    api.add_resource(admin_Person_genre_service_get, '/admin/Person_genre/list')
    api.add_resource(admin_Person_Genre_getbyid, '/admin/Person_genre/list/<int:id>')
    api.add_resource(admin_Person_Genre_service_add, '/admin/Person_genre/add')
    api.add_resource(admin_Person_Genre_service_Update, '/admin/Person_genre/update')
    api.add_resource(admin_Person_Genre_service_Delete, '/admin/Person_genre/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - PERSONAL MÉDICO
    # ===============================================================================
    api.add_resource(admin_Medical_staff_service_get, '/admin/MedicalStaff/list')
    api.add_resource(admin_Medical_staff_getbyid, '/admin/MedicalStaff/list/<int:id>')
    api.add_resource(admin_Medical_staff_service_add, '/admin/MedicalStaff/add')
    api.add_resource(admin_Medical_staff_service_Update, '/admin/MedicalStaff/update')
    api.add_resource(admin_Medical_staff_service_Delete, '/admin/MedicalStaff/delete/<int:id>/<string:user>')
    api.add_resource(admin_MedicalStaffFullListService, '/admin/MedicalStaff/fullList')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - TIPO DE PERSONA MÉDICA
    # ===============================================================================
    api.add_resource(admin_MedicPersonType_service_get, '/admin/MedicPersonType/list')
    api.add_resource(admin_MedicPersonType_getbyid, '/admin/MedicPersonType/list/<int:id>')
    api.add_resource(admin_MedicPersonType_service_add, '/admin/MedicPersonType/add')
    api.add_resource(admin_MedicPersonType_service_Update, '/admin/MedicPersonType/update')
    api.add_resource(admin_MedicPersonType_service_Delete, '/admin/MedicPersonType/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - FACTURACIÓN
    # ===============================================================================
    # Subida de imagenes
    api.add_resource(admin_Invoice_Upload_Proof, '/admin/invoice/upload-proof')
    api.add_resource(admin_Invoice_Proof_Image, '/admin/invoice/proof/<string:nombre_archivo>')

    # Facturas principales
    api.add_resource(admin_Invoice_service_get, '/admin/invoice/list')
    api.add_resource(admin_Invoice_getbyid, '/admin/invoice/<int:id>')
    api.add_resource(admin_Invoice_service_add, '/admin/invoice/add')
    api.add_resource(admin_Invoice_service_Update, '/admin/invoice/update')
    api.add_resource(admin_Invoice_service_Delete, '/admin/invoice/delete/<int:id>')

    # Impuestos de facturación
    api.add_resource(admin_Invoice_tax_service_get, '/admin/invoice/tax/list')
    api.add_resource(admin_Invoice_tax_getbyid, '/admin/invoice/tax/list/<int:id>')
    api.add_resource(admin_Invoice_tax_service_add, '/admin/invoice/tax/add')
    api.add_resource(admin_Invoice_tax_service_Update, '/admin/invoice/tax/update')
    api.add_resource(admin_Invoice_tax_service_Delete, '/admin/invoice/tax/delete/<int:id>')

    # Pagos de facturación
    api.add_resource(admin_Invoice_payment_service_get, '/admin/invoice/payment/list')
    api.add_resource(admin_Invoice_payment_total_income, '/admin/invoice/payment/total_income')
    api.add_resource(AdminInvoicePaymentDashboardIncome, '/admin/invoice/payment/dashboard_income')# dashboard
    api.add_resource(admin_Invoice_payment_getbyid, '/admin/invoice/payment/list/<int:id>')
    api.add_resource(admin_Invoice_payment_service_add, '/admin/invoice/payment/add')
    api.add_resource(admin_Invoice_payment_service_Update, '/admin/invoice/payment/update')
    api.add_resource(admin_Invoice_payment_service_Delete, '/admin/invoice/payment/delete/<int:id>')

    # ===============================================================================
    # RUTAS DE ADMINISTRACIÓN - MÉTODOS DE PAGO
    # ===============================================================================
    api.add_resource(admin_PaymentMethod_service_get, '/admin/PaymentMethod/list')
    api.add_resource(admin_PaymentMethod_getbyid, '/admin/PaymentMethod/list/<int:id>')
    api.add_resource(admin_PaymentMethod_service_add, '/admin/PaymentMethod/add')
    api.add_resource(admin_PaymentMethod_service_Update, '/admin/PaymentMethod/update')
    api.add_resource(admin_PaymentMethod_service_Delete, '/admin/PaymentMethod/delete/<int:id>')

    # ===============================================================================
    # RUTAS CLÍNICAS - TIPOS DE ENFERMEDAD
    # ===============================================================================
    api.add_resource(clinic_DiseaseType_service_get, '/clinic/DiseaseType/list')
    api.add_resource(clinic_DiseaseType_getbyid, '/clinic/DiseaseType/list/<int:id>')
    api.add_resource(clinic_DiseaseType_service_add, '/clinic/DiseaseType/add')
    api.add_resource(clinic_DiseaseType_service_Update, '/clinic/DiseaseType/update')
    api.add_resource(clinic_DiseaseType_service_Delete, '/clinic/DiseaseType/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS CLÍNICAS - CATÁLOGO DE ENFERMEDADES
    # ===============================================================================
    api.add_resource(clinic_DiseaseCatalog_service_get, '/clinic/DiseaseCatalog/list')
    api.add_resource(clinic_DiseaseCatalog_service_getbyid, '/clinic/DiseaseCatalog/list/<int:id>')
    api.add_resource(clinic_DiseaseCatalog_service_add, '/clinic/DiseaseCatalog/add')
    api.add_resource(clinic_DiseaseCatalog_service_update, '/clinic/DiseaseCatalog/update')
    api.add_resource(clinic_DiseaseCatalog_service_delete, '/clinic/DiseaseCatalog/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS CLÍNICAS - CATÁLOGO DE ALERGIAS
    # ===============================================================================
    api.add_resource(clinic_AllergyCatalog_service_get, '/clinic/AllergyCatalog/list')
    api.add_resource(clinic_AllergyCatalog_service_getbyid, '/clinic/AllergyCatalog/list/<int:id>')
    api.add_resource(clinic_AllergyCatalog_service_add, '/clinic/AllergyCatalog/add')
    api.add_resource(clinic_AllergyCatalog_service_Update, '/clinic/AllergyCatalog/update')
    api.add_resource(clinic_AllergyCatalog_service_Delete, '/clinic/AllergyCatalog/delete/<int:id>/<string:user>')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - AUTENTICACIÓN
    # ===============================================================================
    api.add_resource(LoginService, '/security/login')
    api.add_resource(LogoutService, '/security/logout')
    api.add_resource(RecoveringPassword, '/security/recover-password')
    api.add_resource(EmailPasswordUpdate, '/security/change-password')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - MENÚS MULTIROL (NUEVAS)
    # ===============================================================================
    api.add_resource(MenuUserService, '/Menu/user/<int:user_id>')
    api.add_resource(MenuCurrentUserService, '/Menu/my-menus')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - MENÚ-ROL ADICIONALES
    # ===============================================================================
    api.add_resource(MenuRolsByMenu, '/MenuRol/by-menu')
    api.add_resource(MenuRolsByRole, '/MenuRol/by-role')
    api.add_resource(MenuRolBulkAssign, '/MenuRol/bulk-assign')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - VALIDACIÓN DE PERMISOS
    # ===============================================================================
    api.add_resource(UserMenuPermissions, '/security/user-permissions')
    api.add_resource(ValidateMenuAccess, '/security/validate-menu-access')


    # ===============================================================================
    # RUTAS DE SEGURIDAD - USUARIOS
    # ===============================================================================
    api.add_resource(UserService, '/user/list')
    api.add_resource(UserListId, '/user/actulization/data')
    api.add_resource(UserInsert, '/user/insert')
    api.add_resource(UserDelete, '/user/delete')
    api.add_resource(UserUpdate, '/user/update')
    api.add_resource(UserpasswordUpdate, '/user/change-password')
    api.add_resource(GetPersonService, '/person/get')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - ROLES DEL SISTEMA
    # ===============================================================================
    api.add_resource(RolSistemService, '/RolSistem/list')
    api.add_resource(InsertRolSistem, '/RolSistem/insert')
    api.add_resource(DeleteRolSistem, '/RolSistem/delete')
    api.add_resource(UpdateRolSistem, '/RolSistem/update')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - ROLES DE USUARIO
    # ===============================================================================
    api.add_resource(UserRolService, '/UserRol/list')
    api.add_resource(DeleteUserRol, '/UserRol/delete')
    api.add_resource(InsertUserRol, '/UserRol/insert')
    api.add_resource(UpdateUserRol, '/UserRol/update')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - MÓDULOS
    # ===============================================================================
    api.add_resource(ModuleService, '/Module/list')
    api.add_resource(InsertModulo, '/Module/insert')
    api.add_resource(DeleteModulo, '/Module/delete')
    api.add_resource(UpdateModulo, '/Module/update')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - MENÚS
    # ===============================================================================
    api.add_resource(MenuService, '/Menu/list')
    api.add_resource(InsertMenu, '/Menu/insert')
    api.add_resource(DeleteMenu, '/Menu/delete')
    api.add_resource(UpdateMenu, '/Menu/update')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - MENÚ-ROL
    # ===============================================================================
    api.add_resource(MenuRolService, '/MenuRol/list')
    api.add_resource(DeleteMenuRol, '/MenuRol/delete')
    api.add_resource(UpdateMenuRol, '/MenuRol/update')
    api.add_resource(InsertMenuRol, '/MenuRol/insert')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - NOTIFICACIONES
    # ===============================================================================
    api.add_resource(NotificationService, '/Notification/list')
    api.add_resource(NotificationRead, '/Notification/read')
    api.add_resource(NotificationDelete, '/Notification/delete')

    # ===============================================================================
    # RUTAS DE SEGURIDAD - URCP
    # ===============================================================================
    api.add_resource(urcpList, '/urcp/list')
    api.add_resource(Inserturcp, '/urcp/insert')
    api.add_resource(Updateurcp, '/urcp/update')
    api.add_resource(Deleteurcp, '/urcp/delete')

    # ===============================================================================
    # RUTAS DE AUDITORÍA
    # ===============================================================================
    api.add_resource(AuditService, '/Audit/list')
    api.add_resource(ErrorService, '/Error/list')

    # ===============================================================================
    # RUTAS DE CITAS - PRINCIPALES (SISTEMA COMPLEJO)
    # ===============================================================================
    api.add_resource(AdminAppointmentService_get, '/admin/appointments/list')
    api.add_resource(AdminAppointmentService_getbyid, '/admin/appointments/list/<int:appointment_id>')
    api.add_resource(AdminAppointmentService_schedule, '/admin/appointments/schedule')
    api.add_resource(AdminAppointmentService_reschedule, '/admin/appointments/reschedule')
    api.add_resource(AdminAppointmentService_cancel, '/admin/appointments/cancel/<int:appointment_id>')
    api.add_resource(AdminAppointmentService_execute, '/admin/appointments/execute/<int:appointment_id>')

    # ===============================================================================
    # RUTAS DE CITAS - DISPONIBILIDAD Y CALENDARIO
    # ===============================================================================
    api.add_resource(AdminAppointmentService_availability, '/admin/appointments/availability')
    api.add_resource(AdminAppointmentService_calendar, '/admin/appointments/calendar')

    # ===============================================================================
    # RUTAS DE CITAS - AUXILIARES PARA FORMULARIOS
    # ===============================================================================
    api.add_resource(AdminAppointmentService_therapy_types, '/admin/appointments/therapy-types')
    api.add_resource(AdminAppointmentService_medical_staff, '/admin/appointments/medical-staff')
    api.add_resource(AdminAppointmentService_products, '/admin/appointments/products/<int:therapy_type_id>')

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