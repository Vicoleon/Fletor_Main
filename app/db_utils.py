import reflex as rx
import bcrypt
import uuid
from sqlalchemy import text
from typing import Literal


def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


async def get_user_by_email(email: str):
    """Fetches a user from the database by email."""
    async with rx.asession() as session:
        result = await session.execute(
            text(
                'SELECT id, email, "passwordHash" as password_hash, "firstName" || \' \' || "lastName" as full_name, phone, "companyName" as company_name, "nationalId" as license_number, "userType" as role, status FROM users WHERE email = :email'
            ),
            {"email": email},
        )
        user = result.first()
        return user


async def get_user_by_id(user_id: str):
    """Fetches a user from the database by ID."""
    async with rx.asession() as session:
        result = await session.execute(
            text(
                'SELECT id, email, "passwordHash", "firstName" || \' \' || "lastName" as full_name, phone, "companyName" as company_name, "userType" as role, "nationalId" as license_number, status FROM users WHERE id = :id'
            ),
            {"id": user_id},
        )
        user = result.first()
        return user


async def save_uploaded_file(
    user_id: str, file_name: str, file_path: str, file_size: int, mime_type: str | None
) -> str:
    """Saves uploaded file metadata to the database."""
    file_id = str(uuid.uuid4())
    async with rx.asession() as session:
        await session.execute(
            text(
                "INSERT INTO uploaded_files (id, user_id, file_name, file_path, file_size, mime_type) VALUES (:id, :user_id, :file_name, :file_path, :file_size, :mime_type)"
            ),
            {
                "id": file_id,
                "user_id": user_id,
                "file_name": file_name,
                "file_path": file_path,
                "file_size": file_size,
                "mime_type": mime_type,
            },
        )
        await session.commit()
    return file_id


async def get_user_documents(user_id: str):
    """Fetches all documents for a given user."""
    async with rx.asession() as session:
        result = await session.execute(
            text(
                "SELECT id, user_id, file_name as name, file_path as path, created_at as uploaded_at FROM uploaded_files WHERE user_id = :user_id ORDER BY created_at DESC"
            ),
            {"user_id": user_id},
        )
        documents = result.mappings().all()
        return [dict(doc) for doc in documents]


async def delete_uploaded_file(file_id: str):
    """Deletes a file record from the database."""
    async with rx.asession() as session:
        await session.execute(
            text("DELETE FROM uploaded_files WHERE id = :file_id"), {"file_id": file_id}
        )
        await session.commit()


async def get_users_for_verification():
    """Fetches users with status='PENDING' and kycStatus='PENDING'."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT id, email, "userType" as role, "firstName" || ' ' || "lastName" as full_name, "createdAt" 
                   FROM users 
                   WHERE status = 'PENDING' AND "kycStatus" = 'PENDING' 
                   ORDER BY "createdAt" ASC""")
        )
        users = result.mappings().all()
        return [dict(u) for u in users]


async def approve_user(user_id: str):
    """Updates user status to 'ACTIVE' and kycStatus to 'APPROVED'."""
    async with rx.asession() as session:
        await session.execute(
            text("""UPDATE users 
                   SET status = 'ACTIVE', "kycStatus" = 'APPROVED', "kycVerifiedAt" = now() 
                   WHERE id = :user_id"""),
            {"user_id": user_id},
        )
        await session.commit()


async def reject_user(user_id: str):
    """Updates user status to 'BANNED' and kycStatus to 'REJECTED'."""
    async with rx.asession() as session:
        await session.execute(
            text("""UPDATE users 
                   SET status = 'BANNED', "kycStatus" = 'REJECTED' 
                   WHERE id = :user_id"""),
            {"user_id": user_id},
        )
        await session.commit()


