import reflex as rx
from typing import TypedDict, Literal, cast
import random
import string
import datetime

TRANSLATIONS = {
    "en": {
        "title": "Fletor",
        "subtitle": "Freight Transport for Costa Rica",
        "login": "Login",
        "register": "Register",
        "logout": "Logout",
        "home": "Home",
        "dashboard": "Dashboard",
        "profile": "Profile",
        "admin": "Admin",
        "shipper": "Shipper",
        "carrier": "Carrier",
        "select_role": "Select your role",
        "email": "Email",
        "password": "Password",
        "full_name": "Full Name",
        "phone_number": "Phone Number",
        "company_name": "Company Name",
        "license_number": "Driver's License Number (A3)",
        "vehicle_type": "Main Vehicle Type",
        "confirm_password": "Confirm Password",
        "passwords_do_not_match": "Passwords do not match.",
        "registration_successful": "Registration successful! Please log in.",
        "login_failed": "Login failed. Please check your credentials.",
        "user_not_found": "User not found.",
        "save_profile": "Save Profile",
        "profile_saved": "Profile saved successfully.",
        "upload_documents": "Upload Documents",
        "document_name": "Document Name",
        "upload": "Upload",
        "uploaded_files": "Uploaded Files",
        "user_verification": "User Verification",
        "approve": "Approve",
        "reject": "Reject",
        "user_approved": "User approved.",
        "user_rejected": "User rejected.",
        "hero_title": "The Smartest Way to Move Freight in Costa Rica",
        "hero_subtitle": "Connecting shippers with reliable carriers, efficiently and securely.",
        "get_started_shipper": "I'm a Shipper",
        "get_started_carrier": "I'm a Carrier",
        "create_shipment": "Create Shipment",
        "new_shipment": "New Shipment",
        "pickup_location": "Pickup Location",
        "delivery_location": "Delivery Location",
        "address": "Address",
        "city": "City",
        "province": "Province",
        "postal_code": "Postal Code",
        "cargo_details": "Cargo Details",
        "cargo_type": "Cargo Type",
        "general": "General",
        "refrigerated": "Refrigerated",
        "hazardous": "Hazardous",
        "oversized": "Oversized",
        "weight_kg": "Weight (kg)",
        "dimensions_m": "Dimensions (L x W x H in meters)",
        "length": "Length",
        "width": "Width",
        "height": "Height",
        "special_instructions": "Special Instructions",
        "pickup_datetime": "Pickup Date & Time",
        "calculate_quote": "Calculate Quote",
        "estimated_quote": "Estimated Quote",
        "base_rate": "Base Rate",
        "weight_surcharge": "Weight Surcharge",
        "cargo_surcharge": "Cargo Surcharge",
        "total_estimated_price": "Total Estimated Price",
        "post_for_bidding": "Post for Bidding",
        "book_now": "Book Now",
        "shipment_posted_success": "Shipment posted for bidding successfully!",
        "active_shipments": "Active Shipments",
        "pending_quotes": "Pending Quotes",
        "completed_deliveries": "Completed Deliveries",
        "total_spent": "Total Spent",
        "shipments": "Shipments",
        "status": "Status",
        "price": "Price",
        "actions": "Actions",
        "view": "View",
        "all": "All",
        "active": "Active",
        "pending": "Pending",
        "completed": "Completed",
        "pending_assignment": "Pending Assignment",
        "assigned": "Assigned",
        "in_transit": "In Transit",
        "picked_up": "Picked Up",
        "delivered": "Delivered",
        "cancelled": "Cancelled",
        "delayed": "Delayed",
        "shipment_details": "Shipment Details",
        "available_jobs": "Available Jobs",
        "accept_job": "Accept Job",
        "decline_job": "Decline Job",
        "job_details": "Job Details",
        "route_distance": "Route Distance",
        "active_deliveries": "Active Deliveries",
        "earnings": "Earnings",
        "browse_jobs": "Browse Jobs",
        "vehicle_details": "Vehicle Details",
        "fleet_management": "Fleet Management",
        "no_jobs_available": "No jobs available at the moment. Check back later!",
        "job_accepted_success": "Job accepted successfully! You can find it in your dashboard.",
        "completed_jobs": "Completed Jobs",
        "access_denied": "Access Denied.",
        "carriers_only": "Carriers only.",
        "track_shipment": "Track Shipment",
        "live_tracking": "Live Tracking",
        "shipment_timeline": "Shipment Timeline",
        "mark_as_picked_up": "Mark as Picked Up",
        "mark_as_in_transit": "Mark as In Transit",
        "mark_as_delivered": "Mark as Delivered",
        "eta": "Estimated Time of Arrival",
        "messages": "Messages",
        "send_message": "Send Message",
        "type_your_message": "Type your message...",
        "message_sent_success": "Message sent successfully.",
        "no_messages_yet": "No messages yet. Start the conversation!",
        "message_carrier": "Message Carrier",
        "message_shipper": "Message Shipper",
        "review": "Review",
        "admin_dashboard": "Admin Dashboard",
        "total_users": "Total Users",
        "total_shippers": "Total Shippers",
        "total_carriers": "Total Carriers",
        "completed_shipments": "Completed Shipments",
        "total_revenue": "Total Revenue",
        "platform_commission": "Platform Commission",
        "no_users_for_verification": "No users are currently pending verification.",
        "verifying": "Verifying",
        "close": "Close",
        "no_documents_uploaded": "This user has not uploaded any documents yet.",
        "approval_notes_placeholder": "Optional: Add notes for approval...",
        "rejection_reason_placeholder": "Reason for rejection...",
        "disputes": "Disputes",
        "support_tickets": "Support Tickets",
        "financial_overview": "Financial Overview",
        "create_dispute": "Create Dispute",
        "dispute_details": "Dispute Details",
        "view_dispute": "View Dispute",
        "payment_issue": "Payment Issue",
        "service_quality": "Service Quality",
        "cargo_damage": "Cargo Damage",
        "delayed_delivery": "Delayed Delivery",
        "other_issue": "Other Issue",
        "open": "Open",
        "investigating": "Investigating",
        "pending_resolution": "Pending Resolution",
        "resolved": "Resolved",
        "closed": "Closed",
        "new": "New",
        "in_progress": "In Progress",
        "waiting_on_user": "Waiting on User",
        "priority": "Priority",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "urgent": "Urgent",
        "complainant": "Complainant",
        "respondent": "Respondent",
        "resolution": "Resolution",
        "assign_to": "Assign To",
        "admin_response": "Admin Response",
        "quick_replies": "Quick Replies",
        "mark_as_investigating": "Mark as Investigating",
        "mark_as_resolved": "Mark as Resolved",
        "total_revenue": "Total Revenue",
        "platform_commission": "Platform Commission",
        "pending_payouts": "Pending Payouts",
        "processed_payouts": "Processed Payouts",
        "process_payout": "Process Payout",
        "payout_queue": "Payout Queue",
        "commission_rate": "Commission Rate",
        "transaction_history": "Transaction History",
        "technical_issue": "Technical Issue",
        "account_issue": "Account Issue",
        "billing_issue": "Billing Issue",
        "feature_request": "Feature Request",
        "financial": "Financial",
        "support": "Support",
    },
    "es": {
        "title": "Fletor",
        "subtitle": "Transporte de Carga para Costa Rica",
        "login": "Iniciar Sesión",
        "register": "Registrarse",
        "logout": "Cerrar Sesión",
        "home": "Inicio",
        "dashboard": "Panel",
        "profile": "Perfil",
        "admin": "Admin",
        "shipper": "Remitente",
        "carrier": "Transportista",
        "select_role": "Seleccione su rol",
        "email": "Correo Electrónico",
        "password": "Contraseña",
        "full_name": "Nombre Completo",
        "phone_number": "Número de Teléfono",
        "company_name": "Nombre de la Empresa",
        "license_number": "Número de Licencia (A3)",
        "vehicle_type": "Tipo de Vehículo Principal",
        "confirm_password": "Confirmar Contraseña",
        "passwords_do_not_match": "Las contraseñas no coinciden.",
        "registration_successful": "¡Registro exitoso! Por favor inicie sesión.",
        "login_failed": "Inicio de sesión fallido. Verifique sus credenciales.",
        "user_not_found": "Usuario no encontrado.",
        "save_profile": "Guardar Perfil",
        "profile_saved": "Perfil guardado exitosamente.",
        "upload_documents": "Subir Documentos",
        "document_name": "Nombre del Documento",
        "upload": "Subir",
        "uploaded_files": "Archivos Subidos",
        "user_verification": "Verificación de Usuario",
        "approve": "Aprobar",
        "reject": "Rechazar",
        "user_approved": "Usuario aprobado.",
        "user_rejected": "Usuario rechazado.",
        "hero_title": "La Forma Inteligente de Mover Carga en Costa Rica",
        "hero_subtitle": "Conectando remitentes con transportistas confiables, de manera eficiente y segura.",
        "get_started_shipper": "Soy Remitente",
        "get_started_carrier": "Soy Transportista",
        "create_shipment": "Crear Envío",
        "new_shipment": "Nuevo Envío",
        "pickup_location": "Lugar de Recogida",
        "delivery_location": "Lugar de Entrega",
        "address": "Dirección",
        "city": "Ciudad",
        "province": "Provincia",
        "postal_code": "Código Postal",
        "cargo_details": "Detalles de la Carga",
        "cargo_type": "Tipo de Carga",
        "general": "General",
        "refrigerated": "Refrigerada",
        "hazardous": "Peligrosa",
        "oversized": "Sobredimensionada",
        "weight_kg": "Peso (kg)",
        "dimensions_m": "Dimensiones (L x A x A en metros)",
        "length": "Largo",
        "width": "Ancho",
        "height": "Alto",
        "special_instructions": "Instrucciones Especiales",
        "pickup_datetime": "Fecha y Hora de Recogida",
        "calculate_quote": "Calcular Cotización",
        "estimated_quote": "Cotización Estimada",
        "base_rate": "Tarifa Base",
        "weight_surcharge": "Recargo por Peso",
        "cargo_surcharge": "Recargo por Tipo de Carga",
        "total_estimated_price": "Precio Total Estimado",
        "post_for_bidding": "Publicar para Subasta",
        "book_now": "Reservar Ahora",
        "shipment_posted_success": "¡Envío publicado para subasta exitosamente!",
        "active_shipments": "Envíos Activos",
        "pending_quotes": "Cotizaciones Pendientes",
        "completed_deliveries": "Entregas Completadas",
        "total_spent": "Total Gastado",
        "shipments": "Envíos",
        "status": "Estado",
        "price": "Precio",
        "actions": "Acciones",
        "view": "Ver",
        "all": "Todos",
        "active": "Activos",
        "pending": "Pendientes",
        "completed": "Completados",
        "pending_assignment": "Pendiente de Asignación",
        "assigned": "Asignado",
        "in_transit": "En Tránsito",
        "picked_up": "Recogido",
        "delivered": "Entregado",
        "cancelled": "Cancelado",
        "delayed": "Retrasado",
        "shipment_details": "Detalles del Envío",
        "available_jobs": "Trabajos Disponibles",
        "accept_job": "Aceptar Trabajo",
        "decline_job": "Rechazar Trabajo",
        "job_details": "Detalles del Trabajo",
        "route_distance": "Distancia de Ruta",
        "active_deliveries": "Entregas Activas",
        "earnings": "Ganancias",
        "browse_jobs": "Buscar Trabajos",
        "vehicle_details": "Detalles del Vehículo",
        "fleet_management": "Gestión de Flota",
        "no_jobs_available": "No hay trabajos disponibles en este momento. ¡Vuelve a consultar más tarde!",
        "job_accepted_success": "¡Trabajo aceptado con éxito! Puedes encontrarlo en tu panel de control.",
        "completed_jobs": "Trabajos Completados",
        "access_denied": "Acceso Denegado.",
        "carriers_only": "Solo para Transportistas.",
        "track_shipment": "Rastrear Envío",
        "live_tracking": "Rastreo en Vivo",
        "shipment_timeline": "Cronología del Envío",
        "mark_as_picked_up": "Marcar como Recogido",
        "mark_as_in_transit": "Marcar como en Tránsito",
        "mark_as_delivered": "Marcar como Entregado",
        "eta": "Hora Estimada de Llegada",
        "messages": "Mensajes",
        "send_message": "Enviar Mensaje",
        "type_your_message": "Escribe tu mensaje...",
        "message_sent_success": "Mensaje enviado exitosamente.",
        "no_messages_yet": "Aún no hay mensajes. ¡Inicia la conversación!",
        "message_carrier": "Contactar Transportista",
        "message_shipper": "Contactar Remitente",
        "review": "Revisar",
        "admin_dashboard": "Panel de Administrador",
        "total_users": "Usuarios Totales",
        "total_shippers": "Remitentes Totales",
        "total_carriers": "Transportistas Totales",
        "completed_shipments": "Envíos Completados",
        "total_revenue": "Ingresos Totales",
        "platform_commission": "Comisión de la Plataforma",
        "no_users_for_verification": "No hay usuarios pendientes de verificación.",
        "verifying": "Verificando a",
        "close": "Cerrar",
        "no_documents_uploaded": "Este usuario aún no ha subido ningún documento.",
        "approval_notes_placeholder": "Opcional: Añadir notas para la aprobación...",
        "rejection_reason_placeholder": "Razón del rechazo...",
        "disputes": "Disputas",
        "support_tickets": "Tiquetes de Soporte",
        "financial_overview": "Visión Financiera",
        "create_dispute": "Crear Disputa",
        "dispute_details": "Detalles de la Disputa",
        "view_dispute": "Ver Disputa",
        "payment_issue": "Problema de Pago",
        "service_quality": "Calidad del Servicio",
        "cargo_damage": "Daño a la Carga",
        "delayed_delivery": "Entrega Retrasada",
        "other_issue": "Otro Problema",
        "open": "Abierto",
        "investigating": "Investigando",
        "pending_resolution": "Pendiente de Resolución",
        "resolved": "Resuelto",
        "closed": "Cerrado",
        "new": "Nuevo",
        "in_progress": "En Progreso",
        "waiting_on_user": "Esperando al Usuario",
        "priority": "Prioridad",
        "low": "Baja",
        "medium": "Media",
        "high": "Alta",
        "urgent": "Urgente",
        "complainant": "Demandante",
        "respondent": "Demandado",
        "resolution": "Resolución",
        "assign_to": "Asignar A",
        "admin_response": "Respuesta del Admin",
        "quick_replies": "Respuestas Rápidas",
        "mark_as_investigating": "Marcar como Investigando",
        "mark_as_resolved": "Marcar como Resuelto",
        "total_revenue": "Ingresos Totales",
        "platform_commission": "Comisión de la Plataforma",
        "pending_payouts": "Pagos Pendientes",
        "processed_payouts": "Pagos Procesados",
        "process_payout": "Procesar Pago",
        "payout_queue": "Cola de Pagos",
        "commission_rate": "Tasa de Comisión",
        "transaction_history": "Historial de Transacciones",
        "technical_issue": "Problema Técnico",
        "account_issue": "Problema de Cuenta",
        "billing_issue": "Problema de Facturación",
        "feature_request": "Solicitud de Función",
        "financial": "Financiero",
        "support": "Soporte",
    },
}


