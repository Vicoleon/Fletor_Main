import reflex as rx
from app.states.state import State, AuthState, InvoiceState
from app.components.navbar import navbar


def status_badge(status: str) -> rx.Component:
    color_map = {
        "issued": "bg-blue-100 text-blue-800",
        "paid": "bg-green-100 text-green-800",
        "overdue": "bg-red-100 text-red-800",
        "draft": "bg-gray-100 text-gray-800",
    }
    return rx.el.span(
        State.t[status],
        class_name=f"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {color_map.get(status, 'bg-gray-100 text-gray-800')} w-fit",
    )


def invoice_row(invoice: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            invoice["invoice_number"],
            class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
        ),
        rx.el.td(
            invoice["issue_date"], class_name="px-6 py-4 whitespace-nowrap text-sm"
        ),
        rx.el.td(invoice["due_date"], class_name="px-6 py-4 whitespace-nowrap text-sm"),
        rx.el.td(
            f"${invoice['total']:.2f}",
            class_name="px-6 py-4 whitespace-nowrap text-sm text-right font-semibold",
        ),
        rx.el.td(status_badge(invoice["status"])),
        rx.el.td(
            rx.el.button(
                rx.icon(tag="download", class_name="h-4 w-4 mr-2"),
                State.t["download_pdf"],
                class_name="text-sm text-indigo-600 hover:underline flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap text-right text-sm font-medium",
        ),
    )


def invoices_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["invoices"], class_name="text-3xl font-bold text-gray-900"
                ),
                rx.cond(
                    AuthState.is_authenticated,
                    rx.el.div(
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(State.t["invoice_number"]),
                                        rx.el.th(State.t["issue_date"]),
                                        rx.el.th(State.t["due_date"]),
                                        rx.el.th(
                                            State.t["total"], class_name="text-right"
                                        ),
                                        rx.el.th(State.t["status"]),
                                        rx.el.th(""),
                                    )
                                ),
                                rx.el.tbody(
                                    rx.cond(
                                        InvoiceState.invoices.length() > 0,
                                        rx.foreach(InvoiceState.invoices, invoice_row),
                                        rx.el.tr(
                                            rx.el.td(
                                                State.t["no_invoices"],
                                                col_span=6,
                                                class_name="text-center py-10 text-gray-500",
                                            )
                                        ),
                                    )
                                ),
                                class_name="min-w-full divide-y divide-gray-200 mt-4",
                            ),
                            class_name="overflow-x-auto bg-white p-6 rounded-xl border shadow-sm mt-6",
                        )
                    ),
                    rx.el.p("Please log in to view your invoices.", class_name="mt-4"),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=InvoiceState.load_invoices,
        ),
        class_name="bg-gray-50 min-h-screen",
    )