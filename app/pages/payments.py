import reflex as rx
from app.states.state import State, AuthState, PaymentState
from app.components.navbar import navbar


def payments_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["payments"], class_name="text-3xl font-bold text-gray-900"
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                State.t["payment_methods"],
                                class_name="text-xl font-semibold",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    State.t["sinpe_mobile"],
                                    class_name="text-lg font-medium",
                                ),
                                rx.el.input(
                                    placeholder=State.t["phone_number_8_digits"],
                                    on_change=PaymentState.set_sinpe_number,
                                    class_name="mt-2 w-full p-2 border rounded-md",
                                ),
                                rx.el.button(
                                    State.t["add_sinpe"],
                                    on_click=PaymentState.add_sinpe_number,
                                    class_name="mt-2 w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700",
                                ),
                                class_name="p-6 bg-white rounded-lg shadow-md border",
                            ),
                            rx.el.div(
                                rx.el.h3(
                                    State.t["bank_transfer"],
                                    class_name="text-lg font-medium",
                                ),
                                rx.el.input(
                                    placeholder=State.t["iban_account"],
                                    on_change=PaymentState.set_iban_number,
                                    class_name="mt-2 w-full p-2 border rounded-md",
                                ),
                                rx.el.button(
                                    State.t["add_bank_account"],
                                    on_click=PaymentState.add_iban_number,
                                    class_name="mt-2 w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700",
                                ),
                                class_name="p-6 bg-white rounded-lg shadow-md border",
                            ),
                            class_name="grid md:grid-cols-2 gap-6 mt-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                State.t["payment_history"],
                                class_name="text-xl font-semibold mt-10",
                            ),
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th(State.t["transaction_id"]),
                                            rx.el.th(State.t["amount"]),
                                            rx.el.th(State.t["date"]),
                                            rx.el.th(State.t["method"]),
                                            rx.el.th(State.t["status"]),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.el.tr(
                                            rx.el.td(
                                                State.t["no_invoices"],
                                                col_span=5,
                                                class_name="text-center py-10 text-gray-500",
                                            )
                                        )
                                    ),
                                    class_name="min-w-full divide-y divide-gray-200 mt-4",
                                ),
                                class_name="overflow-x-auto bg-white p-6 rounded-xl border shadow-sm mt-6",
                            ),
                        ),
                    ),
                    rx.el.p("Please log in to manage payments.", class_name="mt-4"),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            )
        ),
        class_name="bg-gray-50 min-h-screen",
    )