class User(TypedDict):
    id: str
    email: str
    password_hash: str
    role: Literal["shipper", "carrier", "admin"]
    full_name: str
    phone: str
    company_name: str | None
    license_number: str | None
    vehicle_type: str | None
    is_verified: bool
    created_at: str


class Document(TypedDict):
    id: str
    user_id: str
    name: str
    path: str
    uploaded_at: str


class Location(TypedDict):
    address: str
    city: str
    province: str
    postal_code: str
    lat: float
    lng: float


class StatusEvent(TypedDict):
    status: str
    timestamp: str


class Shipment(TypedDict):
    id: str
    shipper_id: str
    carrier_id: str | None
    pickup_location: Location
    delivery_location: Location
    cargo_type: Literal["general", "refrigerated", "hazardous", "oversized"]
    weight_kg: float
    length_m: float
    width_m: float
    height_m: float
    special_instructions: str
    pickup_datetime: str
    status: Literal[
        "pending_assignment",
        "assigned",
        "picked_up",
        "in_transit",
        "delivered",
        "cancelled",
        "delayed",
    ]
    price: float | None
    created_at: str
    timeline: list[StatusEvent]
    current_lat: float | None
    current_lng: float | None
    route_polyline: str | None


class Message(TypedDict):
    id: str
    shipment_id: str
    sender_id: str
    sender_role: str
    message_text: str
    timestamp: str
    is_read: bool