async def get_platform_analytics():
    """Calculates key platform metrics."""
    async with rx.asession() as session:
        users_res = await session.execute(
            text("""SELECT "userType", COUNT(id) as count 
                   FROM users 
                   WHERE "userType" IN ('SHIPPER', 'CARRIER')
                   GROUP BY "userType" """)
        )
        user_counts = {
            row["userType"]: row["count"] for row in users_res.mappings().all()
        }
        shipments_res = await session.execute(
            text("""SELECT status, COUNT(id) as count, SUM("quotedAmount") as revenue
                   FROM shipments
                   GROUP BY status""")
        )
        shipment_stats = {
            row["status"]: {"count": row["count"], "revenue": row["revenue"] or 0}
            for row in shipments_res.mappings().all()
        }
        total_revenue = shipment_stats.get("DELIVERED", {}).get("revenue", 0)
        analytics = {
            "total_users": sum(user_counts.values()),
            "total_shippers": user_counts.get("SHIPPER", 0),
            "total_carriers": user_counts.get("CARRIER", 0),
            "active_shipments": shipment_stats.get("IN_TRANSIT", {}).get("count", 0)
            + shipment_stats.get("ACCEPTED", {}).get("count", 0),
            "completed_shipments": shipment_stats.get("DELIVERED", {}).get("count", 0),
            "total_revenue": total_revenue,
            "platform_commission": total_revenue * 0.1,
        }
        return analytics


async def create_activity_log(
    admin_user_id: str, action_type: str, target_id: str, notes: str | None
):
    """Inserts a new record into the activity_logs table."""
    log_id = str(uuid.uuid4())
    async with rx.asession() as session:
        await session.execute(
            text("""INSERT INTO activity_logs (id, admin_user_id, action_type, target_id, notes)
                   VALUES (:id, :admin_user_id, :action_type, :target_id, :notes)"""),
            {
                "id": log_id,
                "admin_user_id": admin_user_id,
                "action_type": action_type,
                "target_id": target_id,
                "notes": notes,
            },
        )
        await session.commit()


async def get_carriers_with_compliance():
    """Fetch all carriers with compliance status calculation."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""                SELECT 
                    u.id,
                    u."firstName" || ' ' || u."lastName" as full_name,
                    u.email,
                    u."nationalId" as license_number,
                    u.status,
                    c."licenseExpiry" as license_expiry,
                    c."insuranceExpiry" as insurance_expiry,
                    c."inspectionExpiry" as inspection_expiry,
                    CASE 
                        WHEN u.status = 'SUSPENDED' THEN true
                        ELSE false
                    END as is_suspended
                FROM users u
                LEFT JOIN carriers c ON u.id = c."userId"
                WHERE u."userType" = 'CARRIER'
                ORDER BY u."createdAt" DESC
            """)
        )
        carriers = result.mappings().all()
        return [dict(carrier) for carrier in carriers]


async def suspend_carrier(user_id: str, admin_id: str, reason: str, notes: str):
    """Suspend a carrier account."""
    async with rx.asession() as session:
        await session.execute(
            text("""                UPDATE users 
                SET status = 'SUSPENDED',
                    "suspensionReason" = :reason,
                    "suspendedAt" = now(),
                    "suspendedBy" = :admin_id
                WHERE id = :user_id
            """),
            {"user_id": user_id, "admin_id": admin_id, "reason": f"{reason}: {notes}"},
        )
        await session.commit()
    await create_activity_log(
        admin_user_id=admin_id,
        action_type="user_suspended",
        target_id=user_id,
        notes=f"{reason}: {notes}",
    )


async def unsuspend_carrier(user_id: str, admin_id: str):
    """Reactivate a suspended carrier account."""
    async with rx.asession() as session:
        await session.execute(
            text("""                UPDATE users 
                SET status = 'ACTIVE',
                    "suspensionReason" = NULL,
                    "suspendedAt" = NULL,
                    "suspendedBy" = NULL
                WHERE id = :user_id
            """),
            {"user_id": user_id},
        )
        await session.commit()
    await create_activity_log(
        admin_user_id=admin_id,
        action_type="user_unsuspended",
        target_id=user_id,
        notes=None,
    )


async def get_activity_logs(action_type_filter: str | None = None):
    """Fetches activity logs, optionally filtering by action type."""
    query = "SELECT id, admin_user_id, action_type, target_id, notes, timestamp FROM activity_logs"
    params = {}
    if action_type_filter and action_type_filter != "all":
        query += " WHERE action_type = :action_type"
        params["action_type"] = action_type_filter
    query += " ORDER BY timestamp DESC LIMIT 100"
    async with rx.asession() as session:
        result = await session.execute(text(query), params)
        logs = result.mappings().all()
        return [dict(log) for log in logs]


