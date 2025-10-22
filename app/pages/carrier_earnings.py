import reflex as rx
from app.states.state import State, AuthState, CarrierEarningsState
from app.components.navbar import navbar
from app.components.stats import stat_card


def payout_row(payout: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            payout["id"].to_string()[:8],
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
        rx.el.td(
            f"${payout['net_amount']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm font-semibold",
        ),
        rx.el.td(payout["status"], class_name="px-6 py-4 whitespace-nowrap text-sm"),
        rx.el.td(
            payout["scheduled_date"], class_name="px-6 py-4 whitespace-nowrap text-sm"
        ),
        rx.el.td(
            payout["processed_date"] | "-",
            class_name="px-6 py-4 whitespace-nowrap text-sm",
        ),
    )


def carrier_earnings_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["carrier_earnings"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    AuthState.user_role == "carrier",
                    rx.el.div(
                        rx.el.div(
                            stat_card(
                                "dollar-sign",
                                State.t["total_earnings"],
                                f"${CarrierEarningsState.total_earnings:.2f}",
                                "text-green-500",
                            ),
                            stat_card(
                                "percent",
                                State.t["platform_commission"],
                                f"-${CarrierEarningsState.platform_commission:.2f}",
                                "text-red-500",
                            ),
                            stat_card(
                                "wallet",
                                State.t["net_earnings"],
                                f"${CarrierEarningsState.net_earnings:.2f}",
                                "text-blue-500",
                            ),
                            stat_card(
                                "award",
                                State.t["available_for_payout"],
                                f"${CarrierEarningsState.available_for_payout:.2f}",
                                "text-indigo-500",
                            ),
                            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6",
                        ),
                        rx.el.div(
                            rx.el.h2(
                                State.t["payout_history"],
                                class_name="text-xl font-semibold",
                            ),
                            rx.el.button(
                                State.t["request_payout"],
                                on_click=CarrierEarningsState.request_payout,
                                class_name="ml-auto bg-indigo-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-indigo-700",
                                disabled=CarrierEarningsState.available_for_payout <= 0,
                            ),
                            class_name="flex items-center justify-between mt-10",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(State.t["transaction_id"]),
                                        rx.el.th(State.t["amount"]),
                                        rx.el.th(State.t["status"]),
                                        rx.el.th(State.t["scheduled_date"]),
                                        rx.el.th("Processed Date"),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.cond(
                                        CarrierEarningsState.payout_history.length()
                                        > 0,
                                        rx.foreach(
                                            CarrierEarningsState.payout_history,
                                            payout_row,
                                        ),
                                        rx.el.tr(
                                            rx.el.td(
                                                State.t["no_earnings_yet"],
                                                col_span=5,
                                                class_name="text-center py-10 text-gray-500",
                                            )
                                        ),
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200 mt-4",
                            ),
                            class_name="overflow-x-auto bg-white p-6 rounded-xl border shadow-sm mt-6",
                        ),
                    ),
                    rx.el.p(
                        "Access Denied. This page is for carriers only.",
                        class_name="mt-4 text-red-500",
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=CarrierEarningsState.load_earnings_data,
        ),
        class_name="bg-gray-50 min-h-screen",
    )