class Dispute(TypedDict):
    id: str
    shipment_id: str
    complainant_id: str
    respondent_id: str
    category: str
    priority: str
    description: str
    status: str
    messages: list[dict]
    resolution: str | None
    created_at: str
    updated_at: str


class SupportTicket(TypedDict):
    id: str
    user_id: str
    subject: str
    category: str
    description: str
    priority: str
    status: str
    assigned_to: str | None
    messages: list[dict]
    resolution: str | None
    created_at: str
    updated_at: str


class Payout(TypedDict):
    id: str
    carrier_id: str
    shipment_ids: list[str]
    amount: float
    commission: float
    net_amount: float
    status: str
    payment_method: str
    scheduled_date: str
    processed_date: str | None
    created_at: str


DB: dict[str, list] = {
    "users": [],
    "documents": [],
    "shipments": [],
    "messages": [],
    "disputes": [],
    "support_tickets": [],
    "payouts": [],
}
DB["users"].append(
    {
        "id": "admin",
        "email": "admin@fletor.com",
        "password_hash": "admin123",
        "role": "admin",
        "full_name": "Admin User",
        "phone": "0000-0000",
        "company_name": "Fletor Inc.",
        "license_number": None,
        "vehicle_type": None,
        "is_verified": True,
        "created_at": datetime.datetime.now().isoformat(),
    }
)


