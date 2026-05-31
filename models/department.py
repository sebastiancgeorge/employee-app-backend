"""
Department entity — ORM mapped class for table `departments`.
"""

from typing import Any, TYPE_CHECKING
from sqlalchemy import Column, Integer, ForeignKey, Table, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.entity import Entity

if TYPE_CHECKING:
    from models.employee import Employee

employee_departments = Table("employee_departments", Entity.metadata,
    Column("employee_id", Integer, ForeignKey("employees.id", ondelete="CASCADE"), primary_key=True),
    Column("department_id", Integer, ForeignKey("departments.id", ondelete="CASCADE"), primary_key=True))

class Department(Entity):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer,autoincrement=True,primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    employees: Mapped[list["Employee"]] = relationship("Employee", secondary= "employee_departments",back_populates="departments")