

#----------- MÓDULO ADMINISTRADOR ----------------------------

from ..Services.Admin.AdminPersonService import (AdminPersonService_get,
                                                 AdminPersonService_getbyid,
                                                 admin_Person_service_add,
                                                 admin_Person_service_Update,
                                                 admin_person_service_Delete)


from ..Services.Admin.AdminMaritalStatusservice import (MaritalStatus_get,
                                                        admin_Marital_Status_getbyid,
                                                        admin_Marital_Satus_service_add,
                                                        admin_Marital_Satus_service_Update,
                                                        admin_Marital_Status_Delete)

from ..Services.Admin.AdminParameterListservice import (admin_Parameter_List_service_get,
                                                        admin_Parameter_List_add,
                                                        admin_Parameter_List_Update,
                                                        admin_Parameter_list_Delete)

from ..Services.Admin.AdminPerson_genre_service import (admin_Person_genre_service_get,
                                                        admin_Person_Genre_getbyid,
                                                        admin_Person_Genre_service_add,
                                                        admin_Person_Genre_service_Update,
                                                        admin_Person_Genre_service_Delete)

from ..Services.Admin.AdminMedicalStaffService import (admin_Medical_staff_service_get,
                                                       admin_Medical_staff_getbyid,
                                                       admin_Medical_staff_service_add,
                                                       admin_Medical_staff_service_Update,
                                                       admin_Medical_staff_service_Delete)

from ..Services.Admin.AdminMedicPersonTypeService import (admin_MedicPersonType_service_get,
                                                          admin_MedicPersonType_getbyid,
                                                          admin_MedicPersonType_service_add,
                                                          admin_MedicPersonType_service_Update,
                                                          admin_MedicPersonType_service_Delete)


from ..Services.Clinic.ClinicDiseaseTypeService import (clinic_DiseaseType_service_get,
                                                        clinic_DiseaseType_getbyid,
                                                        clinic_DiseaseType_service_add,
                                                        clinic_DiseaseType_service_Update,
                                                        clinic_DiseaseType_service_Delete)

from ..Services.Clinic.ClinicDiseaseCatalogService import (clinic_DiseaseCatalog_service_get,
                                                           clinic_DiseaseCatalog_service_getbyid,
                                                           clinic_DiseaseCatalog_service_add,
                                                           clinic_DiseaseCatalog_service_update,
                                                           clinic_DiseaseCatalog_service_delete)

from ..Services.Clinic.ClinicAllergyCatalogService import (clinic_AllergyCatalog_service_get,
                                                           clinic_AllergyCatalog_service_getbyid,
                                                           clinic_AllergyCatalog_service_add,
                                                           clinic_AllergyCatalog_service_Update,
                                                           clinic_AllergyCatalog_service_Delete)

from ..Services.Admin.AdminInvoiceFullService import (admin_Invoice_service_get,
                                                      admin_Invoice_getbyid,
                                                      admin_Invoice_service_add,
                                                      admin_Invoice_service_Update,
                                                      admin_Invoice_service_Delete)

from ..Services.Admin.AdminInvoiceTaxService import (admin_Invoice_tax_service_get,
                                                     admin_Invoice_tax_getbyid,
                                                     admin_Invoice_tax_service_add,
                                                     admin_Invoice_tax_service_Update,
                                                     admin_Invoice_tax_service_Delete)

from ..Services.Admin.AdminInvoicePaymentService import (admin_Invoice_payment_service_get,
                                                         admin_Invoice_payment_getbyid,
                                                         admin_Invoice_payment_service_add,
                                                         admin_Invoice_payment_service_Update,
                                                         admin_Invoice_payment_service_Delete)

from ..Services.Admin.AdminTaxService import (admin_Tax_service_get,
                                              admin_Tax_getbyid,
                                              admin_Tax_service_add,
                                              admin_Tax_service_Update,
                                              admin_Tax_service_Delete)