class State(rx.State):
    current_language: str = "en"

    @rx.var
    def t(self) -> dict[str, str]:
        return TRANSLATIONS.get(self.current_language, TRANSLATIONS["en"])

    @rx.event
    def toggle_language(self):
        self.current_language = "es" if self.current_language == "en" else "en"


class AuthState(State):
    is_authenticated: bool = False
    user_role: str = ""
    user_id: str = ""
    error_message: str = ""

    @rx.event
    def handle_login(self, form_data: dict):
        self.error_message = ""
        login_email = form_data.get("email")
        login_password = form_data.get("password")
        for user in DB["users"]:
            if user["email"] == login_email and user["password_hash"] == login_password:
                if not user["is_verified"]:
                    self.error_message = "Your account is not verified yet."
                    return
                self.is_authenticated = True
                self.user_id = user["id"]
                self.user_role = user["role"]
                yield rx.redirect("/dashboard")
                return
        self.error_message = self.t["login_failed"]

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.user_role = ""
        self.user_id = ""
        self.error_message = ""
        yield rx.redirect("/")


class RegistrationState(State):
    reg_user_type: str = "shipper"
    reg_full_name: str = ""
    reg_email: str = ""
    reg_phone: str = ""
    reg_company_name: str = ""
    reg_license_number: str = ""
    reg_vehicle_type: str = ""
    reg_password: str = ""
    reg_confirm_password: str = ""
    error_message: str = ""
    success_message: str = ""

    @rx.event
    def handle_registration(self):
        self.error_message = ""
        self.success_message = ""
        if self.reg_password != self.reg_confirm_password:
            self.error_message = self.t["passwords_do_not_match"]
            return
        user_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
        new_user: User = {
            "id": user_id,
            "email": self.reg_email,
            "password_hash": self.reg_password,
            "role": self.reg_user_type,
            "full_name": self.reg_full_name,
            "phone": self.reg_phone,
            "company_name": self.reg_company_name
            if self.reg_user_type == "shipper"
            else None,
            "license_number": self.reg_license_number
            if self.reg_user_type == "carrier"
            else None,
            "vehicle_type": self.reg_vehicle_type
            if self.reg_user_type == "carrier"
            else None,
            "is_verified": False,
            "created_at": datetime.datetime.now().isoformat(),
        }
        DB["users"].append(new_user)
        self.success_message = self.t["registration_successful"]
        yield rx.toast.success(self.t["registration_successful"])
        yield rx.redirect("/login")
        self._reset_fields()

    def _reset_fields(self):
        self.reg_full_name = ""
        self.reg_email = ""
        self.reg_phone = ""
        self.reg_company_name = ""
        self.reg_license_number = ""
        self.reg_vehicle_type = ""
        self.reg_password = ""
        self.reg_confirm_password = ""


