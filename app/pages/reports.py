import reflex as rx
from app.states.state import State, AuthState, ReportingState
from app.components.navbar import navbar


def report_card(title: str, chart: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-900 mb-4"),
        chart,
        class_name="bg-white p-6 rounded-xl border shadow-sm",
    )


def reports_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        State.t["reporting_dashboard"],
                        class_name="text-3xl font-bold text-gray-900",
                    ),
                    rx.el.div(
                        rx.el.button(State.t["daily"]),
                        rx.el.button(State.t["weekly"]),
                        rx.el.button(State.t["monthly"]),
                        rx.el.button(
                            State.t["export_pdf"],
                            class_name="ml-auto bg-indigo-600 text-white px-4 py-2 rounded-md",
                        ),
                        class_name="flex gap-2 items-center mt-4",
                    ),
                ),
                rx.cond(
                    AuthState.user_role == "admin",
                    rx.el.div(
                        report_card(
                            State.t["revenue_trends"],
                            rx.recharts.line_chart(
                                rx.recharts.x_axis(data_key="name"),
                                rx.recharts.y_axis(),
                                rx.recharts.tooltip(),
                                rx.recharts.line(
                                    data_key="revenue",
                                    stroke="#8884d8",
                                    type_="monotone",
                                ),
                                data=ReportingState.revenue_data,
                                height=300,
                            ),
                        ),
                        report_card(
                            State.t["shipment_volume"],
                            rx.recharts.pie_chart(
                                rx.recharts.pie(
                                    data_key="value",
                                    data=ReportingState.shipment_volume_data,
                                    name_key="name",
                                    cx="50%",
                                    cy="50%",
                                    outer_radius=80,
                                    fill="#8884d8",
                                    label=True,
                                    stroke="#fff",
                                    stroke_width=2,
                                ),
                                rx.recharts.tooltip(),
                                height=300,
                            ),
                        ),
                        report_card(
                            State.t["user_growth"],
                            rx.recharts.area_chart(
                                rx.recharts.x_axis(data_key="name"),
                                rx.recharts.y_axis(),
                                rx.recharts.tooltip(),
                                rx.recharts.area(
                                    type_="monotone",
                                    data_key="users",
                                    stroke="#82ca9d",
                                    fill="#82ca9d",
                                ),
                                data=ReportingState.user_growth_data,
                                height=300,
                            ),
                        ),
                        report_card(
                            State.t["popular_routes"],
                            rx.recharts.bar_chart(
                                rx.recharts.x_axis(data_key="route"),
                                rx.recharts.y_axis(),
                                rx.recharts.tooltip(),
                                rx.recharts.bar(data_key="count", fill="#8884d8"),
                                data=ReportingState.popular_routes_data,
                                layout="vertical",
                                height=300,
                                margin={"left": 100},
                            ),
                        ),
                        class_name="grid md:grid-cols-2 gap-6 mt-6",
                    ),
                    rx.el.p("Access Denied.", class_name="text-red-500"),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=ReportingState.load_reports,
        ),
        class_name="bg-gray-50 min-h-screen",
    )