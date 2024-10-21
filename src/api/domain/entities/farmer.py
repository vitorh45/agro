import logging
from typing import List
from dataclasses import dataclass
from datetime import datetime

from api.domain.repositories.farmer_repository import FarmerRepository


class FarmerNotFound(Exception):
    pass


class FarmerAlreadyRegistered(Exception):
    pass


class FarmerAreaInvalid(Exception):
    pass


@dataclass
class Farmer:
    cpf_cnpj: str
    name: str
    farm_name: str
    city: str
    state: str
    total_area: int
    agricultural_area: int
    vegetation_area: int
    farming_options: List[str]
    update_at: datetime
    insert_at: datetime

    @classmethod
    def get_all(cls, limit: int, offset: int, repository: FarmerRepository):
        return repository.get_all(limit=limit, offset=offset)

    @classmethod
    def create(cls, data: dict, repository: FarmerRepository):
        return repository.create(data)

    @classmethod
    def delete(cls, cpf_cnpj: str, repository: FarmerRepository):
        return repository.delete(cpf_cnpj)
    
    @classmethod
    def update(cls, cpf_cnpj: str, data: dict, repository: FarmerRepository):
        farmer = repository.get_by_cpf_cnpj(cpf_cnpj)
        cls.validate_total_area(data.get("total_area", farmer.total_area),
                            data.get("agricultural_area", farmer.agricultural_area),
                            data.get("vegetation_area", farmer.vegetation_area))
        cls.adjust_farming_options(farmer, data.get("farming_options"))
        return repository.update(farmer=farmer, data=data)
    
    @staticmethod
    def validate_total_area(total_area, agricultural_area, vegetation_area):
        if agricultural_area + vegetation_area > total_area:
            raise FarmerAreaInvalid(f"Agricultural area {agricultural_area} plus "+ 
                                    f"vegetation area {vegetation_area} cannot be "+
                                    f"greater than total area {total_area}")
    
    @staticmethod
    def adjust_farming_options(farmer, new_farming_options):
        if new_farming_options:
            temp_options = farmer.farming_options
            temp_options.extend(new_farming_options)
            new_farming_options = list(set(temp_options))
