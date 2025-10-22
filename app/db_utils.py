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
                'SELECT id, email, "passwordHash", "userType" as role, status FROM users WHERE email = :email'
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


async def create_user(
    email: str,
    password: str,
    role: Literal["shipper", "carrier"],
    full_name: str,
    phone: str,
    company_name: str | None = None,
    license_number: str | None = None,
    vehicle_type: str | None = None,
) -> str:
    """Creates a new user in the database."""
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    hashed_password = hash_password(password)
    user_id = str(uuid.uuid4())
    async with rx.asession() as session:
        await session.execute(
            text(
                'INSERT INTO users (id, email, "passwordHash", "userType", status, "firstName", "lastName", phone, "companyName", "nationalId", "taxId") VALUES (:id, :email, :password_hash, :user_type, :status, :first_name, :last_name, :phone, :company_name, :national_id, :tax_id)'
            ),
            {
                "id": user_id,
                "email": email,
                "password_hash": hashed_password,
                "user_type": role.upper(),
                "status": "ACTIVE",
                "first_name": full_name,
                "last_name": "",
                "phone": phone,
                "company_name": company_name,
                "national_id": license_number,
                "tax_id": license_number,
            },
        )
        await session.commit()
    return user_id