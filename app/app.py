import reflex as rx
from app.states.state import State
from app.components.navbar import navbar
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.profile import profile_page
from app.pages.admin import admin_page
from app.pages.dashboard import dashboard_page
from app.pages.create_shipment import create_shipment_page
from app.pages.shipment_detail import shipment_detail_page
from app.pages.jobs import jobs_page
from app.pages.tracking import tracking_page
from app.pages.messages import messages_page
from app.pages.disputes import disputes_page
from app.pages.support_tickets import support_tickets_page
from app.pages.financial import financial_page
from app.pages.compliance import compliance_page
from app.pages.activity_logs import activity_logs_page
from app.pages.reports import reports_page


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        State.t["hero_title"],
                        class_name="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl",
                    ),
                    rx.el.p(
                        State.t["hero_subtitle"],
                        class_name="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.a(
                                State.t["get_started_shipper"],
                                href="/register",
                                class_name="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10",
                            )
                        ),
                        rx.el.div(
                            rx.el.a(
                                State.t["get_started_carrier"],
                                href="/register",
                                class_name="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 md:py-4 md:text-lg md:px-10",
                            ),
                            class_name="mt-3 sm:mt-0 sm:ml-3",
                        ),
                        class_name="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8",
                    ),
                    class_name="text-center",
                ),
                class_name="relative px-4 py-16 sm:px-6 sm:py-24 lg:py-32 lg:px-8",
            )
        ),
        class_name="font-['Inter'] bg-white",
    )


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(
            src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places"
        ),
    ],
)
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(profile_page, route="/profile")
app.add_page(admin_page, route="/admin")
app.add_page(dashboard_page, route="/dashboard")
app.add_page(create_shipment_page, route="/create-shipment")
app.add_page(shipment_detail_page, route="/shipment/[id]")
app.add_page(jobs_page, route="/jobs")
app.add_page(tracking_page, route="/tracking/[id]")
app.add_page(messages_page, route="/messages/[id]")
app.add_page(disputes_page, route="/disputes")
app.add_page(support_tickets_page, route="/support-tickets")
app.add_page(financial_page, route="/financial")
app.add_page(compliance_page, route="/compliance")
app.add_page(activity_logs_page, route="/activity-logs")
app.add_page(reports_page, route="/reports")