class ProfileState(State):
    user_documents: list[Document] = []

    @rx.var
    async def current_user(self) -> User | None:
        auth = await self.get_state(AuthState)
        if not auth.is_authenticated:
            return None
        for user in DB["users"]:
            if user["id"] == auth.user_id:
                return cast(User, user)
        return None

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("You must be logged in to upload files.")
            return
        for file in files:
            upload_data = await file.read()
            upload_dir = rx.get_upload_dir()
            upload_dir.mkdir(parents=True, exist_ok=True)
            file_path = upload_dir / file.name
            with file_path.open("wb") as f:
                f.write(upload_data)
            doc_id = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
            new_doc: Document = {
                "id": doc_id,
                "user_id": auth_state.user_id,
                "name": file.name,
                "path": file.name,
                "uploaded_at": datetime.datetime.now().isoformat(),
            }
            DB["documents"].append(new_doc)
            self.user_documents.append(new_doc)
        yield rx.toast.success(f"Successfully uploaded {len(files)} file(s).")

    @rx.event
    async def load_documents(self):
        auth = await self.get_state(AuthState)
        self.user_documents = [
            doc for doc in DB["documents"] if doc["user_id"] == auth.user_id
        ]


class AdminState(State):
    users_for_verification: list[User] = []
    selected_user_for_verification: User | None = None
    selected_user_documents: list[Document] = []
    rejection_reason: str = ""
    approval_notes: str = ""
    analytics: dict = {
        "total_users": 0,
        "total_shippers": 0,
        "total_carriers": 0,
        "active_shipments": 0,
        "completed_shipments": 0,
        "total_revenue": 0.0,
        "platform_commission": 0.0,
    }
    disputes: list[Dispute] = []
    support_tickets: list[SupportTicket] = []
    financial_overview: dict = {
        "total_revenue": 0.0,
        "platform_commission": 0.0,
        "pending_payouts": 0.0,
        "processed_payouts": 0.0,
    }
    payouts: list[Payout] = []
    selected_dispute: Dispute | None = None
    selected_ticket: SupportTicket | None = None
    dispute_filter: str = "all"
    ticket_filter: str = "all"

    @rx.event
    def load_admin_dashboard(self):
        self.load_unverified_users()
        self.load_analytics()
        self.load_disputes()
        self.load_support_tickets()
        self.load_financial_overview()
        self.load_payout_history()

    @rx.event
    def load_analytics(self):
        total_users = len(DB["users"]) - 1
        total_shippers = len([u for u in DB["users"] if u["role"] == "shipper"])
        total_carriers = len([u for u in DB["users"] if u["role"] == "carrier"])
        active_shipments = len(
            [
                s
                for s in DB["shipments"]
                if s["status"] not in ["delivered", "cancelled"]
            ]
        )
        completed_shipments = len(
            [s for s in DB["shipments"] if s["status"] == "delivered"]
        )
        total_revenue = sum(
            (
                s["price"]
                for s in DB["shipments"]
                if s["price"] is not None and s["status"] == "delivered"
            )
        )
        platform_commission = total_revenue * 0.1
        self.analytics = {
            "total_users": total_users,
            "total_shippers": total_shippers,
            "total_carriers": total_carriers,
            "active_shipments": active_shipments,
            "completed_shipments": completed_shipments,
            "total_revenue": total_revenue,
            "platform_commission": platform_commission,
        }

    @rx.event
    def load_unverified_users(self):
        self.users_for_verification = [
            cast(User, user)
            for user in DB["users"]
            if not user["is_verified"] and user["role"] != "admin"
        ]

    @rx.event
    def select_user_for_verification(self, user: User):
        self.selected_user_for_verification = user
        self.selected_user_documents = [
            d for d in DB["documents"] if d["user_id"] == user["id"]
        ]
        self.approval_notes = ""
        self.rejection_reason = ""

    @rx.event
    def deselect_user(self):
        self.selected_user_for_verification = None
        self.selected_user_documents = []

    @rx.event
    def approve_user_with_notes(self):
        if not self.selected_user_for_verification:
            return
        user_id = self.selected_user_for_verification["id"]
        for user in DB["users"]:
            if user["id"] == user_id:
                user["is_verified"] = True
                break
        self.load_unverified_users()
        self.deselect_user()
        yield rx.toast.success(f"User {user_id} approved.")

    @rx.event
    def reject_user_with_reason(self):
        if not self.selected_user_for_verification:
            return
        user_id = self.selected_user_for_verification["id"]
        DB["users"] = [user for user in DB["users"] if user["id"] != user_id]
        self.load_unverified_users()
        self.deselect_user()
        yield rx.toast.info(f"User {user_id} rejected and removed.")

    @rx.event
    def load_disputes(self):
        self.disputes = sorted(
            DB["disputes"], key=lambda d: d["created_at"], reverse=True
        )

    @rx.event
    def load_support_tickets(self):
        self.support_tickets = sorted(
            DB["support_tickets"], key=lambda t: t["created_at"], reverse=True
        )

    @rx.event
    def load_financial_overview(self):
        total_revenue = sum(
            (s["price"] for s in DB["shipments"] if s["status"] == "delivered"), 0.0
        )
        platform_commission = total_revenue * 0.1
        pending_payouts = sum(
            (p["net_amount"] for p in DB["payouts"] if p["status"] == "pending"), 0.0
        )
        processed_payouts = sum(
            (p["net_amount"] for p in DB["payouts"] if p["status"] == "processed"), 0.0
        )
        self.financial_overview = {
            "total_revenue": total_revenue,
            "platform_commission": platform_commission,
            "pending_payouts": pending_payouts,
            "processed_payouts": processed_payouts,
        }

    @rx.event
    def load_payout_history(self):
        self.payouts = sorted(
            DB["payouts"], key=lambda p: p["created_at"], reverse=True
        )

    @rx.event
    async def create_dispute(self, shipment_id, category, priority, description):
        auth_state = await self.get_state(AuthState)
        shipment = await self._get_shipment_by_id(shipment_id)
        if not auth_state.is_authenticated or not shipment:
            return
        dispute_id = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        new_dispute = Dispute(
            id=dispute_id,
            shipment_id=shipment_id,
            complainant_id=auth_state.user_id,
            respondent_id=shipment["carrier_id"]
            if auth_state.user_role == "shipper"
            else shipment["shipper_id"],
            category=category,
            priority=priority,
            description=description,
            status="open",
            messages=[],
            resolution=None,
            created_at=datetime.datetime.now().isoformat(),
            updated_at=datetime.datetime.now().isoformat(),
        )
        DB["disputes"].append(new_dispute)
        self.load_disputes()
        yield rx.toast.success("Dispute created successfully.")

    @rx.event
    async def create_support_ticket(self, subject, category, description, priority):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        ticket_id = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        new_ticket = SupportTicket(
            id=ticket_id,
            user_id=auth_state.user_id,
            subject=subject,
            category=category,
            description=description,
            priority=priority,
            status="new",
            assigned_to=None,
            messages=[],
            resolution=None,
            created_at=datetime.datetime.now().isoformat(),
            updated_at=datetime.datetime.now().isoformat(),
        )
        DB["support_tickets"].append(new_ticket)
        self.load_support_tickets()
        yield rx.toast.success("Support ticket created successfully.")


