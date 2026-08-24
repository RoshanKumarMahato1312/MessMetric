from sqlalchemy import (
    Column,
    Integer,
    SmallInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.sql import func

from app.database import Base


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    student_id = Column(
        ForeignKey("users.id"),
        nullable=False
    )

    menu_id = Column(
        ForeignKey("menu.id"),
        nullable=False
    )

    rating = Column(
        SmallInteger,
        nullable=False
    )

    tags = Column(
        ARRAY(Text),
        nullable=True
    )

    comment = Column(
        Text,
        nullable=True
    )

    is_anonymous = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "menu_id",
            name="uq_rating_student_menu"
        ),
    )