import random
import string


async def create_shipment(shipment_data: dict) -> str:
    """Creates a new shipment in the database."""
    shipment_id = str(uuid.uuid4())
    tracking_number = (
        f"TRK-{''.join(random.choices(string.ascii_uppercase + string.digits, k=8))}"
    )
    async with rx.asession() as session:
        result = await session.execute(text("SELECT COUNT(id) FROM shipments"))
        shipment_count = result.scalar_one()
        shipment_number = f"SHP-{shipment_count + 1:05d}"
        await session.execute(
            text("""INSERT INTO shipments (
                id, "shipmentNumber", "trackingNumber", "shipperId", 
                description, "cargoType",
                "pickupContactName", "pickupContactPhone", "pickupAddressLine1",
                "pickupCity", "pickupProvince", "pickupDate",
                "deliveryContactName", "deliveryContactPhone", "deliveryAddressLine1",
                "deliveryCity", "deliveryProvince",
                "weightKg", "quotedAmount", status, "specialInstructions"
            ) VALUES (
                :id, :shipment_number, :tracking_number, :shipper_id,
                :description, :cargo_type,
                :pickup_contact_name, :pickup_contact_phone, :pickup_address,
                :pickup_city, :pickup_province, :pickup_date,
                :delivery_contact_name, :delivery_contact_phone, :delivery_address,
                :delivery_city, :delivery_province,
                :weight_kg, :quoted_amount, :status, :special_instructions
            )"""),
            {
                "id": shipment_id,
                "shipment_number": shipment_number,
                "tracking_number": tracking_number,
                "shipper_id": shipment_data["shipper_id"],
                "description": shipment_data["description"],
                "cargo_type": shipment_data["cargo_type"],
                "pickup_contact_name": shipment_data["pickup_contact_name"],
                "pickup_contact_phone": shipment_data["pickup_contact_phone"],
                "pickup_address": shipment_data["pickup_address"],
                "pickup_city": shipment_data["pickup_city"],
                "pickup_province": shipment_data["pickup_province"],
                "pickup_date": shipment_data["pickup_date"],
                "delivery_contact_name": shipment_data["delivery_contact_name"],
                "delivery_contact_phone": shipment_data["delivery_contact_phone"],
                "delivery_address": shipment_data["delivery_address"],
                "delivery_city": shipment_data["delivery_city"],
                "delivery_province": shipment_data["delivery_province"],
                "weight_kg": shipment_data["weight_kg"],
                "quoted_amount": shipment_data["quoted_amount"],
                "status": "PENDING",
                "special_instructions": shipment_data.get("special_instructions", ""),
            },
        )
        await session.execute(
            text("""INSERT INTO "trackingEvents" (
                id, "shipmentId", "eventType", description
            ) VALUES (:id, :shipment_id, :event_type, :description)"""),
            {
                "id": str(uuid.uuid4()),
                "shipment_id": shipment_id,
                "event_type": "CREATED",
                "description": "Shipment created and awaiting carrier assignment.",
            },
        )
        await session.commit()
    return shipment_id


async def get_shipment_by_id(shipment_id: str):
    """Fetches a single shipment by ID."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT 
                id, "shipmentNumber" as shipment_number, "trackingNumber" as tracking_number,
                "shipperId" as shipper_id, "carrierId" as carrier_id,
                description, "cargoType" as cargo_type,
                "pickupContactName" as pickup_contact_name, "pickupContactPhone" as pickup_contact_phone,
                "pickupAddressLine1" as pickup_address, "pickupCity" as pickup_city, 
                "pickupProvince" as pickup_province, "pickupDate" as pickup_datetime,
                "deliveryContactName" as delivery_contact_name, "deliveryContactPhone" as delivery_contact_phone,
                "deliveryAddressLine1" as delivery_address, "deliveryCity" as delivery_city,
                "deliveryProvince" as delivery_province,
                "weightKg" as weight_kg, "lengthCm" as length_m, "widthCm" as width_m, "heightCm" as height_m,
                "quotedAmount" as price, status, "specialInstructions" as special_instructions,
                "createdAt", "estimatedDelivery" as estimated_delivery
                FROM shipments WHERE id = :shipment_id"""),
            {"shipment_id": shipment_id},
        )
        row = result.first()
        if row:
            return dict(row._mapping)
        return None


