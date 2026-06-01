"""
Address entity — ORM mapped class for table `Address`.
"""

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity
from models.employee import Employee


class Address(Entity):
    __tablename__ = "addresses"

    line1: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(25), nullable=True)
    country: Mapped[str] = mapped_column(String(50), nullable=True)
    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    employees: Mapped["Employee"] = relationship("Employee", back_populates="addresses")