from ..Services.Admin.AdminPaymentMethodService import (admin_PaymentMethod_service_get,
                                                        admin_PaymentMethod_getbyid,
                                                        admin_PaymentMethod_service_add,
                                                        admin_PaymentMethod_service_Update,
                                                        admin_PaymentMethod_service_Delete)

from ..Services.Security.LoginService import LoginService
from ..Services.Security.LogoutService import LogoutService
from ..Services.Security.UserService import UserService, UserInsert, UserDelete, UserUpdate,UserpasswordUpdate,RecoveringPassword,EmailPasswordUpdate

from ..Services.Security.MenuService import MenuService, DeleteMenu, UpdateMenu, InsertMenu
from ..Services.Security.RolSistemService import RolSistemService, DeleteRolSistem, UpdateRolSistem, InsertRolSistem
from ..Services.Security.ModuloService import ModuleService, DeleteModulo, UpdateModulo, InsertModulo
from ..Services.Security.UserRolService import UserRolService, DeleteUserRol,InsertUserRol,UpdateUserRol
from ..Services.Security.GetPersonService import GetPersonService
from ..Services.Security.NotificationService import NotificationDelete

from ..Services.Security.MenuRolServices import MenuRolService,InsertMenuRol,DeleteMenuRol, UpdateMenuRol
from ..Services.Security.NotificationService import NotificationService, NotificationRead
from ..Services.Audit.AuditService import AuditService
from ..Services.Audit.ErrorService import ErrorService
from ..Services.Security.URCPService import urcpList,Updateurcp,Deleteurcp,Inserturcp
from ..Services.Security.UserService import UserListId
#-------------------------------------------------------------------------------
                        #RUTAS JHOEL
#-------------------------------------------------------------------------------

from ..Services.Admin.AdminTherapyService import (
    AdminTherapyService_get,
    AdminTherapyService_getbyid,
    AdminTherapyService_add,
    AdminTherapyService_update,
    AdminTherapyService_delete
)
from ..Services.Admin.AdminProductService import (
    AdminProductService_get,
    AdminProductService_getbyid,
    AdminProductService_add,
    AdminProductService_update,
    AdminProductService_delete
)
from ..Services.Admin.AdminPatientService import (
    AdminPatientService_get,
    AdminPatientService_getbyid,
    AdminPatientService_add,
    AdminPatientService_update,
    AdminPatientService_delete

)
from ..Services.Admin.AdminClientService import (
    AdminClientService_getbyid,
    AdminClientService_add,
    AdminClientService_update,
    AdminClientService_delete,
    AdminClientService_list
)
#-------------------------------------------------------------------------------
#user/insert
#-------------------------------------------------------------------------------

