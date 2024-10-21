from typing import List
from datetime import datetime
from enum import Enum

from api.app import db
from sqlalchemy import Column


class FarmingOptions(Enum):
    SOY = "Soja"
    CORN = "Milho"
    COFFEE = "Café"
    COTTON = "Algodão"
    SUGARCANE = "Cana de açúcar"
    
    @classmethod
    def get(cls, option) -> Enum:
        return cls.__members__.get(option)
    
    @classmethod
    def get_all_values(cls) -> List[str]:
        return [item.name for item in list(cls)]


class Farmer(db.Model):
    __tablename__ = "farmer"

    cpf_cnpj = Column(db.String(15), nullable=False, primary_key=True)
    name = Column(db.String(200), nullable=False)
    farm_name = Column(db.String(200), nullable=False)
    city = Column(db.String(200), nullable=False)
    state = Column(db.String(2), nullable=False)
    total_area = Column(db.Integer, nullable=False)
    agricultural_area = Column(db.Integer, nullable=False)
    vegetation_area = Column(db.Integer, nullable=False)
    farming_options = Column(db.JSON, nullable=True)
    insert_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_at = Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    def __repr__(self) -> str:
        return f"<Farmer {self.cpf_cnpj}|{self.name}|{self.farm_name}>"