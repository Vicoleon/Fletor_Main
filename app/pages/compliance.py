import reflex as rx
from app.states.state import State, AuthState, ComplianceState
from app.components.navbar import navbar


def compliance_status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        State.t[status],
        class_name=rx.match(
            status,
            (
                "compliant",
                "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800 w-fit",
            ),
            (
                "expiring_soon",
                "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 w-fit",
            ),
            (
                "expired",
                "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 w-fit",
            ),
            "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800 w-fit",
        ),
    )


def date_status_cell(date_str: rx.Var[str]) -> rx.Component:
    return rx.el.td(date_str, class_name="px-6 py-4 whitespace-nowrap text-sm")


def suspension_modal() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.cond(
                ComplianceState.user_to_suspend,
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        f"{State.t['suspend']} {ComplianceState.user_to_suspend['full_name']}"
                    ),
                    rx.el.div(
                        rx.el.label(State.t["suspension_reason"]),
                        rx.el.select(
                            rx.el.option(
                                State.t["policy_violation"], value="policy_violation"
                            ),
                            rx.el.option(State.t["expired"], value="expired_documents"),
                            rx.el.option(State.t["fraud"], value="fraud"),
                            rx.el.option(State.t["other"], value="other"),
                            on_change=ComplianceState.set_suspension_reason,
                            default_value="policy_violation",
                            class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                        ),
                        class_name="my-4",
                    ),
                    rx.el.div(
                        rx.el.label(State.t["notes"]),
                        rx.el.textarea(
                            on_change=ComplianceState.set_suspension_notes,
                            placeholder=State.t["rejection_reason_placeholder"],
                            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm",
                        ),
                        class_name="my-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            State.t["cancel"],
                            on_click=ComplianceState.close_suspension_dialog,
                            class_name="w-full justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50",
                        ),
                        rx.el.button(
                            State.t["confirm_suspension"],
                            on_click=ComplianceState.suspend_user,
                            class_name="w-full justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-red-600 hover:bg-red-700",
                        ),
                        class_name="flex gap-4 mt-6",
                    ),
                ),
            ),
            class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-8 rounded-lg shadow-2xl max-w-lg w-full z-50",
        ),
        open=ComplianceState.user_to_suspend.is_not_none(),
    )


def compliance_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        suspension_modal(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["compliance_dashboard"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    AuthState.user_role == "admin",
                    rx.el.div(
                        rx.el.div(
                            rx.el.input(
                                placeholder=State.t["search_carrier"],
                                on_change=ComplianceState.set_search_query,
                                class_name="flex-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm",
                            ),
                            rx.el.select(
                                rx.el.option(State.t["all"], value="all"),
                                rx.el.option(State.t["compliant"], value="compliant"),
                                rx.el.option(
                                    State.t["expiring_soon"], value="expiring_soon"
                                ),
                                rx.el.option(State.t["expired"], value="expired"),
                                on_change=ComplianceState.set_status_filter,
                                class_name="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                            ),
                            class_name="flex gap-4 mt-6",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(State.t["carrier"]),
                                        rx.el.th(State.t["compliance_status"]),
                                        rx.el.th(State.t["license_expiry"]),
                                        rx.el.th(State.t["insurance_expiry"]),
                                        rx.el.th(State.t["inspection_expiry"]),
                                        rx.el.th(State.t["actions"]),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ComplianceState.filtered_carriers,
                                        lambda carrier: rx.el.tr(
                                            rx.el.td(carrier["full_name"]),
                                            rx.el.td(
                                                compliance_status_badge(
                                                    carrier["compliance_status"]
                                                )
                                            ),
                                            date_status_cell(carrier["license_expiry"]),
                                            date_status_cell(
                                                carrier["insurance_expiry"]
                                            ),
                                            date_status_cell(
                                                carrier["inspection_expiry"]
                                            ),
                                            rx.el.td(
                                                rx.cond(
                                                    carrier["is_suspended"],
                                                    rx.el.button(
                                                        State.t["unsuspend"],
                                                        on_click=lambda: ComplianceState.unsuspend_user(
                                                            carrier["id"]
                                                        ),
                                                        class_name="text-sm text-green-600 hover:underline",
                                                    ),
                                                    rx.el.button(
                                                        State.t["suspend"],
                                                        on_click=lambda: ComplianceState.open_suspension_dialog(
                                                            carrier
                                                        ),
                                                        class_name="text-sm text-red-600 hover:underline",
                                                    ),
                                                )
                                            ),
                                            class_name=rx.cond(
                                                carrier["is_suspended"],
                                                "bg-gray-200 opacity-70",
                                                "",
                                            ),
                                        ),
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200 mt-4",
                            ),
                            class_name="overflow-x-auto bg-white p-6 rounded-lg shadow-sm border mt-6",
                        ),
                    ),
                    rx.el.p("Access Denied.", class_name="text-red-500"),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=ComplianceState.load_carriers,
        ),
        class_name="bg-gray-50 min-h-screen",
    )