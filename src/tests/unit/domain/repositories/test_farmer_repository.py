import mock
import pytest
from api.infrastructure.database.models import Farmer as FarmerTable
from api.domain.repositories.farmer_repository import SQLAlchemyFarmerRepository
from api.domain.entities.farmer import FarmerAlreadyRegistered, FarmerNotFound


def test_farmer_create_success(create_farmer_cpf_dict, app):
    SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    
    assert FarmerTable.query.filter_by(cpf_cnpj=create_farmer_cpf_dict["cpf_cnpj"]).count() == 1


def test_farmer_create_duplicated_error(create_farmer_cpf_dict, app):
    create_farmer_cpf_dict["cpf_cnpj"] = "00100200304"
    SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    
    with pytest.raises(FarmerAlreadyRegistered) as e:
        SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)

    assert FarmerTable.query.filter_by(cpf_cnpj=create_farmer_cpf_dict["cpf_cnpj"]).count() == 1
    assert str(e.value) == "Farmer already registered"


def test_farmer_delete_success(create_farmer_cpf_dict, app):
    create_farmer_cpf_dict["cpf_cnpj"] = "00100200305"
    SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    SQLAlchemyFarmerRepository.delete(cpf_cnpj="00100200305")

    assert FarmerTable.query.filter_by(cpf_cnpj=create_farmer_cpf_dict["cpf_cnpj"]).count() == 0


def test_farmer_delete_error_not_found(create_farmer_cpf_dict, app):
    create_farmer_cpf_dict["cpf_cnpj"] = "00100200305"
    SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    
    with pytest.raises(FarmerNotFound) as e:
        SQLAlchemyFarmerRepository.delete(cpf_cnpj="00100200306")

    assert FarmerTable.query.filter_by(cpf_cnpj=create_farmer_cpf_dict["cpf_cnpj"]).count() == 1
    assert str(e.value) == "Farmer not found."


def test_farmer_get_by_cpf_cnpj_success(create_farmer_cpf_dict, app):
    create_farmer_cpf_dict["cpf_cnpj"] = "00100200306"
    SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    farmer = SQLAlchemyFarmerRepository.get_by_cpf_cnpj(cpf_cnpj="00100200306")

    assert farmer.cpf_cnpj == "00100200306"


def test_farmer_get_by_cpf_cnpj_error_not_found(create_farmer_cpf_dict, app):
    create_farmer_cpf_dict["cpf_cnpj"] = "00100200307"
    SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    
    with pytest.raises(FarmerNotFound) as e:
        SQLAlchemyFarmerRepository.get_by_cpf_cnpj(cpf_cnpj="00100200308")

    assert str(e.value) == "Farmer not found."


def test_farmer_update_success(create_farmer_cpf_dict, app):
    create_farmer_cpf_dict["cpf_cnpj"] = "00100200308"
    update_data = {"name": "Farm name updated 123"}
    farmer = SQLAlchemyFarmerRepository.create(data=create_farmer_cpf_dict)
    farmer_updated = SQLAlchemyFarmerRepository.update(farmer=farmer, data=update_data)
    
    assert farmer_updated.name == "Farm name updated 123"
