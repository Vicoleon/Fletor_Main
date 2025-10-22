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
from app.pages.payments import payments_page
from app.pages.invoices import invoices_page
from app.pages.carrier_earnings import carrier_earnings_page


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon, class_name="h-8 w-8 text-white"),
            class_name="flex items-center justify-center h-16 w-16 rounded-full bg-indigo-600",
        ),
        rx.el.h3(title, class_name="mt-6 text-xl font-bold text-gray-900"),
        rx.el.p(description, class_name="mt-2 text-base text-gray-600"),
        class_name="p-6 bg-white rounded-xl shadow-sm border border-gray-200",
    )


def how_it_works_step(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon, class_name="h-8 w-8 text-indigo-600"),
            class_name="flex items-center justify-center h-16 w-16 rounded-full bg-indigo-100 mb-4",
        ),
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-900"),
        rx.el.p(description, class_name="mt-1 text-gray-500"),
        class_name="flex flex-col items-center text-center",
    )


def stat_item(value: str, label: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(value, class_name="text-4xl font-extrabold text-indigo-600"),
        rx.el.p(label, class_name="mt-1 text-lg font-medium text-gray-500"),
        class_name="text-center",
    )


def trust_badge(icon: str, text: str) -> rx.Component:
    return rx.el.div(
        rx.icon(tag=icon, class_name="h-6 w-6 text-green-500"),
        rx.el.span(text, class_name="ml-2 text-gray-700 font-medium"),
        class_name="flex items-center p-3 bg-green-50 rounded-lg",
    )


def index() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "The Future of Freight in Costa Rica",
                            class_name="text-4xl md:text-6xl font-extrabold text-gray-900 tracking-tight text-center lg:text-left",
                        ),
                        rx.el.p(
                            "Connecting Shippers and Carriers with unparalleled efficiency, transparency, and security. Fletor is your all-in-one logistics platform.",
                            class_name="mt-4 max-w-2xl text-lg md:text-xl text-gray-600 mx-auto lg:mx-0 text-center lg:text-left",
                        ),
                        rx.el.div(
                            rx.el.a(
                                "I need to ship cargo",
                                href="/register",
                                class_name="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700",
                            ),
                            rx.el.a(
                                "I am a carrier",
                                href="/register",
                                class_name="ml-4 inline-flex items-center justify-center px-6 py-3 border border-indigo-600 text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50",
                            ),
                            class_name="mt-8 flex flex-wrap gap-4 justify-center lg:justify-start",
                        ),
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32",
                ),
                class_name="bg-gray-50",
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "A smarter way to manage logistics",
                            class_name="text-3xl font-bold tracking-tight text-gray-900 text-center",
                        ),
                        rx.el.p(
                            "Everything you need, from instant quotes to final delivery, in one powerful platform.",
                            class_name="mt-4 text-lg text-gray-600 text-center max-w-3xl mx-auto",
                        ),
                    ),
                    rx.el.div(
                        feature_card(
                            "zap",
                            "Instant Quotes",
                            "Get real-time price estimates for your shipments based on weight, cargo type, and distance.",
                        ),
                        feature_card(
                            "map",
                            "Live GPS Tracking",
                            "Monitor your cargo's journey from pickup to delivery with our real-time map interface.",
                        ),
                        feature_card(
                            "shield",
                            "Verified Carriers",
                            "Rest easy knowing all carriers are vetted for compliance, insurance, and reliability.",
                        ),
                        feature_card(
                            "message-circle",
                            "In-App Messaging",
                            "Communicate directly with your carrier or shipper without leaving the platform.",
                        ),
                        feature_card(
                            "file-text",
                            "Digital Invoicing",
                            "Receive Hacienda-compliant electronic invoices automatically upon delivery.",
                        ),
                        feature_card(
                            "dollar-sign",
                            "Secure Payments",
                            "Manage payments and payouts through secure, local methods like SINPE and bank transfers.",
                        ),
                        class_name="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-20",
                )
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.h2(
                        "Get started in minutes",
                        class_name="text-3xl font-bold text-center text-gray-900 tracking-tight",
                    ),
                    rx.el.div(
                        how_it_works_step(
                            "user-plus",
                            "1. Register & Verify",
                            "Sign up as a shipper or carrier and complete our simple verification process.",
                        ),
                        how_it_works_step(
                            "package-search",
                            "2. Post or Find a Job",
                            "Shippers post their cargo needs, and carriers find the perfect job from our live board.",
                        ),
                        how_it_works_step(
                            "truck",
                            "3. Track & Communicate",
                            "Follow your shipment in real-time and stay in touch throughout the journey.",
                        ),
                        how_it_works_step(
                            "check-check",
                            "4. Deliver & Get Paid",
                            "Complete the delivery, get digital proof, and receive prompt, secure payment.",
                        ),
                        class_name="mt-12 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-20",
                ),
                class_name="bg-gray-50",
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        stat_item("1,500+", "Verified Carriers"),
                        stat_item("20,000+", "Shipments Completed"),
                        stat_item("99.8%", "On-Time Delivery"),
                        stat_item("24/7", "Support Available"),
                        class_name="grid grid-cols-2 md:grid-cols-4 gap-8",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-20",
                )
            ),
            rx.el.section(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            "Your Cargo, Our Commitment",
                            class_name="text-3xl font-bold tracking-tight text-gray-900",
                        ),
                        rx.el.p(
                            "We prioritize security and compliance at every step, ensuring your peace of mind.",
                            class_name="mt-4 text-lg text-gray-600",
                        ),
                        rx.el.div(
                            trust_badge("shield-check", "Full Legal Compliance"),
                            trust_badge("lock-keyhole", "Secure Data Encryption"),
                            trust_badge("life-buoy", "Dedicated Support Team"),
                            class_name="mt-8 flex flex-col sm:flex-row gap-4",
                        ),
                    ),
                    rx.el.div(
                        rx.el.image(
                            src="/placeholder.svg",
                            class_name="rounded-lg shadow-lg aspect-video object-cover",
                        ),
                        class_name="mt-10 lg:mt-0",
                    ),
                    class_name="container mx-auto px-4 sm:px-6 lg:px-8 py-20 grid lg:grid-cols-2 items-center gap-12",
                ),
                class_name="bg-gray-50",
            ),
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
app.add_page(payments_page, route="/payments")
app.add_page(invoices_page, route="/invoices")
app.add_page(carrier_earnings_page, route="/carrier-earnings")