import reflex as rx
from app.states.state import State, AuthState, CarrierState
from app.components.navbar import navbar


def job_card(shipment: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-5 w-5 text-gray-400"),
                rx.el.p(f"{shipment['pickup_city']} -> {shipment['delivery_city']}"),
                class_name="flex items-center gap-2 text-sm text-gray-600 font-medium",
            ),
            rx.el.span(
                State.t[shipment["cargo_type"].to(str)],
                class_name="px-2 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.h3(
                f"{State.t['shipment_details']}",
                class_name="text-lg font-bold text-gray-900",
            ),
            class_name="mt-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(f"{State.t['weight_kg']}: {shipment['weight_kg']} kg"),
                class_name="text-sm",
            ),
            rx.el.div(
                rx.el.p(
                    f"{State.t['dimensions_m']}: {shipment['length_cm']}x{shipment['width_cm']}x{shipment['height_cm']}"
                ),
                class_name="text-sm",
            ),
            rx.el.div(
                rx.el.p(f"{State.t['pickup_datetime']}: {shipment['pickup_datetime']}"),
                class_name="text-sm",
            ),
            class_name="mt-2 space-y-1 text-gray-700",
        ),
        rx.el.div(
            rx.el.p(
                f"${shipment['price']:.2f}",
                class_name="text-2xl font-bold text-indigo-600",
            ),
            rx.el.a(
                State.t["view"],
                href=f"/shipment/{shipment['id']}",
                class_name="inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
            ),
            class_name="mt-6 flex justify-between items-center",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm w-full",
    )


def jobs_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        State.t["available_jobs"],
                        class_name="text-3xl font-bold text-gray-900",
                    ),
                    rx.el.p(
                        f"{CarrierState.filtered_jobs.length()} {State.t['available_jobs']}",
                        class_name="text-gray-600 mt-1",
                    ),
                ),
                rx.cond(
                    AuthState.is_authenticated & (AuthState.user_role == "carrier"),
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    State.t["cargo_type"],
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.select(
                                    rx.el.option(State.t["all"], value="all"),
                                    rx.el.option(State.t["general"], value="general"),
                                    rx.el.option(
                                        State.t["refrigerated"], value="refrigerated"
                                    ),
                                    rx.el.option(
                                        State.t["hazardous"], value="hazardous"
                                    ),
                                    rx.el.option(
                                        State.t["oversized"], value="oversized"
                                    ),
                                    on_change=CarrierState.set_cargo_type_filter,
                                    value=CarrierState.cargo_type_filter,
                                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label(
                                    f"{State.t['weight_kg']} (Max: {CarrierState.max_weight_filter} kg)",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.input(
                                    type="range",
                                    key=f"max-weight-filter-{CarrierState.max_weight_filter}",
                                    default_value=CarrierState.max_weight_filter.to_string(),
                                    min=0,
                                    max=50000,
                                    step=1000,
                                    on_change=CarrierState.set_max_weight_filter.throttle(
                                        100
                                    ),
                                    class_name="w-full mt-2",
                                ),
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 gap-6 p-6 bg-white rounded-xl border border-gray-200 shadow-sm",
                        ),
                        rx.cond(
                            CarrierState.filtered_jobs.length() > 0,
                            rx.el.div(
                                rx.foreach(CarrierState.filtered_jobs, job_card),
                                class_name="mt-6 grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    State.t["no_jobs_available"],
                                    class_name="text-center text-gray-500 py-12",
                                ),
                                class_name="mt-6 bg-white p-6 rounded-xl border border-gray-200 shadow-sm w-full",
                            ),
                        ),
                        class_name="mt-6",
                    ),
                    rx.el.p(
                        f"{State.t['access_denied']} {State.t['carriers_only']}",
                        class_name="mt-6",
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=CarrierState.load_available_jobs,
        ),
        class_name="bg-gray-50 min-h-screen",
    )