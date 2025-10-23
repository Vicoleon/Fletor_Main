import reflex as rx
from typing import TypedDict, Literal, cast
import random
import string
import datetime
import uuid
import bcrypt
from sqlalchemy import text
from app.db_utils import save_uploaded_file, get_user_documents

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
        "PENDING": "Pending",
        "ACCEPTED": "Accepted",
        "PICKUP_SCHEDULED": "Pickup Scheduled",
        "IN_TRANSIT": "In Transit",
        "DELIVERED": "Delivered",
        "CANCELLED": "Cancelled",
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
        "compliance": "Compliance",
        "compliance_dashboard": "Compliance Dashboard",
        "license_expiry": "License Expiry",
        "insurance_expiry": "Insurance Expiry",
        "inspection_expiry": "Inspection Expiry",
        "compliance_status": "Compliance Status",
        "compliant": "Compliant",
        "expiring_soon": "Expiring Soon",
        "expired": "Expired",
        "filter_by_status": "Filter by status",
        "search_carrier": "Search by name or license...",
        "suspend": "Suspend",
        "unsuspend": "Unsuspend",
        "suspension_reason": "Suspension Reason",
        "policy_violation": "Policy Violation",
        "fraud": "Fraud",
        "other": "Other",
        "notes": "Notes",
        "confirm_suspension": "Confirm Suspension",
        "cancel": "Cancel",
        "user_suspended": "User suspended.",
        "user_unsuspended": "User unsuspended.",
        "activity_logs": "Activity Logs",
        "action_type": "Action Type",
        "user": "User",
        "admin_user": "Admin User",
        "timestamp": "Timestamp",
        "target": "Target",
        "filter_by_action": "Filter by action type",
        "select_date_range": "Select date range",
        "user_approved": "User Approved",
        "user_rejected": "User Rejected",
        "user_suspended": "User Suspended",
        "user_unsuspended": "User Unsuspended",
        "dispute_resolved": "Dispute Resolved",
        "ticket_closed": "Ticket Closed",
        "reports": "Reports",
        "reporting_dashboard": "Reporting Dashboard",
        "revenue_trends": "Revenue Trends",
        "shipment_volume": "Shipment Volume",
        "user_growth": "User Growth",
        "popular_routes": "Popular Routes",
        "carrier_performance": "Carrier Performance",
        "daily": "Daily",
        "weekly": "Weekly",
        "monthly": "Monthly",
        "export_csv": "Export CSV",
        "export_pdf": "Export PDF",
        "completion_rate": "Completion Rate",
        "average_rating": "Average Rating",
        "total_earnings": "Total Earnings",
        "invoices": "Invoices",
        "payments": "Payments",
        "payment_methods": "Payment Methods",
        "add_payment_method": "Add Payment Method",
        "sinpe_mobile": "SINPE Móvil",
        "bank_transfer": "Bank Transfer",
        "phone_number_8_digits": "Phone Number (8 digits)",
        "add_sinpe": "Add SINPE Móvil",
        "iban_account": "IBAN Account Number",
        "add_bank_account": "Add Bank Account",
        "payment_history": "Payment History",
        "transaction_id": "Transaction ID",
        "amount": "Amount",
        "date": "Date",
        "method": "Method",
        "invoice_number": "Invoice #",
        "issue_date": "Issue Date",
        "due_date": "Due Date",
        "total": "Total",
        "download_pdf": "Download PDF",
        "no_invoices": "You have no invoices.",
        "draft": "Draft",
        "issued": "Issued",
        "paid": "Paid",
        "overdue": "Overdue",
        "carrier_earnings": "Carrier Earnings",
        "net_earnings": "Net Earnings",
        "payout_history": "Payout History",
        "request_payout": "Request Payout",
        "available_for_payout": "Available for Payout",
        "no_earnings_yet": "No earnings to display yet.",
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
        "PENDING": "Pendiente",
        "ACCEPTED": "Aceptado",
        "PICKUP_SCHEDULED": "Recogida Programada",
        "IN_TRANSIT": "En Tránsito",
        "DELIVERED": "Entregado",
        "CANCELLED": "Cancelado",
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
        "pending_resolution": "Pendiente de ResoluciÃ³n",
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
        "compliance": "Cumplimiento",
        "compliance_dashboard": "Panel de Cumplimiento",
        "license_expiry": "Vencimiento de Licencia",
        "insurance_expiry": "Vencimiento de Seguro",
        "inspection_expiry": "Vencimiento de Inspección",
        "compliance_status": "Estado de Cumplimiento",
        "compliant": "Conforme",
        "expiring_soon": "Vence Pronto",
        "expired": "Vencido",
        "filter_by_status": "Filtrar por estado",
        "search_carrier": "Buscar por nombre o licencia...",
        "suspend": "Suspender",
        "unsuspend": "Reactivar",
        "suspension_reason": "Razón de Suspensión",
        "policy_violation": "Violación de Política",
        "fraud": "Fraude",
        "other": "Otro",
        "notes": "Notas",
        "confirm_suspension": "Confirmar Suspensión",
        "cancel": "Cancelar",
        "user_suspended": "Usuario suspendido.",
        "user_unsuspended": "Usuario reactivado.",
        "activity_logs": "Registros de Actividad",
        "action_type": "Tipo de Acción",
        "user": "Usuario",
        "admin_user": "Usuario Admin",
        "timestamp": "Fecha y Hora",
        "target": "Objetivo",
        "filter_by_action": "Filtrar por tipo de acción",
        "select_date_range": "Seleccionar rango de fechas",
        "user_approved": "Usuario Aprobado",
        "user_rejected": "Usuario Rechazado",
        "user_suspended": "Usuario Suspendido",
        "user_unsuspended": "Usuario Reactivado",
        "dispute_resolved": "Disputa Resuelta",
        "ticket_closed": "Tiquete Cerrado",
        "reports": "Informes",
        "reporting_dashboard": "Panel de Informes",
        "revenue_trends": "Tendencias de Ingresos",
        "shipment_volume": "Volumen de Envíos",
        "user_growth": "Crecimiento de Usuarios",
        "popular_routes": "Rutas Populares",
        "carrier_performance": "Rendimiento de Transportistas",
        "daily": "Diario",
        "weekly": "Semanal",
        "monthly": "Mensual",
        "export_csv": "Exportar CSV",
        "export_pdf": "Exportar PDF",
        "completion_rate": "Tasa de Finalización",
        "average_rating": "Calificación Promedio",
        "total_earnings": "Ganancias Totales",
        "invoices": "Facturas",
        "payments": "Pagos",
        "payment_methods": "Métodos de Pago",
        "add_payment_method": "Agregar Método de Pago",
        "sinpe_mobile": "SINPE Móvil",
        "bank_transfer": "Transferencia Bancaria",
        "phone_number_8_digits": "Número de Teléfono (8 dígitos)",
        "add_sinpe": "Agregar SINPE Móvil",
        "iban_account": "Número de Cuenta IBAN",
        "add_bank_account": "Agregar Cuenta Bancaria",
        "payment_history": "Historial de Pagos",
        "transaction_id": "ID de Transacción",
        "amount": "Monto",
        "date": "Fecha",
        "method": "Método",
        "invoice_number": "Factura #",
        "issue_date": "Fecha de Emisión",
        "due_date": "Fecha de Vencimiento",
        "total": "Total",
        "download_pdf": "Descargar PDF",
        "no_invoices": "No tienes facturas.",
        "draft": "Borrador",
        "issued": "Emitida",
        "paid": "Pagada",
        "overdue": "Vencida",
        "carrier_earnings": "Ganancias del Transportista",
        "net_earnings": "Ganancias Netas",
        "payout_history": "Historial de Pagos",
        "request_payout": "Solicitar Pago",
        "available_for_payout": "Disponible para Retiro",
        "no_earnings_yet": "Aún no hay ganancias para mostrar.",
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
    license_expiry: str | None
    insurance_expiry: str | None
    inspection_expiry: str | None
    is_suspended: bool
    suspension_reason: str | None
    suspended_at: str | None
    suspended_by: str | None


