import mock
import pytest
from flask import request


from api.domain.entities.farmer import Farmer, FarmerNotFound, FarmerAlreadyRegistered
from api.domain.repositories.farmer_repository import SQLAlchemyFarmerRepository


@mock.patch.object(Farmer, "create")
def test_create_success(create_mock, create_farmer_cpf_dict, return_farmer_cpf_model, app):
    
    create_mock.return_value = return_farmer_cpf_model
    response = app.post(
        "/api/v1/farmers",
        json=create_farmer_cpf_dict
    )

    assert response.json["cpf_cnpj"] == return_farmer_cpf_model.cpf_cnpj
    assert response.status_code == 201
    create_mock.assert_called_once_with(data=create_farmer_cpf_dict, repository=SQLAlchemyFarmerRepository)


@mock.patch.object(Farmer, "create")
def test_create_error_invalid_data(create_mock, create_farmer_cpf_dict, app):
    
    create_farmer_cpf_dict["state"] = "PBB"
    response = app.post(
        "/api/v1/farmers",
        json=create_farmer_cpf_dict
    )

    assert response.json == {'message': "{'state': ['Length must be between 2 and 2.']}"}
    assert response.status_code == 400
    create_mock.assert_not_called()


@mock.patch.object(Farmer, "create")
def test_create_error_duplicated_farmer(create_mock, create_farmer_cpf_dict, app):
    
    create_mock.side_effect = FarmerAlreadyRegistered("Farmer already registered")
    response = app.post(
        "/api/v1/farmers",
        json=create_farmer_cpf_dict
    )

    assert response.json == {"message": "Farmer already registered"}
    assert response.status_code == 400


@mock.patch.object(Farmer, "delete")
def test_delete_success(delete_mock, app):

    response = app.delete(
        "/api/v1/farmers?cpf_cnpj=00100200304",
    )

    assert response.json == {"message": "OK"}
    assert response.status_code == 200
    delete_mock.assert_called_once_with(cpf_cnpj="00100200304", repository=SQLAlchemyFarmerRepository)


@mock.patch.object(Farmer, "delete")
def test_delete_farmer_not_found(delete_mock, app):

    delete_mock.side_effect = FarmerNotFound("Farmer not found")
    response = app.delete(
        "/api/v1/farmers?cpf_cnpj=00100200304",
    )

    assert response.json == {"message": "Farmer not found"}
    assert response.status_code == 404
    delete_mock.assert_called_once_with(cpf_cnpj="00100200304", repository=SQLAlchemyFarmerRepository)


@mock.patch.object(Farmer, "delete")
def test_delete_farmer_url_param_missing(delete_mock, app):

    delete_mock.side_effect = FarmerNotFound("Farmer not found")
    response = app.delete(
        "/api/v1/farmers",
    )

    assert response.json == {'errors': {'cpf_cnpj': 'Missing required parameter in the query string'},
                             'message': 'Input payload validation failed'}
    assert response.status_code == 400
    delete_mock.assert_not_called()


@mock.patch.object(Farmer, "update")
def test_update_success(update_mock, update_farmer_cpf_dict, return_farmer_cpf_model, app):
    
    update_mock.return_value = return_farmer_cpf_model
    response = app.patch(
        "/api/v1/farmers?cpf_cnpj=00100200304",
        json=update_farmer_cpf_dict
    )

    assert response.json["cpf_cnpj"] == return_farmer_cpf_model.cpf_cnpj
    assert response.status_code == 200
    update_mock.assert_called_once_with(cpf_cnpj="00100200304", data=update_farmer_cpf_dict,
                                        repository=SQLAlchemyFarmerRepository)


@mock.patch.object(Farmer, "update")
def test_update_farmer_not_found(update_mock, update_farmer_cpf_dict, return_farmer_cpf_model, app):
    
    update_mock.side_effect = FarmerNotFound("Farmer not found")
    response = app.patch(
        "/api/v1/farmers?cpf_cnpj=00100200304",
        json=update_farmer_cpf_dict
    )

    assert response.json == {"message": "Farmer not found"}
    assert response.status_code == 404
    update_mock.assert_called_once_with(cpf_cnpj="00100200304", data=update_farmer_cpf_dict,
                                        repository=SQLAlchemyFarmerRepository)


@mock.patch.object(Farmer, "update")
def test_update_farmer_url_param_missing(update_mock, app):

    response = app.patch(
        "/api/v1/farmers",
    )

    assert response.json == {'errors': {'cpf_cnpj': 'Missing required parameter in the query string'},
                             'message': 'Input payload validation failed'}
    assert response.status_code == 400
    update_mock.assert_not_called()