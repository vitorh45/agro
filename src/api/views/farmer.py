from flask import Blueprint, request
from flask_restx import Api, Resource, marshal, marshal_with
from werkzeug.exceptions import Unauthorized
from marshmallow import ValidationError

from .schemas import (
    farmer_create_request_model,
    farmer_create_response_model,
    farmer_update_request_model,
    farmer_query_args_parser,
    farmers_query_args_parser,
    generic_response_model,
    FarmerCreateRequestSchema,
    FarmerUpdateRequestSchema
)
from api.domain.entities.farmer import Farmer, FarmerNotFound, FarmerAlreadyRegistered
from api.domain.repositories.farmer_repository import SQLAlchemyFarmerRepository


VERSION = "0.0.1"
DOC = "Agro API"

blueprint = Blueprint("farmer", __name__, url_prefix="/api/v1")

api = Api(
    blueprint,
    version=VERSION,
    title="Agro API",
    description=f"{DOC} - Agro",
    doc="/docs/swagger"
)

ns = api.namespace("", description=DOC)


@ns.route("/farmers")
class Farmers(Resource):
    @ns.expect(farmers_query_args_parser)
    @ns.response(201, "OK", farmer_create_response_model)
    def get(self) -> tuple[dict, int]:
        query_args = farmers_query_args_parser.parse_args()
        limit = query_args.get("limit", 20)
        offset = query_args.get("offset", 0)
        try:
            farmers = Farmer.get_all(
                limit=limit,
                offset=offset,
                repository=SQLAlchemyFarmerRepository)
        except Exception as e:
            return {"message": str(e)}, 400

        return marshal(farmers, farmer_create_response_model), 200

    @ns.expect(farmer_create_request_model)
    @ns.response(201, "OK", farmer_create_response_model)
    def post(self) -> tuple[dict, int]:
        try:
            validated_data = FarmerCreateRequestSchema().load(api.payload)
        except ValidationError as err:
            return {'message': str(err)}, 400

        try:
            farmer = Farmer.create(
                data=validated_data,
                repository=SQLAlchemyFarmerRepository)
        except Exception as e:
            return {"message": str(e)}, 400

        return marshal(farmer, farmer_create_response_model), 201

    @ns.expect(farmer_query_args_parser)
    @ns.response(200, "OK", generic_response_model)
    def delete(self) -> tuple[dict, int]:
        query_args = farmer_query_args_parser.parse_args()
        try:
            farmer = Farmer.delete(
                cpf_cnpj=query_args["cpf_cnpj"],
                repository=SQLAlchemyFarmerRepository)
        except FarmerNotFound as e:
            return {"message": str(e)}, 404
        except Exception as e:
            return {"message": str(e)}, 400
        return {"message": "OK"}, 200

    @ns.expect(farmer_update_request_model, farmer_query_args_parser)
    @ns.response(200, "OK", generic_response_model)
    def patch(self) -> tuple[dict, int]:
        query_args = farmer_query_args_parser.parse_args()
        try:
            validated_data = FarmerUpdateRequestSchema().load(api.payload)
        except ValidationError as err:
            return {'message': str(err)}, 400

        try:
            farmer = Farmer.update(
                cpf_cnpj=query_args["cpf_cnpj"],
                data=validated_data,
                repository=SQLAlchemyFarmerRepository)
        except FarmerNotFound as e:
            return {
                "message": str(e)
            }, 404
        except Exception as e:
            return {
                "message": str(e)
            }, 400
        return marshal(farmer, farmer_create_response_model), 200