class CarrierState(State):
    available_jobs: list[Shipment] = []
    filtered_jobs: list[Shipment] = []
    cargo_type_filter: str = "all"
    max_weight_filter: int = 50000

    @rx.event
    async def load_available_jobs(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.user_role == "carrier":
            self.available_jobs = [
                s for s in DB["shipments"] if s["status"] == "pending_assignment"
            ]
            self.apply_filters()

    @rx.event
    def apply_filters(self):
        jobs = self.available_jobs
        if self.cargo_type_filter != "all":
            jobs = [j for j in jobs if j["cargo_type"] == self.cargo_type_filter]
        jobs = [j for j in jobs if j["weight_kg"] <= self.max_weight_filter]
        self.filtered_jobs = jobs

    @rx.event
    def set_cargo_type_filter(self, cargo_type: str):
        self.cargo_type_filter = cargo_type
        self.apply_filters()

    @rx.event
    def set_max_weight_filter(self, weight: str):
        self.max_weight_filter = int(weight)
        self.apply_filters()

    @rx.event
    async def accept_job(self, shipment_id: str):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.user_role != "carrier":
            yield rx.toast.error("You are not authorized to accept jobs.")
            return
        tracking_state = await self.get_state(TrackingState)
        for shipment in DB["shipments"]:
            if shipment["id"] == shipment_id:
                shipment["status"] = "assigned"
                shipment["carrier_id"] = auth_state.user_id
                shipment["current_lat"] = shipment["pickup_location"]["lat"]
                shipment["current_lng"] = shipment["pickup_location"]["lng"]
                await tracking_state.add_status_event(shipment_id, "assigned")
                yield rx.toast.success(self.t["job_accepted_success"])
                yield rx.redirect("/dashboard")
                return


class ShipmentState(State):
    shipments: list[Shipment] = []
    carrier_shipments: list[Shipment] = []
    carrier_dashboard_stats: dict = {
        "available_jobs": 0,
        "active_deliveries": 0,
        "completed_jobs": 0,
        "total_earnings": 0.0,
    }
    filtered_shipments: list[Shipment] = []
    shipment_filter: str = "all"
    new_shipment: dict = {
        "id": "",
        "shipper_id": "",
        "carrier_id": None,
        "pickup_location": {
            "address": "",
            "city": "",
            "province": "",
            "postal_code": "",
            "lat": 9.93,
            "lng": -84.08,
        },
        "delivery_location": {
            "address": "",
            "city": "",
            "province": "",
            "postal_code": "",
            "lat": 10.0,
            "lng": -84.21,
        },
        "cargo_type": "general",
        "weight_kg": 0.0,
        "length_m": 0.0,
        "width_m": 0.0,
        "height_m": 0.0,
        "special_instructions": "",
        "pickup_datetime": "",
        "status": "pending_assignment",
        "price": None,
        "created_at": "",
        "timeline": [],
        "current_lat": None,
        "current_lng": None,
        "route_polyline": None,
    }
    estimated_quote: dict[str, float] = {}

    @rx.event
    async def load_shipper_shipments(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "shipper":
            self.shipments = [
                s for s in DB["shipments"] if s["shipper_id"] == auth_state.user_id
            ]
            self.apply_shipper_filter()

    @rx.event
    async def load_carrier_dashboard_data(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "carrier":
            self.carrier_shipments = [
                s for s in DB["shipments"] if s["carrier_id"] == auth_state.user_id
            ]
            active_deliveries = len(
                [
                    s
                    for s in self.carrier_shipments
                    if s["status"] in ["assigned", "in_transit", "picked_up"]
                ]
            )
            completed_jobs = len(
                [s for s in self.carrier_shipments if s["status"] == "delivered"]
            )
            total_earnings = sum(
                (
                    s["price"]
                    for s in self.carrier_shipments
                    if s["status"] == "delivered" and s["price"] is not None
                ),
                0.0,
            )
            available_jobs = len(
                [s for s in DB["shipments"] if s["status"] == "pending_assignment"]
            )
            self.carrier_dashboard_stats = {
                "available_jobs": available_jobs,
                "active_deliveries": active_deliveries,
                "completed_jobs": completed_jobs,
                "total_earnings": total_earnings,
            }

    @rx.event
    def set_shipment_filter(self, new_filter: str):
        self.shipment_filter = new_filter
        self.apply_shipper_filter()

    @rx.event
    def apply_shipper_filter(self):
        if self.shipment_filter == "all":
            self.filtered_shipments = self.shipments
        elif self.shipment_filter == "active":
            self.filtered_shipments = [
                s
                for s in self.shipments
                if s["status"]
                in ["pending_assignment", "assigned", "in_transit", "picked_up"]
            ]
        else:
            self.filtered_shipments = [
                s for s in self.shipments if s["status"] == self.shipment_filter
            ]

    def _update_new_shipment(self, field, value, nested_field=None):
        if nested_field:
            self.new_shipment[nested_field][field] = value
        else:
            self.new_shipment[field] = value

    @rx.event
    def set_pickup_address(self, value: str):
        self._update_new_shipment("address", value, "pickup_location")

    @rx.event
    def set_pickup_city(self, value: str):
        self._update_new_shipment("city", value, "pickup_location")

    @rx.event
    def set_pickup_province(self, value: str):
        self._update_new_shipment("province", value, "pickup_location")

    @rx.event
    def set_pickup_postal_code(self, value: str):
        self._update_new_shipment("postal_code", value, "pickup_location")

    @rx.event
    def set_delivery_address(self, value: str):
        self._update_new_shipment("address", value, "delivery_location")

    @rx.event
    def set_delivery_city(self, value: str):
        self._update_new_shipment("city", value, "delivery_location")

    @rx.event
    def set_delivery_province(self, value: str):
        self._update_new_shipment("province", value, "delivery_location")

    @rx.event
    def set_delivery_postal_code(self, value: str):
        self._update_new_shipment("postal_code", value, "delivery_location")

    @rx.event
    def set_cargo_type(self, value: str):
        self._update_new_shipment("cargo_type", value)

    @rx.event
    def set_weight_kg(self, value: str):
        self._update_new_shipment("weight_kg", float(value))

    @rx.event
    def set_length_m(self, value: str):
        self._update_new_shipment("length_m", float(value))

    @rx.event
    def set_width_m(self, value: str):
        self._update_new_shipment("width_m", float(value))

    @rx.event
    def set_height_m(self, value: str):
        self._update_new_shipment("height_m", float(value))

    @rx.event
    def set_special_instructions(self, value: str):
        self._update_new_shipment("special_instructions", value)

    @rx.event
    def set_pickup_datetime(self, value: str):
        self._update_new_shipment("pickup_datetime", value)

    @rx.event
    def calculate_quote(self):
        base_rate = 50.0
        weight_surcharge = self.new_shipment["weight_kg"] * 0.1
        cargo_multipliers = {
            "general": 1,
            "refrigerated": 1.5,
            "hazardous": 2,
            "oversized": 1.8,
        }
        cargo_surcharge = base_rate * (
            cargo_multipliers.get(self.new_shipment["cargo_type"], 1) - 1
        )
        total = base_rate + weight_surcharge + cargo_surcharge
        self.estimated_quote = {
            "base_rate": base_rate,
            "weight_surcharge": weight_surcharge,
            "cargo_surcharge": cargo_surcharge,
            "total": total,
        }

    @rx.event
    async def post_shipment_for_bidding(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            return
        tracking_state = await self.get_state(TrackingState)
        self.new_shipment["id"] = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        self.new_shipment["shipper_id"] = auth_state.user_id
        self.new_shipment["created_at"] = datetime.datetime.now().isoformat()
        self.new_shipment["price"] = self.estimated_quote.get("total")
        self.new_shipment["status"] = "pending_assignment"
        new_shipment_obj = self.new_shipment.copy()
        DB["shipments"].append(new_shipment_obj)
        await tracking_state.add_status_event(
            new_shipment_obj["id"], "pending_assignment"
        )
        yield rx.toast.success(self.t["shipment_posted_success"])
        yield rx.redirect("/dashboard")


class TrackingState(State):
    shipment: Shipment | None = None
    is_tracking_active: bool = False
    eta: str = ""

    async def _get_shipment_by_id(self, shipment_id: str) -> Shipment | None:
        for s in DB["shipments"]:
            if s["id"] == shipment_id:
                return cast(Shipment, s)
        return None

    @rx.event
    async def load_shipment_for_tracking(self):
        shipment_id = self.router.page.params.get("id")
        if not shipment_id:
            yield rx.redirect("/dashboard")
            return
        shipment = await self._get_shipment_by_id(shipment_id)
        if shipment:
            self.shipment = shipment
            self.is_tracking_active = shipment["status"] in ["picked_up", "in_transit"]
            self.calculate_eta()
            if self.is_tracking_active:
                yield TrackingState.simulate_gps_updates
                return
        else:
            yield rx.redirect("/dashboard")

    @rx.event(background=True)
    async def simulate_gps_updates(self):
        async with self:
            if not self.shipment or not self.is_tracking_active:
                return
        import asyncio

        while True:
            async with self:
                if not self.shipment or not self.is_tracking_active:
                    break
                target_lat = self.shipment["delivery_location"]["lat"]
                target_lng = self.shipment["delivery_location"]["lng"]
                current_lat = self.shipment["current_lat"]
                current_lng = self.shipment["current_lng"]
                if current_lat is None or current_lng is None:
                    break
                lat_diff = target_lat - current_lat
                lng_diff = target_lng - current_lng
                distance_to_target = (lat_diff**2 + lng_diff**2) ** 0.5
                if distance_to_target < 0.001:
                    self.shipment["current_lat"] = target_lat
                    self.shipment["current_lng"] = target_lng
                    self.is_tracking_active = False
                    break
                step = 0.002
                self.shipment["current_lat"] += lat_diff / distance_to_target * step
                self.shipment["current_lng"] += lng_diff / distance_to_target * step
                self.calculate_eta()
            await asyncio.sleep(5)

    @rx.event
    async def add_status_event(self, shipment_id: str, status: str):
        shipment = await self._get_shipment_by_id(shipment_id)
        if shipment:
            new_event = StatusEvent(
                status=status, timestamp=datetime.datetime.now().isoformat()
            )
            if "timeline" not in shipment or shipment["timeline"] is None:
                shipment["timeline"] = []
            shipment["timeline"].append(new_event)

    @rx.event
    async def change_shipment_status(self, new_status: str):
        if not self.shipment:
            return
        shipment_id = self.shipment["id"]
        shipment = await self._get_shipment_by_id(shipment_id)
        if shipment:
            shipment["status"] = new_status
            await self.add_status_event(shipment_id, new_status)
            self.shipment = shipment
            if new_status in ["picked_up", "in_transit"]:
                self.is_tracking_active = True
                yield TrackingState.simulate_gps_updates
            else:
                self.is_tracking_active = False
            yield rx.toast.success(f"Status updated to {self.t[new_status]}")

    @rx.event
    def calculate_eta(self):
        if (
            not self.shipment
            or self.shipment.get("current_lat") is None
            or self.shipment.get("current_lng") is None
        ):
            self.eta = "N/A"
            return
        from math import sin, cos, sqrt, atan2, radians

        lat1 = radians(self.shipment["current_lat"])
        lon1 = radians(self.shipment["current_lng"])
        lat2 = radians(self.shipment["delivery_location"]["lat"])
        lon2 = radians(self.shipment["delivery_location"]["lng"])
        R = 6371
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance_km = R * c
        avg_speed_kph = 60
        if avg_speed_kph > 0:
            time_hours = distance_km / avg_speed_kph
            eta_datetime = datetime.datetime.now() + datetime.timedelta(
                hours=time_hours
            )
            self.eta = eta_datetime.strftime("%Y-%m-%d %H:%M")
        else:
            self.eta = "N/A"


class MessagingState(State):
    messages: list[Message] = []
    new_message_text: str = ""
    current_shipment_id: str = ""

    @rx.event
    async def load_conversation(self):
        shipment_id = self.router.page.params.get("id")
        if not shipment_id:
            yield rx.redirect("/dashboard")
            return
        self.current_shipment_id = shipment_id
        self.messages = [
            cast(Message, m)
            for m in DB["messages"]
            if m["shipment_id"] == self.current_shipment_id
        ]
        self.messages.sort(key=lambda m: m["timestamp"])
        yield MessagingState.poll_for_new_messages

    @rx.event
    async def send_message(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or not self.new_message_text.strip():
            return
        message_id = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        new_message: Message = {
            "id": message_id,
            "shipment_id": self.current_shipment_id,
            "sender_id": auth_state.user_id,
            "sender_role": auth_state.user_role,
            "message_text": self.new_message_text,
            "timestamp": datetime.datetime.now().isoformat(),
            "is_read": False,
        }
        DB["messages"].append(new_message)
        self.messages.append(new_message)
        self.new_message_text = ""
        yield rx.toast.success(self.t["message_sent_success"])

    @rx.event(background=True)
    async def poll_for_new_messages(self):
        import asyncio

        last_check_count = len(self.messages)
        while True:
            await asyncio.sleep(5)
            async with self:
                current_messages = [
                    cast(Message, m)
                    for m in DB["messages"]
                    if m["shipment_id"] == self.current_shipment_id
                ]
                if len(current_messages) > last_check_count:
                    current_messages.sort(key=lambda m: m["timestamp"])
                    self.messages = current_messages
                    last_check_count = len(current_messages)
                    yield rx.toast.info("New message received!")