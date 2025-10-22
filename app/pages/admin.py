import reflex as rx
from app.states.state import State, AdminState, AuthState
from app.components.navbar import navbar
from app.components.stats import stat_card


def user_verification_card(user: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(user["full_name"], class_name="font-semibold text-lg"),
            rx.el.p(user["email"], class_name="text-sm text-gray-600"),
            rx.el.span(
                user["role"],
                class_name="mt-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 w-fit",
            ),
        ),
        rx.el.div(
            rx.el.button(
                State.t["review"],
                on_click=lambda: AdminState.select_user_for_verification(user),
                class_name="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700",
            ),
            class_name="flex gap-4 mt-4",
        ),
        class_name="p-6 bg-white rounded-lg shadow-md border flex flex-col justify-between",
    )


def document_viewer() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(
                f"{State.t['verifying']} {AdminState.selected_user_for_verification['full_name']}"
            ),
            rx.el.div(
                rx.el.h3(
                    State.t["uploaded_documents"],
                    class_name="text-lg font-semibold mt-4 mb-2",
                ),
                rx.cond(
                    AdminState.selected_user_documents.length() > 0,
                    rx.foreach(
                        AdminState.selected_user_documents,
                        lambda doc: rx.el.a(
                            rx.el.div(
                                rx.icon(tag="file-text", class_name="mr-2"),
                                rx.el.p(doc["name"]),
                                class_name="flex items-center p-2 border-b hover:bg-gray-50",
                            ),
                            href=rx.get_upload_url(doc["path"]),
                            target="_blank",
                        ),
                    ),
                    rx.el.p(
                        State.t["no_documents_uploaded"], class_name="text-gray-500"
                    ),
                ),
                rx.el.h3(
                    State.t["actions"], class_name="text-lg font-semibold mt-6 mb-2"
                ),
                rx.el.div(
                    rx.el.textarea(
                        placeholder=State.t["approval_notes_placeholder"],
                        on_change=AdminState.set_approval_notes,
                        class_name="w-full p-2 border rounded-md",
                    ),
                    rx.el.button(
                        State.t["approve"],
                        on_click=AdminState.approve_user_with_notes,
                        class_name="w-full mt-2 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600",
                    ),
                    class_name="mt-4",
                ),
                rx.el.div(
                    rx.el.textarea(
                        placeholder=State.t["rejection_reason_placeholder"],
                        on_change=AdminState.set_rejection_reason,
                        class_name="w-full p-2 border rounded-md",
                    ),
                    rx.el.button(
                        State.t["reject"],
                        on_click=AdminState.reject_user_with_reason,
                        class_name="w-full mt-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600",
                    ),
                    class_name="mt-4",
                ),
            ),
            rx.radix.primitives.dialog.close(
                rx.el.button(
                    State.t["close"],
                    on_click=AdminState.deselect_user,
                    class_name="mt-4 w-full px-4 py-2 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300",
                )
            ),
            class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-8 rounded-lg shadow-2xl max-w-lg w-full z-50",
        ),
        open=AdminState.selected_user_for_verification.is_not_none(),
    )


def admin_dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.h1(
            State.t["admin_dashboard"], class_name="text-3xl font-bold text-gray-900"
        ),
        rx.el.div(
            stat_card(
                State.t["total_users"],
                "users",
                AdminState.analytics["total_users"].to_string(),
                "text-blue-500",
            ),
            stat_card(
                State.t["total_shippers"],
                "package",
                AdminState.analytics["total_shippers"].to_string(),
                "text-green-500",
            ),
            stat_card(
                State.t["total_carriers"],
                "truck",
                AdminState.analytics["total_carriers"].to_string(),
                "text-yellow-500",
            ),
            stat_card(
                State.t["active_shipments"],
                "activity",
                AdminState.analytics["active_shipments"].to_string(),
                "text-indigo-500",
            ),
            stat_card(
                State.t["completed_shipments"],
                "check-circle",
                AdminState.analytics["completed_shipments"].to_string(),
                "text-purple-500",
            ),
            stat_card(
                State.t["total_revenue"],
                "dollar-sign",
                f"${AdminState.analytics['total_revenue']:.2f}",
                "text-pink-500",
            ),
            stat_card(
                State.t["platform_commission"],
                "briefcase",
                f"${AdminState.analytics['platform_commission']:.2f}",
                "text-red-500",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6",
        ),
        rx.el.h2(
            State.t["user_verification"],
            class_name="text-2xl font-bold text-gray-900 mt-10",
        ),
        rx.cond(
            AdminState.users_for_verification.length() > 0,
            rx.el.div(
                rx.foreach(AdminState.users_for_verification, user_verification_card),
                class_name="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6",
            ),
            rx.el.p(
                State.t["no_users_for_verification"], class_name="mt-6 text-gray-500"
            ),
        ),
        document_viewer(),
    )


def admin_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.cond(
                    AuthState.user_role == "admin",
                    admin_dashboard_content(),
                    rx.el.p("Access Denied. Admins only.", class_name="text-red-500"),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=AdminState.load_admin_dashboard,
        ),
        class_name="bg-gray-50 min-h-screen",
    )