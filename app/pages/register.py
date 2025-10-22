import reflex as rx
from app.states.state import State, RegistrationState
from app.components.navbar import navbar


def form_input(label: str, placeholder: str, type: str, state_setter) -> rx.Component:
    return rx.el.div(
        rx.el.label(label, class_name="block text-sm font-medium text-gray-700"),
        rx.el.input(
            type=type,
            placeholder=placeholder,
            on_change=state_setter,
            class_name="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm",
        ),
    )


def register_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        State.t["register"],
                        class_name="text-center text-3xl font-extrabold text-gray-900",
                    ),
                    rx.cond(
                        RegistrationState.error_message != "",
                        rx.el.div(
                            RegistrationState.error_message,
                            class_name="mt-4 p-3 bg-red-100 text-red-700 rounded-md text-sm",
                        ),
                        None,
                    ),
                    rx.cond(
                        RegistrationState.success_message != "",
                        rx.el.div(
                            RegistrationState.success_message,
                            class_name="mt-4 p-3 bg-green-100 text-green-700 rounded-md text-sm",
                        ),
                        None,
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                State.t["select_role"],
                                class_name="block text-sm font-medium text-gray-700",
                            ),
                            rx.el.select(
                                rx.el.option(State.t["shipper"], value="shipper"),
                                rx.el.option(State.t["carrier"], value="carrier"),
                                value=RegistrationState.reg_user_type,
                                on_change=RegistrationState.set_reg_user_type,
                                class_name="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md",
                            ),
                            class_name="mb-4",
                        ),
                        form_input(
                            State.t["full_name"],
                            "Juan Pérez",
                            "text",
                            RegistrationState.set_reg_full_name,
                        ),
                        form_input(
                            State.t["email"],
                            "juan.perez@example.com",
                            "email",
                            RegistrationState.set_reg_email,
                        ),
                        form_input(
                            State.t["phone_number"],
                            "8888-8888",
                            "tel",
                            RegistrationState.set_reg_phone,
                        ),
                        rx.cond(
                            RegistrationState.reg_user_type == "shipper",
                            form_input(
                                State.t["company_name"],
                                "Mi Empresa S.A.",
                                "text",
                                RegistrationState.set_reg_company_name,
                            ),
                            rx.el.div(
                                form_input(
                                    State.t["license_number"],
                                    "123456789",
                                    "text",
                                    RegistrationState.set_reg_license_number,
                                ),
                                form_input(
                                    State.t["vehicle_type"],
                                    "Cabezal",
                                    "text",
                                    RegistrationState.set_reg_vehicle_type,
                                ),
                                class_name="space-y-4",
                            ),
                        ),
                        form_input(
                            State.t["password"],
                            "********",
                            "password",
                            RegistrationState.set_reg_password,
                        ),
                        form_input(
                            State.t["confirm_password"],
                            "********",
                            "password",
                            RegistrationState.set_reg_confirm_password,
                        ),
                        rx.el.button(
                            State.t["register"],
                            type="submit",
                            class_name="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 mt-6",
                        ),
                        on_submit=RegistrationState.handle_registration,
                        class_name="mt-8 space-y-4",
                    ),
                ),
                class_name="max-w-lg mx-auto py-12 px-4 sm:px-6 lg:px-8",
            )
        ),
        class_name="bg-gray-50 min-h-screen",
    )