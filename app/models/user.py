import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database import Base


class UserRole(str, enum.Enum):
    STUDENT = "student"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        Enum(
            UserRole,
            name="userrole",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        nullable=False,
        default=UserRole.STUDENT,
    )

    hostel_block = Column(
        String(50),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )