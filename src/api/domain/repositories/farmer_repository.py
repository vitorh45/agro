from abc import ABC
import logging
from typing import Union, Optional
from sqlalchemy.exc import IntegrityError

from api.app import db
from api.infrastructure.database.models import Farmer as FarmerTable

logger = logging.getLogger("agro")


class FarmerRepository(ABC):
    @classmethod
    def create(cls, data: dict) -> "Farmer":
        raise NotImplementedError

    @classmethod
    def update(cls, cpf_cnpj: str, data: dict) -> "User":
        raise NotImplementedError

    @classmethod
    def delete(cls, cpf_cnpj: str) -> "Farmer":
        raise NotImplementedError
    
    @classmethod
    def get_by_cpf_cnpj(cls, cpf_cnpj: str) -> "Farmer":
        raise NotImplementedError


class SQLAlchemyFarmerRepository(FarmerRepository):
    @staticmethod
    def _build_farmer(farmer) -> "Farmer":
        from api.domain.entities.farmer import Farmer
        return Farmer(
            cpf_cnpj=farmer.cpf_cnpj,
            name=farmer.name,
            farm_name=farmer.farm_name,
            city=farmer.city,
            state=farmer.state,
            total_area=farmer.total_area,
            agricultural_area=farmer.agricultural_area,
            vegetation_area=farmer.vegetation_area,
            farming_options=farmer.farming_options,
            insert_at=farmer.insert_at,
            update_at=farmer.update_at,
        )

    @classmethod
    def create(
        cls,
        data: dict
    ) -> "Farmer":
        from api.domain.entities.farmer import FarmerAlreadyRegistered
        logger.info(
            "Creating farmer.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "create",
                    "data": data
                }
            },
        )
        try:
            farmer = FarmerTable(**data)
            db.session.add(farmer)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to create farmer. Integrity error.",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "create",
                        "data": data,
                        "error": str(e)
                    }
                },
            )

            raise FarmerAlreadyRegistered("Farmer already registered")
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to create farmer",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "create",
                        "data": data,
                        "error": str(e)
                    }
                },
            )
            raise e

        return farmer

    @classmethod
    def delete(
        cls,
        cpf_cnpj: str
    ) -> "Farmer":
        from api.domain.entities.farmer import FarmerNotFound
        logger.info(
            "Deleting farmer.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "delete",
                    "cpf_cnpj": cpf_cnpj
                }
            },
        )
        try:
            farmer = FarmerTable.query.filter_by(cpf_cnpj=cpf_cnpj).first()
            if farmer:
                db.session.delete(farmer)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to create farmer",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "create",
                        "data": data
                    }
                },
            )
            raise e
        if not farmer:
            raise FarmerNotFound("Farmer not found.")
        return None
    
    @classmethod
    def get_by_cpf_cnpj(
        cls,
        cpf_cnpj: str
    ) -> "Farmer":
        from api.domain.entities.farmer import FarmerNotFound
        logger.info(
            "Getting farmer by cpf_cnpj.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_by_cpf_cnpj",
                    "cpf_cnpj": cpf_cnpj
                }
            },
        )
        try:
            farmer = FarmerTable.query.filter_by(cpf_cnpj=cpf_cnpj).first()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to get farmer by cpf_cnpj",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_by_cpf_cnpj",
                        "cpf_cnpj": cpf_cnpj,
                        "error": str(e)
                    }
                },
            )
            raise e
        if not farmer:
            raise FarmerNotFound("Farmer not found.")
        return farmer

    @classmethod
    def update(
        cls,
        farmer: "Farmer",
        data: dict
    ) -> "Farmer":
        logger.info(
            "Updateing farmer.",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "update",
                    "data": data,
                    "cpf_cnpj": farmer.cpf_cnpj
                }
            },
        )
        try:
            for field_name, new_value in data.items():
                setattr(farmer, field_name, new_value)
            db.session.add(farmer)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to create farmer",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "update",
                        "data": data,
                        "cpf_cnpj": farmer.cpf_cnpj,
                        "error": str(e)
                    }
                },
            )
            raise e

        return farmer

    @classmethod
    def get_all(
        cls,
        limit: int,
        offset: int
    ) -> "Farmer":
        logger.info(
            "Getting farmers",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service_method": "get_all",
                    "limit": limit,
                    "offset": offset
                }
            },
        )
        try:
            farmers = FarmerTable.query.limit(limit).offset(offset).all()
        except Exception as e:
            db.session.rollback()
            logger.exception(
                "Error while trying to get farmers",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service_method": "get_all",
                        "limit": limit,
                        "offset": offset,
                        "error": str(e)
                    }
                },
            )
            raise e

        return farmers