import reflex as rx
from app.states.state import State, AuthState, Shipment, InvoiceState, Location
from app.components.navbar import navbar
from app.states.state import CarrierState, TrackingState


class ShipmentDetailState(State):
    shipment: Shipment | None = None

    @rx.event
    async def load_shipment(self):
        from app.db_utils import get_shipment_by_id
        from typing import cast

        shipment_id = self.router.page.params.get("id")
        if not shipment_id:
            yield rx.redirect("/dashboard")
            return
        shipment_data = await get_shipment_by_id(shipment_id)
        if shipment_data:
            self.shipment = cast(
                Shipment,
                {
                    "id": shipment_data["id"],
                    "shipper_id": shipment_data["shipper_id"],
                    "carrier_id": shipment_data.get("carrier_id"),
                    "pickup_location": {
                        "address": shipment_data["pickup_address"],
                        "city": shipment_data["pickup_city"],
                        "province": shipment_data["pickup_province"],
                        "postal_code": "",
                        "lat": 0,
                        "lng": 0,
                    },
                    "delivery_location": {
                        "address": shipment_data["delivery_address"],
                        "city": shipment_data["delivery_city"],
                        "province": shipment_data["delivery_province"],
                        "postal_code": "",
                        "lat": 0,
                        "lng": 0,
                    },
                    "cargo_type": shipment_data["cargo_type"],
                    "weight_kg": shipment_data["weight_kg"],
                    "length_m": shipment_data.get("length_cm", 0),
                    "width_m": shipment_data.get("width_cm", 0),
                    "height_m": shipment_data.get("height_cm", 0),
                    "special_instructions": shipment_data.get(
                        "special_instructions", ""
                    ),
                    "pickup_datetime": str(shipment_data["pickup_datetime"]),
                    "status": shipment_data["status"],
                    "price": shipment_data["price"],
                    "created_at": str(shipment_data["createdAt"]),
                    "timeline": [],
                    "current_lat": None,
                    "current_lng": None,
                    "route_polyline": None,
                },
            )
        else:
            yield rx.redirect("/dashboard")


def detail_item(label: rx.Var[str], value: rx.Var) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="mt-1 text-lg font-semibold text-gray-900"),
    )


def shipment_detail_card(shipment: rx.Var[dict]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h2(
                f"{State.t['shipment_details']} - ID: {shipment['id'].to_string()[:8]}",
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.div(
                rx.el.a(
                    State.t["track_shipment"],
                    href=f"/tracking/{shipment['id']}",
                    class_name="inline-flex items-center gap-2 px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200",
                ),
                rx.el.a(
                    rx.cond(
                        AuthState.user_role == "shipper",
                        State.t["message_carrier"],
                        State.t["message_shipper"],
                    ),
                    href=f"/messages/{shipment['id']}",
                    class_name="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200",
                ),
                class_name="flex gap-2",
            ),
            class_name="flex justify-between items-center",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    State.t["pickup_location"],
                    class_name="text-lg font-medium text-gray-900 border-b pb-2 mb-4",
                ),
                detail_item(State.t["address"], shipment["pickup_location"]["address"]),
                detail_item(State.t["city"], shipment["pickup_location"]["city"]),
                detail_item(
                    State.t["province"], shipment["pickup_location"]["province"]
                ),
                class_name="p-6 bg-white rounded-lg shadow-md border",
            ),
            rx.el.div(
                rx.el.h3(
                    State.t["delivery_location"],
                    class_name="text-lg font-medium text-gray-900 border-b pb-2 mb-4",
                ),
                detail_item(
                    State.t["address"], shipment["delivery_location"]["address"]
                ),
                detail_item(State.t["city"], shipment["delivery_location"]["city"]),
                detail_item(
                    State.t["province"], shipment["delivery_location"]["province"]
                ),
                class_name="p-6 bg-white rounded-lg shadow-md border",
            ),
            rx.el.div(
                rx.el.h3(
                    State.t["cargo_details"],
                    class_name="text-lg font-medium text-gray-900 border-b pb-2 mb-4",
                ),
                detail_item(State.t["cargo_type"], State.t[shipment["cargo_type"]]),
                detail_item(State.t["weight_kg"], f"{shipment['weight_kg']} kg"),
                detail_item(
                    State.t["dimensions_m"],
                    f"{shipment['length_m']} x {shipment['width_m']} x {shipment['height_m']} cm",
                ),
                detail_item(
                    State.t["special_instructions"],
                    shipment["special_instructions"] | "N/A",
                ),
                class_name="p-6 bg-white rounded-lg shadow-md border",
            ),
            rx.el.div(
                rx.el.h3(
                    "Status & Logistics",
                    class_name="text-lg font-medium text-gray-900 border-b pb-2 mb-4",
                ),
                detail_item(State.t["status"], State.t[shipment["status"]]),
                detail_item(State.t["price"], f"${shipment['price']:.2f}"),
                detail_item(State.t["pickup_datetime"], shipment["pickup_datetime"]),
                class_name="p-6 bg-white rounded-lg shadow-md border",
            ),
            class_name="grid md:grid-cols-2 gap-6 mt-6",
        ),
    )


def shipment_detail_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            rx.el.div(
                rx.cond(
                    ~AuthState.is_authenticated,
                    rx.el.p("Please log in to view shipment details."),
                    rx.cond(
                        ShipmentDetailState.shipment,
                        rx.el.div(
                            shipment_detail_card(ShipmentDetailState.shipment),
                            rx.cond(
                                (
                                    ShipmentDetailState.shipment["status"]
                                    == "pending_assignment"
                                )
                                & (AuthState.user_role == "carrier"),
                                rx.el.div(
                                    rx.el.button(
                                        State.t["accept_job"],
                                        on_click=lambda: CarrierState.accept_job(
                                            ShipmentDetailState.shipment["id"]
                                        ),
                                        class_name="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-green-600 hover:bg-green-700",
                                    ),
                                    rx.el.a(
                                        State.t["decline_job"],
                                        href="/jobs",
                                        class_name="w-full text-center py-3 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50",
                                    ),
                                    class_name="mt-8 flex flex-col md:flex-row gap-4",
                                ),
                                None,
                            ),
                        ),
                        rx.el.p("Loading shipment..."),
                    ),
                ),
                class_name="max-w-7xl mx-auto py-10 px-4",
            ),
            on_mount=ShipmentDetailState.load_shipment,
        ),
        class_name="bg-gray-50 min-h-screen",
    )