import reflex as rx
from app.states.state import State, AdminState, AuthState
from app.components.navbar import navbar
from app.components.stats import stat_card


def financial_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["financial_overview"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    AuthState.user_role == "admin",
                    rx.el.div(
                        rx.el.div(
                            stat_card(
                                "dollar-sign",
                                State.t["total_revenue"],
                                f"${AdminState.financial_overview['total_revenue']:.2f}",
                                "text-green-500",
                            ),
                            stat_card(
                                "percent",
                                State.t["platform_commission"],
                                f"${AdminState.financial_overview['platform_commission']:.2f}",
                                "text-blue-500",
                            ),
                            stat_card(
                                "clock",
                                State.t["pending_payouts"],
                                f"${AdminState.financial_overview['pending_payouts']:.2f}",
                                "text-yellow-500",
                            ),
                            stat_card(
                                "circle-check",
                                State.t["processed_payouts"],
                                f"${AdminState.financial_overview['processed_payouts']:.2f}",
                                "text-purple-500",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6",
                        ),
                        rx.el.h2(
                            State.t["payout_queue"],
                            class_name="text-2xl font-bold text-gray-900 mt-10",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th("Carrier ID"),
                                            rx.el.th(State.t["net_amount"]),
                                            rx.el.th(State.t["status"]),
                                            rx.el.th(State.t["scheduled_date"]),
                                            rx.el.th(State.t["actions"]),
                                        )
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            AdminState.payouts,
                                            lambda p: rx.el.tr(
                                                rx.el.td(p["carrier_id"]),
                                                rx.el.td(f"${p['net_amount']:.2f}"),
                                                rx.el.td(p["status"]),
                                                rx.el.td(p["scheduled_date"]),
                                                rx.el.td(
                                                    rx.el.button(
                                                        State.t["process_payout"],
                                                        class_name="text-sm text-indigo-600 hover:underline",
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
                    ),
                    rx.el.p(
                        "Access Denied. Admins only.", class_name="text-red-500 mt-4"
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=[
                AdminState.load_financial_overview,
                AdminState.load_payout_history,
            ],
        ),
        class_name="bg-gray-50 min-h-screen",
    )