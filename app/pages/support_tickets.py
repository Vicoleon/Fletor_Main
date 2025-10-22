import reflex as rx
from app.states.state import State, AdminState, AuthState
from app.components.navbar import navbar


def priority_badge(priority: str) -> rx.Component:
    color_map = {
        "low": "bg-gray-100 text-gray-800",
        "medium": "bg-yellow-100 text-yellow-800",
        "high": "bg-orange-100 text-orange-800",
        "urgent": "bg-red-100 text-red-800",
    }
    return rx.el.span(
        State.t[priority],
        class_name=rx.cond(
            priority,
            f"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {color_map.get(priority, 'bg-gray-100 text-gray-800')} w-fit",
            "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800 w-fit",
        ),
    )


def status_badge(status: str) -> rx.Component:
    color_map = {
        "new": "bg-blue-100 text-blue-800",
        "assigned": "bg-indigo-100 text-indigo-800",
        "in_progress": "bg-purple-100 text-purple-800",
        "resolved": "bg-green-100 text-green-800",
        "closed": "bg-gray-100 text-gray-800",
    }
    return rx.el.span(
        State.t[status],
        class_name=rx.cond(
            status,
            f"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {color_map.get(status, 'bg-gray-100 text-gray-800')} w-fit",
            "px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800 w-fit",
        ),
    )


def ticket_card(ticket: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                f"ID: {ticket['id'].to_string()[:8]}",
                class_name="text-sm font-mono text-gray-500",
            ),
            priority_badge(ticket["priority"]),
            class_name="flex justify-between items-center",
        ),
        rx.el.h3(ticket["subject"], class_name="font-semibold mt-2"),
        rx.el.p(
            f"{State.t['category']}: {State.t[ticket['category']]}",
            class_name="text-sm text-gray-600",
        ),
        rx.el.p(
            f"{State.t['user_id']}: {ticket['user_id']}",
            class_name="text-sm text-gray-600",
        ),
        rx.el.div(
            status_badge(ticket["status"]),
            rx.el.button(
                State.t["view"], class_name="text-sm text-indigo-600 hover:underline"
            ),
            class_name="flex justify-between items-center mt-4",
        ),
        class_name="bg-white p-4 rounded-lg shadow-sm border",
    )


def support_tickets_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["support_tickets"],
                    class_name="text-3xl font-bold text-gray-900",
                ),
                rx.cond(
                    AuthState.user_role == "admin",
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(AdminState.support_tickets, ticket_card),
                            class_name="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6",
                        )
                    ),
                    rx.el.p(
                        "Access Denied. Admins only.", class_name="text-red-500 mt-4"
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=AdminState.load_support_tickets,
        ),
        class_name="bg-gray-50 min-h-screen",
    )