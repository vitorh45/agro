import mock
import pytest
from datetime import datetime

from api.domain.repositories.farmer_repository import SQLAlchemyFarmerRepository
from api.domain.entities.farmer import Farmer, FarmerAreaInvalid, FarmerAlreadyRegistered, FarmerNotFound


@mock.patch.object(SQLAlchemyFarmerRepository, "get_all")
def test_get_all_success(get_all_mock, create_farmer_cpf_dict, return_farmer_cpf_model, app):
    create_farmer_mock.return_value = return_farmer_cpf_model

    farmer = Farmer.create(data=create_farmer_cpf_dict, repository=SQLAlchemyFarmerRepository)

    assert farmer.name == create_farmer_cpf_dict["name"]
    create_farmer_mock.assert_called_once_with(create_farmer_cpf_dict)
    
    
@mock.patch.object(SQLAlchemyFarmerRepository, "create")
def test_create_farmer_cpf_success(create_farmer_mock, create_farmer_cpf_dict, return_farmer_cpf_model, app):
    create_farmer_mock.return_value = return_farmer_cpf_model

    farmer = Farmer.create(data=create_farmer_cpf_dict, repository=SQLAlchemyFarmerRepository)

    assert farmer.name == create_farmer_cpf_dict["name"]
    create_farmer_mock.assert_called_once_with(create_farmer_cpf_dict)


@mock.patch.object(SQLAlchemyFarmerRepository, "create")
def test_create_farmer_cnpj_success(create_farmer_mock, create_farmer_cnpj_dict, return_farmer_cnpj_model, app):
    create_farmer_mock.return_value = return_farmer_cnpj_model

    farmer = Farmer.create(data=create_farmer_cnpj_dict, repository=SQLAlchemyFarmerRepository)

    assert farmer.name == create_farmer_cnpj_dict["name"]
    create_farmer_mock.assert_called_once_with(create_farmer_cnpj_dict)


@mock.patch.object(SQLAlchemyFarmerRepository, "delete")
def test_delete_farmer_cpf_success(delete_farmer_mock, app):
    farmer = Farmer.delete(cpf_cnpj="00100200304", repository=SQLAlchemyFarmerRepository)
    delete_farmer_mock.assert_called_once_with("00100200304")
    

@mock.patch.object(SQLAlchemyFarmerRepository, "get_by_cpf_cnpj")
@mock.patch.object(SQLAlchemyFarmerRepository, "update")
def test_update_farmer_success(update_farmer_mock,
                               get_by_cpf_cnpj_mock,
                               update_farmer_cpf_dict,
                               return_farmer_cpf_model,
                               app):
    update_farmer_mock.return_value = return_farmer_cpf_model
    get_by_cpf_cnpj_mock.return_value = return_farmer_cpf_model
    
    farmer = Farmer.update(cpf_cnpj="42063478082", data=update_farmer_cpf_dict, repository=SQLAlchemyFarmerRepository)
    
    update_farmer_mock.assert_called_once_with(farmer=return_farmer_cpf_model, data=update_farmer_cpf_dict)
    get_by_cpf_cnpj_mock.assert_called_once_with("42063478082")


@mock.patch.object(SQLAlchemyFarmerRepository, "get_by_cpf_cnpj")
@mock.patch.object(SQLAlchemyFarmerRepository, "update")
def test_update_farmer_error(update_farmer_mock,
                             get_by_cpf_cnpj_mock,
                             update_farmer_cpf_dict,
                             return_farmer_cpf_model,
                             app):
    get_by_cpf_cnpj_mock.return_value = return_farmer_cpf_model
    update_farmer_cpf_dict["agricultural_area"] = 100
    
    with pytest.raises(FarmerAreaInvalid) as e:
        Farmer.update(cpf_cnpj="42063478082", data=update_farmer_cpf_dict, repository=SQLAlchemyFarmerRepository)
    
    update_farmer_mock.assert_not_called()
    get_by_cpf_cnpj_mock.assert_called_once_with("42063478082")
    assert str(e.value) == "Agricultural area 100 plus vegetation area 50 cannot be greater than total area 100"
