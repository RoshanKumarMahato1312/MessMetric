import enum

from app.models.menu import MealType
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    Float,
    Integer,
    JSON,
    String,
)
from sqlalchemy.sql import func

from app.database import Base


class EscalationStatus(str, enum.Enum):
    PENDING = "pending"
    EMAIL_SENT = "email_sent"
    RESOLVED = "resolved"
    RE_ESCALATED = "re_escalated"


class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    meal_type = Column(
        Enum(
            MealType,
            name="mealtype",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        nullable=False,
    )

    date_range_start = Column(
        Date,
        nullable=False,
    )

    date_range_end = Column(
        Date,
        nullable=False,
    )

    dissatisfaction_ratio = Column(
        Float,
        nullable=False,
    )

    top_tags = Column(
        JSON,
        nullable=True,
    )

    status = Column(
        Enum(
            EscalationStatus,
            name="escalationstatus",
            values_callable=lambda enum_class: [
                member.value for member in enum_class
            ],
        ),
        nullable=False,
        default=EscalationStatus.PENDING,
    )

    pdf_report_url = Column(
        String(255),
        nullable=True,
    )

    email_sent_at = Column(
        DateTime,
        nullable=True,
    )

    resolved_at = Column(
        DateTime,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )