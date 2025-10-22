import reflex as rx
from app.states.state import State, ShipmentState, AuthState
from app.components.navbar import navbar


def form_input(
    label: rx.Var[str], placeholder: rx.Var[str], type: str, state_setter, value=None
) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700"),
        rx.el.input(
            type=type,
            placeholder=placeholder,
            on_change=state_setter,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
            default_value=value,
        ),
    )


def location_form(title: rx.Var[str], state_prefix: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-medium leading-6 text-gray-900"),
        rx.el.div(
            form_input(
                State.t["address"],
                "123 Main St",
                "text",
                getattr(ShipmentState, f"set_{state_prefix}_address"),
            ),
            form_input(
                State.t["city"],
                "San José",
                "text",
                getattr(ShipmentState, f"set_{state_prefix}_city"),
            ),
            form_input(
                State.t["province"],
                "San José",
                "text",
                getattr(ShipmentState, f"set_{state_prefix}_province"),
            ),
            form_input(
                State.t["postal_code"],
                "10101",
                "text",
                getattr(ShipmentState, f"set_{state_prefix}_postal_code"),
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4",
        ),
    )


def cargo_details_form() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            State.t["cargo_details"],
            class_name="text-lg font-medium leading-6 text-gray-900",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    State.t["cargo_type"],
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.select(
                    rx.el.option(State.t["general"], value="general"),
                    rx.el.option(State.t["refrigerated"], value="refrigerated"),
                    rx.el.option(State.t["hazardous"], value="hazardous"),
                    rx.el.option(State.t["oversized"], value="oversized"),
                    on_change=ShipmentState.set_cargo_type,
                    value=ShipmentState.new_shipment["cargo_type"],
                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                ),
            ),
            form_input(
                State.t["weight_kg"], "500", "number", ShipmentState.set_weight_kg
            ),
            rx.el.div(
                rx.el.label(
                    State.t["dimensions_m"],
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.div(
                    form_input(
                        State.t["length"], "2.5", "number", ShipmentState.set_length_m
                    ),
                    form_input(
                        State.t["width"], "2.5", "number", ShipmentState.set_width_m
                    ),
                    form_input(
                        State.t["height"], "2.5", "number", ShipmentState.set_height_m
                    ),
                    class_name="grid grid-cols-3 gap-2 mt-1",
                ),
            ),
            form_input(
                State.t["pickup_datetime"],
                "",
                "datetime-local",
                ShipmentState.set_pickup_datetime,
            ),
            rx.el.div(
                rx.el.label(
                    State.t["special_instructions"],
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.textarea(
                    placeholder="e.g. Fragile items, requires careful handling.",
                    on_change=ShipmentState.set_special_instructions,
                    class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
                ),
                class_name="col-span-1 md:col-span-2",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4",
        ),
    )


def quote_display() -> rx.Component:
    return rx.cond(
        ShipmentState.estimated_quote.keys().length() > 0,
        rx.el.div(
            rx.el.h3(
                State.t["estimated_quote"],
                class_name="text-lg font-medium leading-6 text-gray-900",
            ),
            rx.el.div(
                rx.el.p(
                    f"{State.t['base_rate']}: ${ShipmentState.estimated_quote['base_rate']:.2f}"
                ),
                rx.el.p(
                    f"{State.t['weight_surcharge']}: ${ShipmentState.estimated_quote['weight_surcharge']:.2f}"
                ),
                rx.el.p(
                    f"{State.t['cargo_surcharge']}: ${ShipmentState.estimated_quote['cargo_surcharge']:.2f}"
                ),
                rx.el.hr(class_name="my-2"),
                rx.el.p(
                    f"{State.t['total_estimated_price']}: ${ShipmentState.estimated_quote['total']:.2f}",
                    class_name="font-bold",
                ),
                class_name="p-4 bg-indigo-50 rounded-lg mt-4",
            ),
            rx.el.div(
                rx.el.button(
                    State.t["post_for_bidding"],
                    on_click=ShipmentState.post_shipment_for_bidding,
                    class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                ),
                class_name="mt-4",
            ),
            class_name="mt-6",
        ),
    )


def create_shipment_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["new_shipment"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    ~AuthState.is_authenticated,
                    rx.el.p("Please log in to create a shipment."),
                    rx.el.div(
                        rx.el.div(
                            location_form(State.t["pickup_location"], "pickup"),
                            class_name="p-6 bg-white rounded-lg shadow-md border",
                        ),
                        rx.el.div(
                            location_form(State.t["delivery_location"], "delivery"),
                            class_name="p-6 bg-white rounded-lg shadow-md border mt-6",
                        ),
                        rx.el.div(
                            cargo_details_form(),
                            class_name="p-6 bg-white rounded-lg shadow-md border mt-6",
                        ),
                        rx.el.button(
                            State.t["calculate_quote"],
                            on_click=ShipmentState.calculate_quote,
                            class_name="mt-6 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                        ),
                        quote_display(),
                        class_name="mt-6",
                    ),
                ),
                class_name="max-w-4xl mx-auto py-10 px-4",
            )
        ),
        class_name="bg-gray-50 min-h-screen",
    )