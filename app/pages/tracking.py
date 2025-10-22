import reflex as rx
from app.states.state import State, AuthState, TrackingState, Shipment
from app.components.navbar import navbar


def map_component(shipment: Shipment) -> rx.Component:
    return rx.el.div(
        id="gmap_canvas", class_name="h-[400px] w-full bg-gray-200 rounded-lg"
    )


def timeline_event(event: dict, is_last: bool) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                class_name="w-4 h-4 bg-indigo-600 rounded-full mt-1.5 -left-2 border-4 border-white"
            ),
            rx.cond(~is_last, rx.el.div(class_name="w-px h-full bg-gray-300"), None),
            class_name="absolute flex items-center justify-center",
        ),
        rx.el.div(
            rx.el.p(State.t[event["status"]], class_name="font-semibold text-gray-900"),
            rx.el.time(
                event["timestamp"].to_string(), class_name="text-sm text-gray-500"
            ),
            class_name="ml-6",
        ),
        class_name="relative flex",
    )


def tracking_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["live_tracking"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    TrackingState.shipment,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                map_component(TrackingState.shipment),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.p(
                                            State.t["status"],
                                            class_name="text-sm font-medium text-gray-500",
                                        ),
                                        rx.el.p(
                                            State.t[TrackingState.shipment["status"]],
                                            class_name="text-lg font-semibold text-indigo-600",
                                        ),
                                    ),
                                    rx.el.div(
                                        rx.el.p(
                                            State.t["eta"],
                                            class_name="text-sm font-medium text-gray-500",
                                        ),
                                        rx.el.p(
                                            TrackingState.eta,
                                            class_name="text-lg font-semibold text-gray-900",
                                        ),
                                    ),
                                    class_name="mt-4 grid grid-cols-2 gap-4",
                                ),
                                class_name="p-6 bg-white rounded-lg shadow-md border",
                            ),
                            rx.el.div(
                                rx.el.h2(
                                    State.t["shipment_timeline"],
                                    class_name="text-xl font-bold text-gray-900 mb-4",
                                ),
                                rx.foreach(
                                    TrackingState.shipment["timeline"],
                                    lambda event, index: timeline_event(
                                        event,
                                        index
                                        == TrackingState.shipment["timeline"].length()
                                        - 1,
                                    ),
                                ),
                                class_name="p-6 bg-white rounded-lg shadow-md border",
                            ),
                            class_name="grid md:grid-cols-2 gap-6 mt-6",
                        ),
                        rx.cond(
                            AuthState.user_role == "carrier",
                            rx.el.div(
                                rx.el.h3(
                                    "Carrier Actions",
                                    class_name="text-xl font-bold text-gray-900 mb-4",
                                ),
                                rx.el.div(
                                    rx.el.button(
                                        State.t["mark_as_picked_up"],
                                        on_click=lambda: TrackingState.change_shipment_status(
                                            "picked_up"
                                        ),
                                        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700",
                                    ),
                                    rx.el.button(
                                        State.t["mark_as_in_transit"],
                                        on_click=lambda: TrackingState.change_shipment_status(
                                            "in_transit"
                                        ),
                                        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                                    ),
                                    rx.el.button(
                                        State.t["mark_as_delivered"],
                                        on_click=lambda: TrackingState.change_shipment_status(
                                            "delivered"
                                        ),
                                        class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700",
                                    ),
                                    class_name="grid grid-cols-1 md:grid-cols-3 gap-4",
                                ),
                                class_name="p-6 bg-white rounded-lg shadow-md border mt-6",
                            ),
                            None,
                        ),
                    ),
                    rx.el.p("Loading shipment tracking..."),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=TrackingState.load_shipment_for_tracking,
        ),
        class_name="bg-gray-50 min-h-screen",
    )