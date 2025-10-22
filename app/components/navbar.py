import reflex as rx
from app.states.state import State, AuthState


def nav_link(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name="text-sm font-medium text-gray-500 hover:text-gray-900",
    )


def navbar() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.div(
                        rx.icon(tag="box", class_name="h-6 w-6 text-indigo-600"),
                        rx.el.span(State.t["title"], class_name="text-xl font-bold"),
                        class_name="flex items-center gap-2",
                    ),
                    href="/",
                ),
                class_name="flex items-center gap-4",
            ),
            rx.el.nav(
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        nav_link(State.t["dashboard"], "/dashboard"),
                        nav_link(State.t["profile"], "/profile"),
                        rx.cond(
                            AuthState.user_role == "admin",
                            nav_link(State.t["admin"], "/admin"),
                            None,
                        ),
                        rx.cond(
                            AuthState.user_role == "shipper",
                            nav_link(State.t["create_shipment"], "/create-shipment"),
                            None,
                        ),
                        rx.cond(
                            AuthState.user_role == "carrier",
                            nav_link(State.t["browse_jobs"], "/jobs"),
                            None,
                        ),
                        class_name="flex items-center gap-4",
                    ),
                    rx.el.div(),
                ),
                class_name="flex-1 flex justify-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.cond(State.current_language == "en", "ES", "EN"),
                    on_click=State.toggle_language,
                    class_name="text-sm font-medium text-gray-500 hover:text-gray-900",
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.button(
                        State.t["logout"],
                        on_click=AuthState.logout,
                        class_name="ml-4 inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                    ),
                    rx.el.div(
                        nav_link(State.t["login"], "/login"),
                        rx.el.a(
                            State.t["register"],
                            href="/register",
                            class_name="ml-4 inline-flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                        ),
                        class_name="flex items-center",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-center justify-between h-16 px-4 sm:px-6 lg:px-8 border-b",
        ),
        class_name="bg-white w-full sticky top-0 z-50",
    )