import reflex as rx
from app.states.state import State, AuthState, ActivityLogState
from app.components.navbar import navbar


def activity_log_row(log: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    State.t[log["action_type"]], class_name="font-medium text-gray-900"
                ),
                rx.el.p(log["timestamp"], class_name="text-sm text-gray-500"),
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(log["admin_user_id"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(log["target_id"], class_name="px-6 py-4 whitespace-nowrap"),
        rx.el.td(
            rx.el.p(log["notes"] | "N/A", class_name="max-w-xs truncate"),
            class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
        ),
    )


def activity_logs_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["activity_logs"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    AuthState.user_role == "admin",
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(State.t["filter_by_action"]),
                                rx.el.select(
                                    rx.el.option(State.t["all"], value="all"),
                                    rx.el.option(
                                        State.t["user_approved"], value="user_approved"
                                    ),
                                    rx.el.option(
                                        State.t["user_rejected"], value="user_rejected"
                                    ),
                                    rx.el.option(
                                        State.t["user_suspended"],
                                        value="user_suspended",
                                    ),
                                    rx.el.option(
                                        State.t["user_unsuspended"],
                                        value="user_unsuspended",
                                    ),
                                    on_change=ActivityLogState.set_action_filter,
                                    class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                                ),
                            ),
                            rx.el.button(
                                State.t["export_csv"],
                                class_name="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700",
                            ),
                            class_name="flex justify-between items-end mt-6",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(State.t["action_type"]),
                                        rx.el.th(State.t["admin_user"]),
                                        rx.el.th(State.t["target"]),
                                        rx.el.th(State.t["notes"]),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        ActivityLogState.filtered_logs, activity_log_row
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200 mt-4",
                            ),
                            class_name="overflow-x-auto",
                        ),
                    ),
                    rx.el.p("Access Denied.", class_name="text-red-500"),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=ActivityLogState.load_logs,
        ),
        class_name="bg-gray-50 min-h-screen",
    )