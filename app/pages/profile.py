import reflex as rx
from app.states.state import State, ProfileState, AuthState
from app.components.navbar import navbar


def profile_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.el.h1(
                    State.t["profile"], class_name="text-3xl font-bold text-gray-900"
                ),
                rx.cond(
                    ~AuthState.is_authenticated,
                    rx.el.p("Please log in to view your profile."),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                State.t["profile"],
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.el.p(
                                f"{State.t['full_name']}: {ProfileState.current_user['full_name']}"
                            ),
                            rx.el.p(
                                f"{State.t['email']}: {ProfileState.current_user['email']}"
                            ),
                            rx.el.p(
                                f"{State.t['phone_number']}: {ProfileState.current_user['phone']}"
                            ),
                            rx.cond(
                                ProfileState.current_user["role"] == "shipper",
                                rx.el.p(
                                    f"{State.t['company_name']}: {ProfileState.current_user['company_name']}"
                                ),
                                None,
                            ),
                            rx.cond(
                                ProfileState.current_user["role"] == "carrier",
                                rx.el.div(
                                    rx.el.p(
                                        f"{State.t['license_number']}: {ProfileState.current_user['license_number']}"
                                    ),
                                    rx.el.p(
                                        f"{State.t['vehicle_type']}: {ProfileState.current_user['vehicle_type']}"
                                    ),
                                ),
                                None,
                            ),
                            class_name="p-6 bg-white rounded-lg shadow-md border",
                        ),
                        rx.cond(
                            AuthState.user_role == "carrier",
                            rx.el.div(
                                rx.el.h2(
                                    State.t["fleet_management"],
                                    class_name="text-xl font-semibold mb-4",
                                ),
                                rx.el.p(
                                    f"{State.t['license_number']}: {ProfileState.current_user['license_number']}"
                                ),
                                rx.el.p(
                                    f"{State.t['vehicle_type']}: {ProfileState.current_user['vehicle_type']}"
                                ),
                                class_name="p-6 bg-white rounded-lg shadow-md border",
                            ),
                            None,
                        ),
                        rx.el.div(
                            rx.el.h2(
                                State.t["upload_documents"],
                                class_name="text-xl font-semibold mb-4",
                            ),
                            rx.upload.root(
                                rx.el.div(
                                    rx.icon(
                                        tag="cloud_upload",
                                        class_name="mx-auto h-12 w-12 text-gray-400",
                                    ),
                                    rx.el.p(
                                        "Drag and drop files here, or click to select files",
                                        class_name="mt-2 text-sm text-gray-600",
                                    ),
                                    class_name="text-center p-6 border-2 border-dashed border-gray-300 rounded-md cursor-pointer",
                                ),
                                id="upload_area",
                                multiple=True,
                                accept={
                                    "image/png": [".png"],
                                    "image/jpeg": [".jpg", ".jpeg"],
                                    "application/pdf": [".pdf"],
                                },
                            ),
                            rx.el.button(
                                State.t["upload"],
                                on_click=ProfileState.handle_upload(
                                    rx.upload_files(upload_id="upload_area")
                                ),
                                class_name="mt-4 w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700",
                            ),
                            rx.el.h3(
                                State.t["uploaded_files"],
                                class_name="mt-6 text-lg font-medium",
                            ),
                            rx.foreach(
                                ProfileState.user_documents,
                                lambda doc: rx.el.div(
                                    rx.icon(tag="file-text", class_name="mr-2"),
                                    rx.el.span(doc["name"]),
                                    class_name="flex items-center p-2 border-b",
                                ),
                            ),
                            class_name="p-6 bg-white rounded-lg shadow-md border mt-6",
                        ),
                        class_name="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6",
                    ),
                ),
                class_name="max-w-4xl mx-auto py-10 px-4",
            ),
            on_mount=ProfileState.load_documents,
        ),
        class_name="bg-gray-50 min-h-screen",
    )