class CarrierData(User):
    compliance_status: str
    days_to_expiry: int


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


class ActivityLog(TypedDict):
    id: str
    timestamp: str
    admin_user_id: str
    action_type: str
    target_id: str
    notes: str | None


class Invoice(TypedDict):
    id: str
    invoice_number: str
    shipment_id: str
    shipper_id: str
    issue_date: str
    due_date: str
    subtotal: float
    tax: float
    total: float
    status: str


DB: dict[str, list] = {
    "users": [],
    "documents": [],
    "shipments": [],
    "messages": [],
    "disputes": [],
    "support_tickets": [],
    "payouts": [],
    "activity_logs": [],
    "invoices": [],
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
        "license_expiry": None,
        "insurance_expiry": None,
        "inspection_expiry": None,
        "is_suspended": False,
        "suspension_reason": None,
        "suspended_at": None,
        "suspended_by": None,
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
    async def handle_login(self, form_data: dict):
        from app.db_utils import get_user_by_email, verify_password

        self.error_message = ""
        login_email = form_data.get("email")
        login_password = form_data.get("password")
        user = await get_user_by_email(login_email)
        if not user:
            self.error_message = self.t["user_not_found"]
            return
        if not verify_password(login_password, user.password_hash):
            self.error_message = self.t["login_failed"]
            return
        if user.status != "ACTIVE":
            self.error_message = (
                f"Account status is {user.status}. Please contact support."
            )
            return
        self.is_authenticated = True
        self.user_id = user.id
        self.user_role = user.role.lower()
        yield rx.redirect("/dashboard")

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
    async def handle_registration(self, form_data: dict):
        self.error_message = ""
        self.success_message = ""
        if self.reg_password != self.reg_confirm_password:
            self.error_message = self.t["passwords_do_not_match"]
            return
        if len(self.reg_password) < 8:
            self.error_message = "Password must be at least 8 characters long."
            return
        user_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(
            self.reg_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        first_name, *last_name_parts = self.reg_full_name.split()
        last_name = " ".join(last_name_parts)
        async with rx.asession() as session:
            result = await session.execute(
                text("SELECT id FROM users WHERE email = :email"),
                {"email": self.reg_email},
            )
            if result.first():
                self.error_message = "An account with this email already exists."
                return
            await session.execute(
                text("""INSERT INTO users (id, email, "passwordHash", "userType", "firstName", "lastName", phone, "nationalId", "companyName", status, "kycStatus")
                       VALUES (:id, :email, :password_hash, :user_type, :first_name, :last_name, :phone, :national_id, :company_name, 'PENDING', 'PENDING')"""),
                {
                    "id": user_id,
                    "email": self.reg_email,
                    "password_hash": password_hash,
                    "user_type": self.reg_user_type.upper(),
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": self.reg_phone,
                    "national_id": self.reg_license_number
                    if self.reg_user_type == "carrier"
                    else None,
                    "company_name": self.reg_company_name
                    if self.reg_user_type == "shipper"
                    else None,
                },
            )
            if self.reg_user_type == "carrier":
                license_expiry = (
                    datetime.date.today()
                    + datetime.timedelta(days=random.randint(30, 730))
                ).isoformat()
                insurance_expiry = (
                    datetime.date.today()
                    + datetime.timedelta(days=random.randint(30, 365))
                ).isoformat()
                inspection_expiry = (
                    datetime.date.today()
                    + datetime.timedelta(days=random.randint(30, 180))
                ).isoformat()
                carrier_id = str(uuid.uuid4())
                await session.execute(
                    text("""INSERT INTO carriers (id, "userId", "licenseExpiry", "insuranceExpiry", "inspectionExpiry")
                           VALUES (:id, :user_id, :license_expiry, :insurance_expiry, :inspection_expiry)"""),
                    {
                        "id": carrier_id,
                        "user_id": user_id,
                        "license_expiry": license_expiry,
                        "insurance_expiry": insurance_expiry,
                        "inspection_expiry": inspection_expiry,
                    },
                )
            await session.commit()
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
            import uuid

            unique_suffix = str(uuid.uuid4())[:8]
            unique_filename = f"{unique_suffix}_{file.name}"
            file_path = upload_dir / unique_filename
            with file_path.open("wb") as f:
                f.write(upload_data)
            await save_uploaded_file(
                user_id=auth_state.user_id,
                file_name=file.name,
                file_path=unique_filename,
                file_size=len(upload_data),
                mime_type=file.content_type,
            )
        await self.load_documents()
        yield rx.toast.success(f"Successfully uploaded {len(files)} file(s).")

    @rx.event
    async def load_documents(self):
        auth = await self.get_state(AuthState)
        if auth.is_authenticated:
            self.user_documents = await get_user_documents(auth.user_id)


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
    async def load_admin_dashboard(self):
        await self.load_unverified_users()
        await self.load_analytics()
        self.load_disputes()
        self.load_support_tickets()
        self.load_financial_overview()
        self.load_payout_history()

    @rx.event
    async def load_analytics(self):
        from app.db_utils import get_platform_analytics

        self.analytics = await get_platform_analytics()

    @rx.event
    async def load_unverified_users(self):
        from app.db_utils import get_users_for_verification

        self.users_for_verification = await get_users_for_verification()

    @rx.event
    @rx.event
    async def select_user_for_verification(self, user: User):
        self.selected_user_for_verification = user
        self.selected_user_documents = await get_user_documents(user["id"])
        self.approval_notes = ""
        self.rejection_reason = ""

    @rx.event
    def deselect_user(self):
        self.selected_user_for_verification = None
        self.selected_user_documents = []

    @rx.event
    async def approve_user_with_notes(self):
        from app.db_utils import approve_user, create_activity_log

        if not self.selected_user_for_verification:
            return
        user_id = self.selected_user_for_verification["id"]
        auth_state = await self.get_state(AuthState)
        await approve_user(user_id)
        await create_activity_log(
            admin_user_id=auth_state.user_id,
            action_type="user_approved",
            target_id=user_id,
            notes=self.approval_notes,
        )
        await self.load_unverified_users()
        self.deselect_user()
        yield rx.toast.success(f"User {user_id} approved.")

    @rx.event
    async def reject_user_with_reason(self):
        from app.db_utils import reject_user, create_activity_log

        if not self.selected_user_for_verification:
            return
        user_id = self.selected_user_for_verification["id"]
        auth_state = await self.get_state(AuthState)
        await reject_user(user_id)
        await create_activity_log(
            admin_user_id=auth_state.user_id,
            action_type="user_rejected",
            target_id=user_id,
            notes=self.rejection_reason,
        )
        await self.load_unverified_users()
        self.deselect_user()
        yield rx.toast.info(f"User {user_id} rejected.")

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

    async def _get_shipment_by_id(self, shipment_id: str) -> Shipment | None:
        for s in DB["shipments"]:
            if s["id"] == shipment_id:
                return cast(Shipment, s)
        return None

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


class ComplianceState(State):
    carriers: list[User] = []
    filtered_carriers: list[CarrierData] = []
    status_filter: str = "all"
    search_query: str = ""
    user_to_suspend: User | None = None
    suspension_reason: str = "policy_violation"
    suspension_notes: str = ""

    @rx.event
    async def load_carriers(self):
        from app.db_utils import get_carriers_with_compliance

        carriers_data = await get_carriers_with_compliance()
        self.carriers = carriers_data
        self.apply_filters()

    def _get_compliance_status(self, carrier: User) -> tuple[str, int]:
        today = datetime.date.today()
        exp_dates = [
            carrier.get("license_expiry"),
            carrier.get("insurance_expiry"),
            carrier.get("inspection_expiry"),
        ]
        min_days = 9999
        has_expired = False
        for date_str in exp_dates:
            if date_str:
                try:
                    exp_date = datetime.date.fromisoformat(date_str)
                    days_left = (exp_date - today).days
                    if days_left < 0:
                        has_expired = True
                    min_days = min(min_days, days_left)
                except (ValueError, TypeError) as e:
                    import logging

                    logging.exception(f"Error parsing date: {e}")
                    continue
        if has_expired or min_days < 0:
            return ("expired", min_days)
        if min_days <= 7:
            return ("expiring_soon", min_days)
        if min_days <= 30:
            return ("expiring_soon", min_days)
        return ("compliant", min_days)

    @rx.var
    def carriers_with_status(self) -> list[CarrierData]:
        carrier_list: list[CarrierData] = []
        for c in self.carriers:
            status, days = self._get_compliance_status(c)
            carrier_dict = cast(dict, c).copy()
            carrier_dict["compliance_status"] = status
            carrier_dict["days_to_expiry"] = days
            carrier_list.append(cast(CarrierData, carrier_dict))
        return carrier_list

    @rx.event
    def apply_filters(self):
        carriers = self.carriers_with_status
        if self.status_filter != "all":
            carriers = [
                c for c in carriers if c["compliance_status"] == self.status_filter
            ]
        if self.search_query:
            query = self.search_query.lower()
            carriers = [
                c
                for c in carriers
                if query in c["full_name"].lower()
                or (c["license_number"] and query in c["license_number"])
            ]
        self.filtered_carriers = carriers

    @rx.event
    def set_status_filter(self, status: str):
        self.status_filter = status
        self.apply_filters()

    @rx.event
    def set_search_query(self, query: str):
        self.search_query = query
        self.apply_filters()

    @rx.event
    def open_suspension_dialog(self, user: User):
        self.user_to_suspend = user
        self.suspension_reason = "policy_violation"
        self.suspension_notes = ""

    @rx.event
    def close_suspension_dialog(self):
        self.user_to_suspend = None

    @rx.event
    async def suspend_user(self):
        if not self.user_to_suspend:
            return
        user_id = self.user_to_suspend["id"]
        auth_state = await self.get_state(AuthState)
        from app.db_utils import suspend_carrier

        await suspend_carrier(
            user_id=user_id,
            admin_id=auth_state.user_id,
            reason=self.suspension_reason,
            notes=self.suspension_notes,
        )
        await self.load_carriers()
        self.close_suspension_dialog()
        yield rx.toast.success(self.t["user_suspended"])

    @rx.event
    async def unsuspend_user(self, user_id: str):
        auth_state = await self.get_state(AuthState)
        from app.db_utils import unsuspend_carrier

        await unsuspend_carrier(user_id=user_id, admin_id=auth_state.user_id)
        await self.load_carriers()
        yield rx.toast.success(self.t["user_unsuspended"])


class ActivityLogState(State):
    activity_logs: list[ActivityLog] = []
    filtered_logs: list[ActivityLog] = []
    action_filter: str = "all"
    date_filter: dict = {}

    @rx.event
    def load_logs(self):
        self.activity_logs = sorted(
            DB["activity_logs"], key=lambda log: log["timestamp"], reverse=True
        )
        self.apply_filters()

    @rx.event
    def apply_filters(self):
        logs = self.activity_logs
        if self.action_filter != "all":
            logs = [log for log in logs if log["action_type"] == self.action_filter]
        self.filtered_logs = logs

    @rx.event
    def set_action_filter(self, action: str):
        self.action_filter = action
        self.apply_filters()


class ReportingState(State):
    report_timespan: str = "monthly"
    revenue_data: list[dict] = []
    shipment_volume_data: list[dict] = []
    user_growth_data: list[dict] = []
    popular_routes_data: list[dict] = []
    carrier_performance_data: list[dict] = []

    @rx.event
    def set_report_timespan(self, timespan: str):
        self.report_timespan = timespan
        self.load_reports()

    @rx.event
    def load_reports(self):
        self.revenue_data = [
            {"name": "Jan", "revenue": 4000},
            {"name": "Feb", "revenue": 3000},
            {"name": "Mar", "revenue": 5000},
            {"name": "Apr", "revenue": 4500},
            {"name": "May", "revenue": 6000},
            {"name": "Jun", "revenue": 5500},
        ]
        self.shipment_volume_data = [
            {"name": "Delivered", "value": 400},
            {"name": "In Transit", "value": 50},
            {"name": "Pending", "value": 30},
            {"name": "Cancelled", "value": 15},
        ]
        self.user_growth_data = [
            {"name": "Jan", "users": 10},
            {"name": "Feb", "users": 15},
            {"name": "Mar", "users": 25},
            {"name": "Apr", "users": 40},
            {"name": "May", "users": 60},
            {"name": "Jun", "users": 85},
        ]
        self.popular_routes_data = [
            {"route": "San José -> Limón", "count": 150},
            {"route": "San José -> Puntarenas", "count": 120},
            {"route": "Alajuela -> Heredia", "count": 90},
            {"route": "Cartago -> San José", "count": 80},
        ]
        self.carrier_performance_data = [
            {
                "carrier": "Carrier A",
                "completion_rate": 98,
                "average_rating": 4.9,
                "total_earnings": 12500,
            },
            {
                "carrier": "Carrier B",
                "completion_rate": 95,
                "average_rating": 4.7,
                "total_earnings": 9800,
            },
            {
                "carrier": "Carrier C",
                "completion_rate": 99,
                "average_rating": 4.95,
                "total_earnings": 15200,
            },
        ]


class CarrierState(State):
    available_jobs: list[dict] = []
    filtered_jobs: list[dict[str, str | int | float | None]] = []
    cargo_type_filter: str = "all"
    max_weight_filter: int = 50000

    @rx.event
    async def load_available_jobs(self):
        from app.db_utils import get_available_shipments

        auth_state = await self.get_state(AuthState)
        if auth_state.user_role == "carrier":
            self.available_jobs = await get_available_shipments()
            self.apply_filters()

    @rx.event
    def apply_filters(self):
        jobs = self.available_jobs
        if self.cargo_type_filter != "all":
            jobs = [j for j in jobs if j["cargo_type"] == self.cargo_type_filter]
        if self.max_weight_filter < 50000:
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
        from app.db_utils import assign_shipment_to_carrier

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.user_role != "carrier":
            yield rx.toast.error("You are not authorized to accept jobs.")
            return
        try:
            await assign_shipment_to_carrier(shipment_id, auth_state.user_id)
            yield rx.toast.success(self.t["job_accepted_success"])
            yield rx.redirect("/dashboard")
        except ValueError as e:
            import logging

            logging.exception(f"Error: {e}")
            yield rx.toast.error(f"Error: {e}")
        except Exception as e:
            import logging

            logging.exception(f"Failed to accept job: {e}")
            yield rx.toast.error("An unexpected error occurred.")


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
        "shipper_id": "",
        "pickup_address": "",
        "pickup_city": "",
        "pickup_province": "",
        "pickup_postal_code": "",
        "pickup_contact_name": "",
        "pickup_contact_phone": "",
        "delivery_address": "",
        "delivery_city": "",
        "delivery_province": "",
        "delivery_postal_code": "",
        "delivery_contact_name": "",
        "delivery_contact_phone": "",
        "cargo_type": "general",
        "description": "",
        "weight_kg": 0.0,
        "length_m": 0.0,
        "width_m": 0.0,
        "height_m": 0.0,
        "special_instructions": "",
        "pickup_date": "",
        "quoted_amount": 0.0,
    }
    estimated_quote: dict[str, float] = {}

    @rx.event
    async def load_shipper_shipments(self):
        from app.db_utils import get_shipments_by_shipper

        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "shipper":
            self.shipments = await get_shipments_by_shipper(auth_state.user_id)
            self.apply_shipper_filter()

    @rx.event
    async def load_carrier_dashboard_data(self):
        from app.db_utils import get_shipments_by_carrier, get_available_shipments

        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated and auth_state.user_role == "carrier":
            self.carrier_shipments = await get_shipments_by_carrier(auth_state.user_id)
            active_deliveries = len(
                [
                    s
                    for s in self.carrier_shipments
                    if s["status"] in ["ACCEPTED", "IN_TRANSIT", "PICKUP_SCHEDULED"]
                ]
            )
            completed_jobs = len(
                [s for s in self.carrier_shipments if s["status"] == "DELIVERED"]
            )
            total_earnings = sum(
                (
                    s["price"]
                    for s in self.carrier_shipments
                    if s["status"] == "DELIVERED" and s["price"] is not None
                ),
                0.0,
            )
            available_jobs_list = await get_available_shipments()
            self.carrier_dashboard_stats = {
                "available_jobs": len(available_jobs_list),
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
                in ["PENDING", "ACCEPTED", "IN_TRANSIT", "PICKUP_SCHEDULED"]
            ]
        else:
            self.filtered_shipments = [
                s for s in self.shipments if s["status"].lower() == self.shipment_filter
            ]

    def _update_new_shipment(self, field, value):
        self.new_shipment[field] = value

    @rx.event
    def set_pickup_address(self, value: str):
        self._update_new_shipment("pickup_address", value)

    @rx.event
    def set_pickup_city(self, value: str):
        self._update_new_shipment("pickup_city", value)

    @rx.event
    def set_pickup_province(self, value: str):
        self._update_new_shipment("pickup_province", value)

    @rx.event
    def set_pickup_postal_code(self, value: str):
        self._update_new_shipment("pickup_postal_code", value)

    @rx.event
    def set_pickup_contact_name(self, value: str):
        self._update_new_shipment("pickup_contact_name", value)

    @rx.event
    def set_pickup_contact_phone(self, value: str):
        self._update_new_shipment("pickup_contact_phone", value)

    @rx.event
    def set_delivery_address(self, value: str):
        self._update_new_shipment("delivery_address", value)

    @rx.event
    def set_delivery_city(self, value: str):
        self._update_new_shipment("delivery_city", value)

    @rx.event
    def set_delivery_province(self, value: str):
        self._update_new_shipment("delivery_province", value)

    @rx.event
    def set_delivery_postal_code(self, value: str):
        self._update_new_shipment("delivery_postal_code", value)

    @rx.event
    def set_delivery_contact_name(self, value: str):
        self._update_new_shipment("delivery_contact_name", value)

    @rx.event
    def set_delivery_contact_phone(self, value: str):
        self._update_new_shipment("delivery_contact_phone", value)

    @rx.event
    def set_cargo_type(self, value: str):
        self._update_new_shipment("cargo_type", value)

    @rx.event
    def set_weight_kg(self, value: str):
        try:
            self._update_new_shipment("weight_kg", float(value))
        except ValueError as e:
            import logging

            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_length_m(self, value: str):
        try:
            self._update_new_shipment("length_m", float(value))
        except ValueError as e:
            import logging

            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_width_m(self, value: str):
        try:
            self._update_new_shipment("width_m", float(value))
        except ValueError as e:
            import logging

            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_height_m(self, value: str):
        try:
            self._update_new_shipment("height_m", float(value))
        except ValueError as e:
            import logging

            logging.exception(f"Error: {e}")
            pass

    @rx.event
    def set_description(self, value: str):
        self._update_new_shipment("description", value)

    @rx.event
    def set_special_instructions(self, value: str):
        self._update_new_shipment("special_instructions", value)

    @rx.event
    def set_pickup_date(self, value: str):
        self._update_new_shipment("pickup_date", value)

    @rx.event
    def calculate_quote(self):
        from app.db_utils import calculate_shipment_quote

        quote = calculate_shipment_quote(
            weight_kg=self.new_shipment["weight_kg"],
            cargo_type=self.new_shipment["cargo_type"],
        )
        self.estimated_quote = quote
        self.new_shipment["quoted_amount"] = quote["total"]

    @rx.event
    async def post_shipment_for_bidding(self):
        from app.db_utils import create_shipment, get_user_by_id

        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated:
            yield rx.toast.error("Authentication required to post a shipment.")
            return
        user = await get_user_by_id(auth_state.user_id)
        if not user:
            yield rx.toast.error("User not found.")
            return
        if user.status != "ACTIVE":
            yield rx.toast.error(
                f"Account is not active ({user.status}). Cannot create shipments."
            )
            return
        self.new_shipment["shipper_id"] = auth_state.user_id
        try:
            shipment_id = await create_shipment(self.new_shipment)
            yield rx.toast.success(self.t["shipment_posted_success"])
            yield rx.redirect("/dashboard")
        except Exception as e:
            import logging

            logging.exception(f"Error creating shipment: {e}")
            yield rx.toast.error(f"Failed to create shipment: {e}")


class TrackingState(State):
    shipment: Shipment | None = None
    is_tracking_active: bool = False
    eta: str = ""

    async def _reload_shipment_data(self, shipment_id: str) -> bool:
        from app.db_utils import get_shipment_by_id, get_tracking_events

        shipment_data = await get_shipment_by_id(shipment_id)
        if not shipment_data:
            return False
        events_data = await get_tracking_events(shipment_id)
        timeline = [
            StatusEvent(status=e["event_type"], timestamp=e["event_timestamp"])
            for e in events_data
        ]
        self.shipment = Shipment(
            id=shipment_data["id"],
            shipper_id=shipment_data["shipper_id"],
            carrier_id=shipment_data.get("carrier_id"),
            pickup_location=Location(
                address=shipment_data["pickup_address"],
                city=shipment_data["pickup_city"],
                province=shipment_data["pickup_province"],
                postal_code="",
                lat=9.9333,
                lng=-84.0833,
            ),
            delivery_location=Location(
                address=shipment_data["delivery_address"],
                city=shipment_data["delivery_city"],
                province=shipment_data["delivery_province"],
                postal_code="",
                lat=9.9936,
                lng=-84.6333,
            ),
            cargo_type=shipment_data["cargo_type"],
            weight_kg=shipment_data["weight_kg"],
            length_m=shipment_data.get("length_m", 0),
            width_m=shipment_data.get("width_m", 0),
            height_m=shipment_data.get("height_m", 0),
            special_instructions=shipment_data.get("special_instructions", ""),
            pickup_datetime=str(shipment_data["pickup_datetime"]),
            status=shipment_data["status"],
            price=shipment_data["price"],
            created_at=str(shipment_data["createdAt"]),
            timeline=timeline,
            current_lat=shipment_data.get("latitude"),
            current_lng=shipment_data.get("longitude"),
            route_polyline=None,
        )
        self.is_tracking_active = self.shipment["status"] in [
            "PICKUP_SCHEDULED",
            "IN_TRANSIT",
        ]
        self.calculate_eta()
        return True

    @rx.event
    async def load_shipment_for_tracking(self):
        shipment_id = self.router.page.params.get("id")
        if not shipment_id:
            yield rx.redirect("/dashboard")
            return
        success = await self._reload_shipment_data(shipment_id)
        if not success:
            yield rx.redirect("/dashboard")
            return
        if self.is_tracking_active:
            yield TrackingState.simulate_gps_updates

    @rx.event(background=True)
    async def simulate_gps_updates(self):
        from app.db_utils import update_shipment_location

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
                current_lat = self.shipment.get("current_lat")
                current_lng = self.shipment.get("current_lng")
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
                new_lat = current_lat + lat_diff / distance_to_target * step
                new_lng = current_lng + lng_diff / distance_to_target * step
                self.shipment["current_lat"] = new_lat
                self.shipment["current_lng"] = new_lng
                await update_shipment_location(
                    shipment_id=self.shipment["id"],
                    latitude=new_lat,
                    longitude=new_lng,
                    address="En route",
                )
                self.calculate_eta()
            await asyncio.sleep(5)

    @rx.event
    async def add_status_event(self, shipment_id: str, status: str):
        from app.db_utils import create_tracking_event

        await create_tracking_event(shipment_id, status, f"Status updated to {status}")

    @rx.event
    async def change_shipment_status(self, new_status: str):
        from app.db_utils import update_shipment_status

        if not self.shipment:
            return
        auth_state = await self.get_state(AuthState)
        shipment_id = self.shipment["id"]
        await update_shipment_status(
            shipment_id=shipment_id, new_status=new_status, user_id=auth_state.user_id
        )
        success = await self._reload_shipment_data(shipment_id)
        if not success:
            yield rx.redirect("/dashboard")
            return
        yield rx.toast.success(
            f"Status updated to {self.t.get(new_status, new_status)}"
        )
        if new_status == "DELIVERED":
            invoice_state = await self.get_state(InvoiceState)
            await invoice_state.create_invoice(shipment_id)

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


class PaymentState(State):
    sinpe_number: str = ""
    iban_number: str = ""

    @rx.event
    def add_sinpe_number(self):
        if len(self.sinpe_number) == 8 and self.sinpe_number.isdigit():
            yield rx.toast.success("SINPE Móvil number added.")
            self.sinpe_number = ""
        else:
            yield rx.toast.error("Invalid SINPE Móvil number. Must be 8 digits.")

    @rx.event
    def add_iban_number(self):
        if len(self.iban_number) > 10:
            yield rx.toast.success("IBAN added.")
            self.iban_number = ""
        else:
            yield rx.toast.error("Invalid IBAN.")


class InvoiceState(State):
    invoices: list[Invoice] = []

    @rx.event
    async def load_invoices(self):
        auth_state = await self.get_state(AuthState)
        if auth_state.is_authenticated:
            self.invoices = [
                i for i in DB["invoices"] if i["shipper_id"] == auth_state.user_id
            ]

    @rx.event
    async def create_invoice(self, shipment_id: str):
        shipment = next((s for s in DB["shipments"] if s["id"] == shipment_id), None)
        if not shipment or shipment["price"] is None:
            return
        invoice_count = len(DB["invoices"]) + 1
        new_invoice = Invoice(
            id="".join(random.choices(string.ascii_lowercase + string.digits, k=10)),
            invoice_number=f"INV-{invoice_count:05d}",
            shipment_id=shipment_id,
            shipper_id=shipment["shipper_id"],
            issue_date=datetime.date.today().isoformat(),
            due_date=(datetime.date.today() + datetime.timedelta(days=30)).isoformat(),
            subtotal=shipment["price"],
            tax=shipment["price"] * 0.13,
            total=shipment["price"] * 1.13,
            status="issued",
        )
        DB["invoices"].append(new_invoice)
        self.load_invoices()


class CarrierEarningsState(State):
    total_earnings: float = 0.0
    platform_commission: float = 0.0
    net_earnings: float = 0.0
    available_for_payout: float = 0.0
    payout_history: list[Payout] = []

    @rx.event
    async def load_earnings_data(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or auth_state.user_role != "carrier":
            return
        completed_shipments = [
            s
            for s in DB["shipments"]
            if s["carrier_id"] == auth_state.user_id and s["status"] == "delivered"
        ]
        self.total_earnings = sum(
            (s["price"] for s in completed_shipments if s["price"] is not None)
        )
        self.platform_commission = self.total_earnings * 0.1
        self.net_earnings = self.total_earnings - self.platform_commission
        user_payouts = [
            p for p in DB["payouts"] if p["carrier_id"] == auth_state.user_id
        ]
        total_paid_out = sum((p["net_amount"] for p in user_payouts))
        self.available_for_payout = self.net_earnings - total_paid_out
        self.payout_history = sorted(
            user_payouts, key=lambda p: p["created_at"], reverse=True
        )

    @rx.event
    async def request_payout(self):
        auth_state = await self.get_state(AuthState)
        if not auth_state.is_authenticated or self.available_for_payout <= 0:
            yield rx.toast.error("No funds available for payout.")
            return
        payout_id = "".join(
            random.choices(string.ascii_lowercase + string.digits, k=10)
        )
        new_payout = Payout(
            id=payout_id,
            carrier_id=auth_state.user_id,
            shipment_ids=[],
            amount=self.available_for_payout / 0.9,
            commission=self.available_for_payout * 0.1 / 0.9,
            net_amount=self.available_for_payout,
            status="pending",
            payment_method="sinpe_mobile",
            scheduled_date=(
                datetime.date.today() + datetime.timedelta(days=7)
            ).isoformat(),
            processed_date=None,
            created_at=datetime.datetime.now().isoformat(),
        )
        DB["payouts"].append(new_payout)
        yield rx.toast.success("Payout requested successfully.")
        self.load_earnings_data()