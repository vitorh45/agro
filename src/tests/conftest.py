import pytest
from datetime import datetime
from copy import deepcopy

from api.app import create_app, db
from api.infrastructure.database.models import Farmer as FarmerTable
from api.domain.repositories.farmer_repository import FarmerRepository


@pytest.fixture(scope="package")
def app():
    app = create_app("Testing")
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        yield client


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    db.session.rollback()

def pytest_addoption(parser):
    parser.addoption("--skip-startfinish", default=False, action="store_true")


@pytest.fixture
def skip_startfinish(request):
    return request.config.getoption("--skip-startfinish")


def pytest_sessionstart(session):
    from sqlalchemy import text, exc

    if session.config.getoption("--skip-startfinish"):
        return

    app = create_app("Testing")
    app.config["TESTING"] = True

    with app.app_context():
        db.metadata.bind = db.engine
        try:
            db.session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        except exc.OperationalError:
            session.db_connected = False
        else:
            session.db_connected = True
            db.session.commit()
            db.create_all()


def pytest_sessionfinish(session):
    if session.config.getoption("--skip-startfinish") or not session.db_connected:
        return

    app = create_app("Testing")
    with app.app_context():
        db.metadata.bind = db.engine
        db.drop_all()


@pytest.fixture()
def create_farmer_cpf_dict():
    return {
        "cpf_cnpj": "42063478082",
        "name": "Fazendeiro 123",
        "farm_name": "Fazenda LOTR",
        "city": "Joao Pessoa",
        "state": "PB",
        "total_area": 100,
        "agricultural_area": 40,
        "vegetation_area": 50,
        "farming_options": ["SUGARCANE"]
    }


@pytest.fixture()
def create_farmer_cpf_dict_2():
    return {
        "cpf_cnpj": "28375661015",
        "name": "Fazendeiro 123",
        "farm_name": "Fazenda LOTR",
        "city": "Joao Pessoa",
        "state": "PB",
        "total_area": 100,
        "agricultural_area": 40,
        "vegetation_area": 50,
        "farming_options": ["SUGARCANE"]
    }


@pytest.fixture()
def create_farmer_cnpj_dict():
    return {
        "cpf_cnpj": "98877409000195",
        "name": "Fazendeiro 123",
        "farm_name": "Fazenda LOTR",
        "city": "Joao Pessoa",
        "state": "PB",
        "total_area": 100,
        "agricultural_area": 40,
        "vegetation_area": 50,
        "farming_options": ["SUGARCANE"]
    }


@pytest.fixture()
def update_farmer_cpf_dict(create_farmer_cpf_dict):
    update_dict = deepcopy(create_farmer_cpf_dict)
    update_dict.pop("cpf_cnpj")
    return update_dict


@pytest.fixture()
def return_farmer_cpf_model(create_farmer_cpf_dict):
    create_farmer_cpf_dict_full = deepcopy(create_farmer_cpf_dict)
    create_farmer_cpf_dict_full.update({
        "insert_at": datetime(2024, 10, 21, 0, 0, 0),
        "update_at": datetime(2024, 10, 21, 0, 0, 0),
    })
    return FarmerTable(**create_farmer_cpf_dict_full)


@pytest.fixture()
def return_farmer_cpf_model_2(create_farmer_cpf_dict_2):
    create_farmer_cpf_dict_2_full = deepcopy(create_farmer_cpf_dict_2)
    create_farmer_cpf_dict_2_full.update({
        "insert_at": datetime(2024, 10, 21, 0, 0, 0),
        "update_at": datetime(2024, 10, 21, 0, 0, 0),
    })
    return FarmerTable(**create_farmer_cpf_dict_2_full)


@pytest.fixture()
def return_farmer_cnpj_model(create_farmer_cnpj_dict):
    create_farmer_cnpj_dict_full = deepcopy(create_farmer_cnpj_dict)
    create_farmer_cnpj_dict_full.update({
        "insert_at": datetime(2024, 10, 21, 0, 0, 0),
        "update_at": datetime(2024, 10, 21, 0, 0, 0),
    })
    return FarmerTable(**create_farmer_cnpj_dict_full)
