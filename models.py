from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from db import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(Date, nullable=False)
    location = Column(String(200), nullable=False)
    max_capacity = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "max_capacity > 0",
            name="check_positive_capacity"
        ),
    )


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer,
        ForeignKey("events.id"),
        nullable=False
    )

    employee_name = Column(String(100), nullable=False)
    employee_email = Column(String(150), nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "event_id",
            "employee_email",
            name="unique_employee_per_event"
        ),
    )