def load_routes(api):
    # -------------------------------------------------------------------------------
    # user/insert
    # -------------------------------------------------------------------------------
    # Ruta de Tabla Patient
    api.add_resource(AdminPatientService_get, '/admin/patients/list')
    api.add_resource(AdminPatientService_getbyid, '/admin/patients/list/<int:id>')
    api.add_resource(AdminPatientService_add, '/admin/patients/add')
    api.add_resource(AdminPatientService_update, '/admin/patients/update')
    api.add_resource(AdminPatientService_delete, '/admin/patients/delete/<int:pat_id>/<string:user>')
    # -------------------------------------------------------------------------------
    # Ruta de Tabla Admin Client
    api.add_resource(AdminClientService_list, '/admin/clients/list')
    api.add_resource(AdminClientService_getbyid, '/admin/clients/<int:cli_id>')
    api.add_resource(AdminClientService_add, '/admin/clients/add')
    api.add_resource(AdminClientService_update, '/admin/clients/update')
    api.add_resource(AdminClientService_delete, '/admin/clients/delete/<int:cli_id>/<string:user>')
    # -------------------------------------------------------------------------------

    # Ruta de Tabla Therapy Type
    api.add_resource(AdminTherapyService_get, '/admin/therapy-type/list')  # List
    api.add_resource(AdminTherapyService_getbyid, '/admin/therapy-type/list/<int:tht_id>')  # List for ID
    api.add_resource(AdminTherapyService_add, '/admin/therapy-type/add')  # Add
    api.add_resource(AdminTherapyService_update, '/admin/therapy-type/update')  # Update
    api.add_resource(AdminTherapyService_delete, '/admin/therapy-type/delete/<int:tht_id>/<string:user>')  # Delete
    # Ruta de Tabla Product
    api.add_resource(AdminProductService_get, '/admin/products/list')
    api.add_resource(AdminProductService_getbyid, '/admin/products/list/<int:pro_id>')
    api.add_resource(AdminProductService_add, '/admin/products/add')
    api.add_resource(AdminProductService_update, '/admin/products/update')
    api.add_resource(AdminProductService_delete, '/admin/products/delete/<int:pro_id>/<string:user>')

    # -------------------------------------------------------------------------------

    # Ruta de Tabla Person
    api.add_resource(AdminPersonService_get, '/admin/persons/list')   # List
    api.add_resource(AdminPersonService_getbyid, '/admin/persons/list/<int:id>')  # List for ID
    api.add_resource(admin_Person_service_add, '/admin/persons/add')   # Add
    api.add_resource(admin_Person_service_Update, '/admin/persons/update')   # Update
    api.add_resource(admin_person_service_Delete, '/admin/persons/delete/<int:per_id>/<string:user>')  # Delete

    # Ruta de Tabla Marital Status
    api.add_resource(MaritalStatus_get, '/admin/Marital_status/list')   # List
    api.add_resource(admin_Marital_Status_getbyid, '/admin/Marital_status/list/<int:id>')  # List for ID
    api.add_resource(admin_Marital_Satus_service_add, '/admin/Marital_status/add')   # Add
    api.add_resource(admin_Marital_Satus_service_Update, '/admin/Marital_status/update')   # Update
    api.add_resource(admin_Marital_Status_Delete, '/admin/Marital_status/delete/<int:id>/<string:user>')  # Delete

    # Ruta de Tabla Parameter List
    api.add_resource(admin_Parameter_List_service_get, '/admin/Parameter_list/list')   # List

    api.add_resource(admin_Parameter_List_add, '/admin/Parameter_list/add')   # Add
    api.add_resource(admin_Parameter_List_Update, '/admin/Parameter_list/update')   # Update
    api.add_resource(admin_Parameter_list_Delete,'/admin/Parameter_list/delete/<int:id>/<string:user>')  # Delete

    # Ruta de Tabla Person Genre
    api.add_resource(admin_Person_genre_service_get, '/admin/Person_genre/list')   # List
    api.add_resource(admin_Person_Genre_getbyid, '/admin/Person_genre/list/<int:id>')  # List for ID
    api.add_resource(admin_Person_Genre_service_add, '/admin/Person_genre/add')   # Add
    api.add_resource(admin_Person_Genre_service_Update, '/admin/Person_genre/update')   # Update
    api.add_resource(admin_Person_Genre_service_Delete, '/admin/Person_genre/delete/<int:id>/<string:user>')  # Delete

    #Ruta de Tabla Medical Staff
    api.add_resource(admin_Medical_staff_service_get, '/admin/MedicalStaff/list')  # List
    api.add_resource(admin_Medical_staff_getbyid, '/admin/MedicalStaff/list/<int:id>') # List for ID
    api.add_resource(admin_Medical_staff_service_add, '/admin/MedicalStaff/add') # Add
    api.add_resource(admin_Medical_staff_service_Update, '/admin/MedicalStaff/update') # Update
    api.add_resource(admin_Medical_staff_service_Delete, '/admin/MedicalStaff/delete/<int:id>/<string:user>') # Delete

    #Ruta de Tabla Medic Person Type
    api.add_resource(admin_MedicPersonType_service_get, '/admin/MedicPersonType/list')
    api.add_resource(admin_MedicPersonType_getbyid, '/admin/MedicPersonType/list/<int:id>')
    api.add_resource(admin_MedicPersonType_service_add, '/admin/MedicPersonType/add')
    api.add_resource(admin_MedicPersonType_service_Update, '/admin/MedicPersonType/update')
    api.add_resource(admin_MedicPersonType_service_Delete, '/admin/MedicPersonType/delete/<int:id>/<string:user>')

    # Rutas de Tabla Disease Type
    api.add_resource(clinic_DiseaseType_service_get, '/clinic/DiseaseType/list')
    api.add_resource(clinic_DiseaseType_getbyid, '/clinic/DiseaseType/list/<int:id>')
    api.add_resource(clinic_DiseaseType_service_add, '/clinic/DiseaseType/add')
    api.add_resource(clinic_DiseaseType_service_Update, '/clinic/DiseaseType/update')
    api.add_resource(clinic_DiseaseType_service_Delete, '/clinic/DiseaseType/delete/<int:id>/<string:user>')

    # Rutas para el catálogo de enfermedades (clinic_disease_catalog)
    api.add_resource(clinic_DiseaseCatalog_service_get, '/clinic/DiseaseCatalog/list')
    api.add_resource(clinic_DiseaseCatalog_service_getbyid, '/clinic/DiseaseCatalog/list/<int:id>')
    api.add_resource(clinic_DiseaseCatalog_service_add, '/clinic/DiseaseCatalog/add')
    api.add_resource(clinic_DiseaseCatalog_service_update, '/clinic/DiseaseCatalog/update')
    api.add_resource(clinic_DiseaseCatalog_service_delete, '/clinic/DiseaseCatalog/delete/<int:id>/<string:user>')

    # Rutas para el catálogo de alergias (clinic_allergy_catalog)
    api.add_resource(clinic_AllergyCatalog_service_get, '/clinic/AllergyCatalog/list')
    api.add_resource(clinic_AllergyCatalog_service_getbyid, '/clinic/AllergyCatalog/list/<int:id>')
    api.add_resource(clinic_AllergyCatalog_service_add, '/clinic/AllergyCatalog/add')
    api.add_resource(clinic_AllergyCatalog_service_Update, '/clinic/AllergyCatalog/update')
    api.add_resource(clinic_AllergyCatalog_service_Delete, '/clinic/AllergyCatalog/delete/<int:id>/<string:user>')

    # Rutas para el módulo de facturación (admin_invoice)
    api.add_resource(admin_Invoice_service_get, '/admin/invoice/list')
    api.add_resource(admin_Invoice_getbyid, '/admin/invoice/list/<int:id>')
    api.add_resource(admin_Invoice_service_add, '/admin/invoice/add')
    api.add_resource(admin_Invoice_service_Update, '/admin/invoice/update')
    api.add_resource(admin_Invoice_service_Delete, '/admin/invoice/delete/<int:id>')

    # Rutas para los pagos de facturación (admin_invoice_payment)
    api.add_resource(admin_Invoice_payment_service_get, '/admin/invoice/payment/list')
    api.add_resource(admin_Invoice_payment_getbyid, '/admin/invoice/payment/list/<int:id>')
    api.add_resource(admin_Invoice_payment_service_add, '/admin/invoice/payment/add')
    api.add_resource(admin_Invoice_payment_service_Update, '/admin/invoice/payment/update')
    api.add_resource(admin_Invoice_payment_service_Delete, '/admin/invoice/payment/delete/<int:id>')

    # Rutas para los impuestos de facturación (admin_invoice_tax)
    api.add_resource(admin_Invoice_tax_service_get, '/admin/invoice/tax/list')
    api.add_resource(admin_Invoice_tax_getbyid, '/admin/invoice/tax/list/<int:id>')
    api.add_resource(admin_Invoice_tax_service_add, '/admin/invoice/tax/add')
    api.add_resource(admin_Invoice_tax_service_Update, '/admin/invoice/tax/update')
    api.add_resource(admin_Invoice_tax_service_Delete, '/admin/invoice/tax/delete/<int:id>')

    # Rutas de Tabla Admin Tax
    api.add_resource(admin_Tax_service_get, '/admin/Tax/list')  # Listar todos
    api.add_resource(admin_Tax_getbyid, '/admin/Tax/list/<int:id>')  # Obtener por ID
    api.add_resource(admin_Tax_service_add, '/admin/Tax/add')  # Agregar nuevo
    api.add_resource(admin_Tax_service_Update, '/admin/Tax/update')  # Actualizar
    api.add_resource(admin_Tax_service_Delete, '/admin/Tax/delete/<int:id>')  # Eliminación lógica

    # Rutas de Tabla Admin Payment Method
    api.add_resource(admin_PaymentMethod_service_get, '/admin/PaymentMethod/list')  # Listar todos
    api.add_resource(admin_PaymentMethod_getbyid, '/admin/PaymentMethod/list/<int:id>')  # Obtener por ID
    api.add_resource(admin_PaymentMethod_service_add, '/admin/PaymentMethod/add')  # Agregar nuevo
    api.add_resource(admin_PaymentMethod_service_Update, '/admin/PaymentMethod/update')  # Actualizar
    api.add_resource(admin_PaymentMethod_service_Delete, '/admin/PaymentMethod/delete/<int:id>')  # Eliminación lógica

    #******* SECURITY PATH ******#
    #metodo para el login
    api.add_resource(LoginService, '/security/login')
    api.add_resource(LogoutService, '/security/logout')
    api.add_resource(UserListId, '/user/actulization/data')
    api.add_resource(UserService, '/user/list')
    api.add_resource(UserInsert, '/user/insert')
    api.add_resource(UserDelete, '/user/delete')
    api.add_resource(UserUpdate, '/user/update')
    api.add_resource(UserpasswordUpdate, '/user/change-password')
    api.add_resource(RecoveringPassword, '/security/recover-password')
    api.add_resource(EmailPasswordUpdate, '/security/change-password')
    api.add_resource(GetPersonService, '/person/get')

    api.add_resource(InsertRolSistem, '/RolSistem/insert')
    api.add_resource(RolSistemService, '/RolSistem/list')
    api.add_resource(DeleteRolSistem, '/RolSistem/delete')
    api.add_resource(UpdateRolSistem, '/RolSistem/update')


    api.add_resource(UserRolService, '/UserRol/list')
    api.add_resource(DeleteUserRol, '/UserRol/delete')
    api.add_resource(InsertUserRol, '/UserRol/insert')
    api.add_resource(UpdateUserRol, '/UserRol/update')

    api.add_resource(InsertModulo, '/Module/insert')
    api.add_resource(ModuleService, '/Module/list')
    api.add_resource(DeleteModulo, '/Module/delete')
    api.add_resource(UpdateModulo, '/Module/update')

    api.add_resource(InsertMenu, '/Menu/insert')
    api.add_resource(MenuService, '/Menu/list')
    api.add_resource(DeleteMenu, '/Menu/delete')
    api.add_resource(UpdateMenu, '/Menu/update')

    api.add_resource(MenuRolService, '/MenuRol/list')
    api.add_resource(DeleteMenuRol, '/MenuRol/delete')
    api.add_resource(UpdateMenuRol, '/MenuRol/update')
    api.add_resource(InsertMenuRol, '/MenuRol/insert')

    api.add_resource(AuditService, '/Audit/list')
    api.add_resource(ErrorService, '/Error/list')

    api.add_resource(NotificationService, '/Notification/list')
    api.add_resource(NotificationRead, '/Notification/read')

    api.add_resource(NotificationDelete, '/Notification/delete')

    api.add_resource(urcpList,'/urcp/list')
    api.add_resource(Inserturcp, '/urcp/insert')
    api.add_resource(Updateurcp, '/urcp/update')
    api.add_resource(Deleteurcp, '/urcp/delete')