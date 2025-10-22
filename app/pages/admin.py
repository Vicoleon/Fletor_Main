import reflex as rx
from app.states.state import State, AdminState, AuthState
from app.components.navbar import navbar


def user_verification_card(user: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(user["full_name"], class_name="font-semibold text-lg"),
            rx.el.p(user["email"], class_name="text-sm text-gray-600"),
            rx.el.span(
                user["role"],
                class_name="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800",
            ),
        ),
        rx.el.div(
            rx.el.button(
                State.t["approve"],
                on_click=lambda: AdminState.approve_user(user["id"]),
                class_name="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600",
            ),
            rx.el.button(
                State.t["reject"],
                on_click=lambda: AdminState.reject_user(user["id"]),
                class_name="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600",
            ),
            class_name="flex gap-4 mt-4",
        ),
        class_name="p-6 bg-white rounded-lg shadow-md border",
    )


def admin_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["user_verification"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    AuthState.user_role != "admin",
                    rx.el.p("Access Denied. Admins only."),
                    rx.el.div(
                        rx.foreach(
                            AdminState.users_for_verification, user_verification_card
                        ),
                        class_name="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=AdminState.load_unverified_users,
        ),
        class_name="bg-gray-50 min-h-screen",
    )