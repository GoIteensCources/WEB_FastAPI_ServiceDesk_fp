import datetime as dt
from enum import Enum

from sqlalchemy import Boolean, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from settings import Base


class RequestStatus(str, Enum):
    NEW = "Нова"
    IN_PROGRESS = "В обробці"
    MESSAGE = "Повідомлення"
    COMPLETED = "Завершено"
    CANCELLED = "Скасовано"


# Модель Note
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(
        String(100), nullable=False
    )  # Зберігаємо хеш пароля

    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    repair_requests: Mapped[list["RepairRequest"]] = relationship(
        "RepairRequest", backref="user", lazy="selectin"
    )
    assigned_repairs: Mapped[list["RepairRequest"]] = relationship(
        "RepairRequest", backref="admin", lazy="selectin"
    )

    admin_messages: Mapped[list["AdminMessage"]] = relationship(
        "AdminMessage", backref="admin", lazy="selectin"
    )

    def __str__(self):
        return f"<User> з {self.id} та {self.username}"


class RepairRequest(Base):
    __tablename__ = "repair_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    photo_url: Mapped[str] = mapped_column(String(255), nullable=True)

    required_time: Mapped[dt.datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(RequestStatus), default=RequestStatus.NEW.value
    )

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[dt.datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User"] = relationship(
        "User", backref="repair_requests", foreign_keys=[user_id], lazy="selectin"
    )

    admin: Mapped["User"] = relationship(
        "User", backref="assigned_repairs", foreign_keys=[admin_id], lazy="selectin"
    )

    messages: Mapped[list["AdminMessage"]] = relationship(
        "AdminMessage", backref="repair_request", lazy="selectin"
    )

    def __str__(self):
        return f"<RepairRequest> з {self.id} та статусом {self.status}"


class AdminMessage(Base):
    __tablename__ = "admin_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )

    request_id: Mapped[int] = mapped_column(
        ForeignKey("repair_requests.id"), nullable=False
    )
    admin_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # зв’язки
    to_repair_request: Mapped["RepairRequest"] = relationship(
        "RepairRequest", back_populates="messages"
    )
    admin: Mapped["User"] = relationship("User", back_populates="admin_messages")


class Rewiews(Base):
    __tablename__ = "rewiews"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[dt.datetime] = mapped_column(DateTime, default=func.now())
