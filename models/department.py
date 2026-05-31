"""
Department entity — ORM mapped class for table `Department`.
"""

from sqlalchemy import DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,  relationship

from models.entity import Entity
from models.employee import Employee

class Address(Entity):
    __tablename__ = "departments"

    id: int
    name: str

