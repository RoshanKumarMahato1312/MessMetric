import enum

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from app.database import Base


class MealType(str, enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    SNACKS = "snacks"
    DINNER = "dinner"


class Menu(Base):
    __tablename__ = "menu"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    date = Column(
        Date,
        nullable=False,
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

    dish_names = Column(
        ARRAY(Text),
        nullable=False,
    )

    created_by = Column(
        ForeignKey("users.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "date",
            "meal_type",
            name="uq_menu_date_meal_type",
        ),
    )