async def get_shipments_by_shipper(shipper_id: str):
    """Fetches all shipments for a specific shipper."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT 
                id, "shipmentNumber" as shipment_number, "trackingNumber" as tracking_number,
                "shipperId" as shipper_id, "carrierId" as carrier_id,
                "cargoType" as cargo_type,
                "pickupCity" as pickup_city, "pickupProvince" as pickup_province,
                "deliveryCity" as delivery_city, "deliveryProvince" as delivery_province,
                "weightKg" as weight_kg, "quotedAmount" as price, status,
                "createdAt"
                FROM shipments 
                WHERE "shipperId" = :shipper_id
                ORDER BY "createdAt" DESC"""),
            {"shipper_id": shipper_id},
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]


async def get_shipments_by_carrier(carrier_id: str):
    """Fetches all shipments assigned to a specific carrier."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT 
                id, "shipmentNumber" as shipment_number, "trackingNumber" as tracking_number,
                "shipperId" as shipper_id, "carrierId" as carrier_id,
                "cargoType" as cargo_type,
                "pickupCity" as pickup_city, "pickupProvince" as pickup_province,
                "deliveryCity" as delivery_city, "deliveryProvince" as delivery_province,
                "weightKg" as weight_kg, "quotedAmount" as price, status,
                "createdAt"
                FROM shipments 
                WHERE "carrierId" = :carrier_id
                ORDER BY "createdAt" DESC"""),
            {"carrier_id": carrier_id},
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]


async def get_available_shipments():
    """Fetches all shipments available for carriers to accept."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT 
                id, "shipmentNumber" as shipment_number, "trackingNumber" as tracking_number,
                "shipperId" as shipper_id, "cargoType" as cargo_type,
                "pickupCity" as pickup_city, "pickupProvince" as pickup_province,
                "pickupDate" as pickup_datetime,
                "deliveryCity" as delivery_city, "deliveryProvince" as delivery_province,
                "weightKg" as weight_kg, "lengthCm" as length_m, "widthCm" as width_m, "heightCm" as height_m,
                "quotedAmount" as price, status, "specialInstructions" as special_instructions,
                "createdAt"
                FROM shipments 
                WHERE status = 'PENDING'
                ORDER BY "createdAt" DESC""")
        )
        rows = result.mappings().all()
        return [dict(row) for row in rows]


async def assign_shipment_to_carrier(shipment_id: str, carrier_id: str):
    """Assigns a shipment to a carrier."""
    async with rx.asession() as session:
        user_res = await session.execute(
            text("SELECT status FROM users WHERE id = :carrier_id"),
            {"carrier_id": carrier_id},
        )
        user = user_res.first()
        if not user or user.status != "ACTIVE":
            raise ValueError("Carrier is not active or does not exist.")
        await session.execute(
            text("""UPDATE shipments 
                   SET "carrierId" = :carrier_id, status = 'ACCEPTED'
                   WHERE id = :shipment_id AND status = 'PENDING'"""),
            {"carrier_id": carrier_id, "shipment_id": shipment_id},
        )
        await session.execute(
            text("""INSERT INTO "trackingEvents" (
                id, "shipmentId", "eventType", description, "createdBy"
            ) VALUES (:id, :shipment_id, :event_type, :description, :created_by)"""),
            {
                "id": str(uuid.uuid4()),
                "shipment_id": shipment_id,
                "event_type": "ACCEPTED",
                "description": "Shipment accepted by carrier.",
                "created_by": carrier_id,
            },
        )
        await session.commit()


async def update_shipment_status(
    shipment_id: str, new_status: str, user_id: str | None = None
):
    """Updates shipment status and creates tracking event."""
    await create_tracking_event(
        shipment_id=shipment_id,
        event_type=new_status,
        description=f"Status updated to {new_status}",
        user_id=user_id,
        is_automatic=False,
    )
    async with rx.asession() as session:
        await session.execute(
            text("UPDATE shipments SET status = :status WHERE id = :shipment_id"),
            {"status": new_status, "shipment_id": shipment_id},
        )
        await session.commit()


def calculate_shipment_quote(
    weight_kg: float,
    cargo_type: str,
    is_fragile: bool = False,
    requires_refrigeration: bool = False,
    requires_insurance: bool = False,
) -> dict:
    """Calculates a detailed price quote for a shipment."""
    base_rate = 50.0
    weight_surcharge = weight_kg * 0.1
    cargo_multipliers = {
        "general": 1.0,
        "refrigerated": 1.5,
        "hazardous": 2.0,
        "oversized": 1.8,
    }
    cargo_surcharge = base_rate * (cargo_multipliers.get(cargo_type, 1.0) - 1.0)
    fragile_surcharge = 20.0 if is_fragile else 0.0
    refrigeration_surcharge = 30.0 if requires_refrigeration else 0.0
    insurance_surcharge = 25.0 if requires_insurance else 0.0
    subtotal = (
        base_rate
        + weight_surcharge
        + cargo_surcharge
        + fragile_surcharge
        + refrigeration_surcharge
        + insurance_surcharge
    )
    tax = subtotal * 0.13
    total = subtotal + tax
    return {
        "base_rate": base_rate,
        "weight_surcharge": weight_surcharge,
        "cargo_surcharge": cargo_surcharge,
        "fragile_surcharge": fragile_surcharge,
        "refrigeration_surcharge": refrigeration_surcharge,
        "insurance_surcharge": insurance_surcharge,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
    }


async def get_tracking_events(shipment_id: str) -> list[dict]:
    """Fetches all tracking events for a shipment, sorted by time."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT 
                    id, "shipmentId" as shipment_id, "eventType" as event_type, 
                    description, notes, latitude, longitude, address, 
                    "eventTimestamp" as event_timestamp, "createdBy" as created_by, 
                    "isAutomatic" as is_automatic, metadata
                FROM "trackingEvents"
                WHERE "shipmentId" = :shipment_id
                ORDER BY "eventTimestamp" ASC"""),
            {"shipment_id": shipment_id},
        )
        events = result.mappings().all()
        return [dict(event) for event in events]


async def create_tracking_event(
    shipment_id: str,
    event_type: str,
    description: str,
    user_id: str | None = None,
    latitude: float | None = None,
    longitude: float | None = None,
    address: str | None = None,
    is_automatic: bool = False,
) -> str:
    """Creates a new tracking event."""
    event_id = str(uuid.uuid4())
    async with rx.asession() as session:
        await session.execute(
            text("""INSERT INTO "trackingEvents" (
                    id, "shipmentId", "eventType", description, "createdBy", 
                    latitude, longitude, address, "isAutomatic"
                ) VALUES (
                    :id, :shipment_id, :event_type, :description, :user_id, 
                    :latitude, :longitude, :address, :is_automatic
                )"""),
            {
                "id": event_id,
                "shipment_id": shipment_id,
                "event_type": event_type,
                "description": description,
                "user_id": user_id,
                "latitude": latitude,
                "longitude": longitude,
                "address": address,
                "is_automatic": is_automatic,
            },
        )
        await session.commit()
    return event_id


async def update_shipment_location(
    shipment_id: str, latitude: float, longitude: float, address: str | None
):
    """Updates the shipment's current location in the shipments table."""
    async with rx.asession() as session:
        await session.execute(
            text("""UPDATE shipments 
                   SET "currentLocation" = :address, 
                       latitude = :latitude, 
                       longitude = :longitude
                   WHERE id = :shipment_id"""),
            {
                "shipment_id": shipment_id,
                "address": address,
                "latitude": latitude,
                "longitude": longitude,
            },
        )
        await session.commit()


async def get_shipment_current_location(shipment_id: str) -> dict | None:
    """Gets the current location of a shipment."""
    async with rx.asession() as session:
        result = await session.execute(
            text("""SELECT latitude, longitude, "currentLocation" as address 
                   FROM shipments 
                   WHERE id = :shipment_id"""),
            {"shipment_id": shipment_id},
        )
        location = result.mappings().first()
        return dict(location) if location else None