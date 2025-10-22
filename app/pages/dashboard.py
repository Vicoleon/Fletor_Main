import reflex as rx
from app.states.state import State, AuthState, ShipmentState
from app.components.navbar import navbar
from app.components.stats import stat_card


def shipment_status_badge(status: str) -> rx.Component:
    color_map = {
        "pending_assignment": "bg-yellow-100 text-yellow-800",
        "assigned": "bg-blue-100 text-blue-800",
        "picked_up": "bg-cyan-100 text-cyan-800",
        "in_transit": "bg-indigo-100 text-indigo-800",
        "delivered": "bg-green-100 text-green-800",
        "cancelled": "bg-red-100 text-red-800",
        "delayed": "bg-orange-100 text-orange-800",
    }
    return rx.el.span(
        State.t[status],
        class_name=f"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {color_map.get(status, 'bg-gray-100 text-gray-800')}",
    )


def shipper_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card(State.t["active_shipments"], "package", "12", "text-blue-500"),
            stat_card(State.t["pending_quotes"], "clock", "3", "text-yellow-500"),
            stat_card(
                State.t["completed_deliveries"], "check-circle", "128", "text-green-500"
            ),
            stat_card(
                State.t["total_spent"], "dollar-sign", "$24,500", "text-purple-500"
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    State.t["shipments"], class_name="text-xl font-bold text-gray-900"
                ),
                rx.el.a(
                    State.t["create_shipment"],
                    href="/create-shipment",
                    class_name="ml-auto inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                ),
                class_name="flex items-center mt-8",
            ),
            rx.el.div(
                rx.el.button(
                    State.t["all"],
                    on_click=lambda: ShipmentState.set_shipment_filter("all"),
                ),
                rx.el.button(
                    State.t["active"],
                    on_click=lambda: ShipmentState.set_shipment_filter("active"),
                ),
                rx.el.button(
                    State.t["pending"],
                    on_click=lambda: ShipmentState.set_shipment_filter(
                        "pending_assignment"
                    ),
                ),
                rx.el.button(
                    State.t["completed"],
                    on_click=lambda: ShipmentState.set_shipment_filter("delivered"),
                ),
                class_name="flex gap-2 mt-4",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("ID"),
                            rx.el.th(State.t["pickup_location"]),
                            rx.el.th(State.t["delivery_location"]),
                            rx.el.th(State.t["status"]),
                            rx.el.th(State.t["carrier"]),
                            rx.el.th(State.t["price"]),
                            rx.el.th(State.t["actions"]),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ShipmentState.filtered_shipments,
                            lambda shipment: rx.el.tr(
                                rx.el.td(shipment["id"].to_string()[:6]),
                                rx.el.td(shipment["pickup_location"]["city"]),
                                rx.el.td(shipment["delivery_location"]["city"]),
                                rx.el.td(shipment_status_badge(shipment["status"])),
                                rx.el.td(shipment["carrier_id"].to_string() | "N/A"),
                                rx.el.td(f"${shipment['price']:.2f}"),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.a(
                                            State.t["view"],
                                            href=f"/shipment/{shipment['id']}",
                                            class_name="text-indigo-600 hover:text-indigo-900",
                                        ),
                                        rx.el.a(
                                            State.t["track_shipment"],
                                            href=f"/tracking/{shipment['id']}",
                                            class_name="ml-4 text-green-600 hover:text-green-900",
                                        ),
                                        class_name="flex",
                                    )
                                ),
                            ),
                        )
                    ),
                    class_name="min-w-full divide-y divide-gray-200 mt-4",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
        ),
    )


def carrier_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_card(
                State.t["available_jobs"],
                "search",
                ShipmentState.carrier_dashboard_stats["available_jobs"].to_string(),
                "text-blue-500",
            ),
            stat_card(
                State.t["active_deliveries"],
                "truck",
                ShipmentState.carrier_dashboard_stats["active_deliveries"].to_string(),
                "text-yellow-500",
            ),
            stat_card(
                State.t["completed_deliveries"],
                "check-circle",
                ShipmentState.carrier_dashboard_stats["completed_jobs"].to_string(),
                "text-green-500",
            ),
            stat_card(
                State.t["earnings"],
                "dollar-sign",
                f"${ShipmentState.carrier_dashboard_stats['total_earnings']:.2f}",
                "text-purple-500",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        rx.el.div(
            rx.el.h2(
                State.t["active_deliveries"],
                class_name="text-xl font-bold text-gray-900 mt-8",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("ID"),
                            rx.el.th(State.t["pickup_location"]),
                            rx.el.th(State.t["delivery_location"]),
                            rx.el.th(State.t["status"]),
                            rx.el.th(State.t["price"]),
                            rx.el.th(State.t["actions"]),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ShipmentState.carrier_shipments,
                            lambda shipment: rx.el.tr(
                                rx.el.td(shipment["id"].to_string()[:6]),
                                rx.el.td(shipment["pickup_location"]["city"]),
                                rx.el.td(shipment["delivery_location"]["city"]),
                                rx.el.td(shipment_status_badge(shipment["status"])),
                                rx.el.td(f"${shipment['price']:.2f}"),
                                rx.el.td(
                                    rx.el.div(
                                        rx.el.a(
                                            State.t["view"],
                                            href=f"/shipment/{shipment['id']}",
                                            class_name="text-indigo-600 hover:text-indigo-900",
                                        ),
                                        rx.el.a(
                                            State.t["track_shipment"],
                                            href=f"/tracking/{shipment['id']}",
                                            class_name="ml-4 text-green-600 hover:text-green-900",
                                        ),
                                        class_name="flex",
                                    )
                                ),
                            ),
                        )
                    ),
                    class_name="min-w-full divide-y divide-gray-200 mt-4",
                ),
                class_name="overflow-x-auto",
            ),
            class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mt-6",
        ),
        on_mount=[ShipmentState.load_carrier_dashboard_data],
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["dashboard"], class_name="text-3xl font-bold text-gray-900"
                ),
                rx.cond(
                    ~AuthState.is_authenticated,
                    rx.el.p("Please log in to view the dashboard."),
                    rx.el.div(
                        rx.match(
                            AuthState.user_role,
                            ("shipper", shipper_dashboard()),
                            ("carrier", carrier_dashboard()),
                            (
                                "admin",
                                rx.el.a(
                                    "Go to Admin Panel",
                                    href="/admin",
                                    class_name="text-indigo-600 hover:underline",
                                ),
                            ),
                            rx.el.p("No dashboard available for your role."),
                        ),
                        class_name="mt-6",
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=[
                ShipmentState.load_shipper_shipments,
                ShipmentState.load_carrier_dashboard_data,
            ],
        ),
        class_name="bg-gray-50 min-h-screen",
    )