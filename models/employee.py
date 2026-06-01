"""
Employee entity — ORM mapped class for table `employees`.
"""

from typing import TYPE_CHECKING
import enum
from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from models.entity import Entity

if TYPE_CHECKING:
    from models.address import Address 
    from models.department import Department, employee_departments

class EmployeeRole(str, enum.Enum):
    UI = "UI",
    UX = "UX",
    DEVELOPER = "DEVOLOPER"
    HR = "HR"

class Employee(Entity):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255),nullable= False)

    addresses: Mapped[list["Address"]] = relationship("Address", back_populates= "employees")
    departments: Mapped[list["Department"]] = relationship("Department", secondary= "employee_departments", back_populates="employees")
    role : Mapped[EmployeeRole] = mapped_column(Enum(EmployeeRole, name="employeerole",values_callable=lambda enum_cls: [e.value for e in enum_cls]), nullable= False, server_default = EmployeeRole.DEVELOPER.value)