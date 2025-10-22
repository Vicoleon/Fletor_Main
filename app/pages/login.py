import reflex as rx
from app.states.state import State, AuthState
from app.components.navbar import navbar


def login_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        State.t["login"],
                        class_name="text-center text-3xl font-extrabold text-gray-900",
                    ),
                    rx.cond(
                        AuthState.error_message != "",
                        rx.el.div(
                            AuthState.error_message,
                            class_name="mt-4 p-3 bg-red-100 text-red-700 rounded-md text-sm",
                        ),
                        None,
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(State.t["email"], class_name="sr-only"),
                            rx.el.input(
                                name="email",
                                placeholder=State.t["email"],
                                type="email",
                                class_name="appearance-none rounded-t-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
                            ),
                            rx.el.label(State.t["password"], class_name="sr-only"),
                            rx.el.input(
                                name="password",
                                placeholder=State.t["password"],
                                type="password",
                                class_name="appearance-none rounded-b-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm",
                            ),
                            class_name="rounded-md shadow-sm -space-y-px",
                        ),
                        rx.el.button(
                            State.t["login"],
                            type="submit",
                            class_name="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mt-6",
                        ),
                        on_submit=AuthState.handle_login,
                        class_name="mt-8 space-y-6",
                    ),
                    class_name="max-w-md w-full space-y-8",
                ),
                class_name="min-h-full flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8",
            )
        ),
        class_name="bg-gray-50",
    )