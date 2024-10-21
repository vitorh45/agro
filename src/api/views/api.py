from flask import Blueprint, request
from flask_restx import Api, Resource

from .schemas import (
    index_model,
    farmer_create_request_model,
    farmer_create_response_model,
    farmer_update_request_model,
    generic_response_model
)
from .farmer import Farmers

VERSION = "0.0.1"
DOC = "Agro API"

blueprint = Blueprint("index", __name__)

api = Api(
    blueprint,
    version=VERSION,
    title="Agro Index API",
    description=f"{DOC} - Index",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)

ns.add_model(index_model.name, index_model)
ns.add_model(farmer_create_request_model.name, farmer_create_request_model)
ns.add_model(farmer_create_response_model.name, farmer_create_response_model)
ns.add_model(farmer_update_request_model.name, farmer_update_request_model)
ns.add_model(generic_response_model.name, generic_response_model)


ns.add_resource(Farmers, "/farmers")


@ns.route("/health")
class Index(Resource):
    @ns.response(200, "OK", index_model)
    def get(self) -> tuple[dict, int]:
        return dict(
            service=DOC,
            version=VERSION
        ), 200
