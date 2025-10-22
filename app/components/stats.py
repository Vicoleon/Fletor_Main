import reflex as rx


def stat_card(icon_name: str, title: str, value: str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(tag=icon_name, class_name=f"h-6 w-6 {color}"),
            class_name="p-3 bg-gray-100 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
            class_name="mt-2",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )