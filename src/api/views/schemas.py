from flask_restx import fields, Model, reqparse
from validate_docbr import CPF, CNPJ
import marshmallow as ma


farmer_query_args_parser = reqparse.RequestParser()
farmer_query_args_parser.add_argument(
    "cpf_cnpj",
    type=str,
    location="args",
    required=True,
    nullable=False,
)

farmers_query_args_parser = reqparse.RequestParser()
farmers_query_args_parser.add_argument(
    "limit",
    type=str,
    location="args",
    required=False,
    nullable=False,
)
farmers_query_args_parser.add_argument(
    "offset",
    type=str,
    location="args",
    required=False,
    nullable=False,
)

index_model = Model(
    "Health-Status",
    {
        "service": fields.String(
            description="Service name"
        ),
        "version": fields.String(
            description="API version"
        )
    }
)


generic_response_model = Model(
    "GenericResponse",
    {
        "message": fields.String(example="Generic message")
    }
)


class CustomJsonField(fields.Raw):
    __schema_type__ = ["array"]
    __schema_example__ = "list"

    def format(self, value):        
        if isinstance(value, list):
            return value
        else:
            raise fields.MarshallingError(
                "Invalid type. Allowed type is list."
            )


### CREATE FARMER
class FarmerCreateRequestSchema(ma.Schema):
    cpf_cnpj = ma.fields.String(
        description="CPF or CNPJ",
        example="00100200304|XXXXXXXX0001XX",
        required=True
    )
    name = ma.fields.String(
        description="Name",
        example="Aragorn",
        required=True
    )
    farm_name = ma.fields.String(
        description="Farm name",
        example="Fazenda LOTR",
        required=True
    )
    city = ma.fields.String(
        description="City name",
        example="Joao Pessoa",
        required=True
    )
    state = ma.fields.String(
        description="State",
        example="SP|PB|PE",
        required=True,
        validate=ma.validate.Length(min=2, max=2)
    )
    total_area = ma.fields.Integer(
        description="Total farm area in hectares",
        example="100",
        required=True
    )
    agricultural_area = ma.fields.Integer(
        description="Agricultural area in hectares",
        example="30",
        required=True
    )
    vegetation_area = ma.fields.Integer(
        description="Vegetation area in hectares",
        example="20",
        required=True
    )
    farming_options = ma.fields.List(
        ma.fields.String(),
        description="Farming options",
        example=["SOY", "CORN"],
        required=True
    )
    
    class Meta:
        unknown = ma.EXCLUDE

    @ma.validates_schema
    def validate_total_area(self, data, **kwargs):
        if data["agricultural_area"] + data["vegetation_area"] > data["total_area"]:
            raise ma.ValidationError(f"Agricultural area {data['agricultural_area']} "+
                                  f"plus vegetation area {data['vegetation_area']} "+
                                  f"cannot be greater than total area {data['total_area']}")

    @ma.validates('farming_options')
    def validate_farming_options(self, value):
        from api.infrastructure.database.models import FarmingOptions
        for option in value:
            if not FarmingOptions.get(option):
                raise ma.ValidationError(f"Wrong farming options value. The options are {FarmingOptions.get_all_values()}")
        return value
    
    @ma.validates('cpf_cnpj')
    def validate_cpf_cnpj(self, value):
        validator = CPF() if len(value) == 11 else CNPJ()
        if not validator.validate(value):
            raise ma.ValidationError("Wrong value for CPF or CNPJ")


farmer_create_request_model = Model(
    "Farmer create request",
    {
        "cpf_cnpj": fields.String(
            description="cpf or cnpj",
            example="00100200304|XXXXXXXX0001XX",
            required=True
        ),
        "name": fields.String(
            description="Name",
            example="Aragorn",
            required=True
        ),
        "farm_name": fields.String(
            description="Farm name",
            example="Fazenda LOTR",
            required=True
        ),
        "city": fields.String(
            description="City name",
            example="Joao Pessoa",
            required=True
        ),
        "state": fields.String(
            description="State",
            example="SP|PB|PE",
            required=True,
            length=2
        ),
        "total_area": fields.Integer(
            description="Total farm area in hectares",
            example="100",
            required=True
        ),
        "agricultural_area": fields.Integer(
            description="Agricultural area in hectares",
            example="30",
            required=True
        ),
        "vegetation_area": fields.Integer(
            description="Vegetation area in hectares",
            example="20",
            required=True
        ),
        "farming_options": CustomJsonField(
            description="Farming options",
            example="['SOY', 'CORN']",
            required=True
        )
    }
)


farmer_create_response_model = Model(
    "Farmer create response",
    farmer_create_request_model)
farmer_create_response_model["insert_at"] = fields.DateTime(
                                            required=True,
                                            description="Farmer creation date",
                                            example="2022-01-01T00:00:00",
                                        )
farmer_create_response_model["update_at"] = fields.DateTime(
                                            required=True,
                                            description="Farmer creation date",
                                            example="2022-01-01T00:00:00",
                                        )


### UPDATE FARMER
class FarmerUpdateRequestSchema(FarmerCreateRequestSchema):
    name = ma.fields.String(
        description="Name",
        example="Aragorn"
    )
    farm_name = ma.fields.String(
        description="Farm name",
        example="Fazenda LOTR"
    )
    city = ma.fields.String(
        description="City name",
        example="Joao Pessoa"
    )
    state = ma.fields.String(
        description="State",
        example="SP|PB|PE",
        validate=ma.validate.Length(min=2, max=2)
    )
    total_area = ma.fields.Integer(
        description="Total farm area in hectares",
        example="100"
    )
    agricultural_area = ma.fields.Integer(
        description="Agricultural area in hectares",
        example="30"
    )
    vegetation_area = ma.fields.Integer(
        description="Vegetation area in hectares",
        example="20"
    )
    farming_options = ma.fields.List(
        ma.fields.String(),
        description="Farming options",
        example=["SOY", "CORN"]
    )
    
    @ma.validates_schema
    def validate_total_area(self, data, **kwargs):
        pass

    class Meta:
        exclude = ["cpf_cnpj"]

farmer_update_request_model = Model(
    "Farmer update request",
    {
        "name": fields.String(
            description="Name",
            example="Aragorn"
        ),
        "farm_name": fields.String(
            description="Farm name",
            example="Fazenda LOTR"
        ),
        "city": fields.String(
            description="City name",
            example="Joao Pessoa"
        ),
        "state": fields.String(
            description="State",
            example="SP|PB|PE",
            max_length=2
        ),
        "total_area": fields.Integer(
            description="Total farm area in hectares",
            example="100"
        ),
        "agricultural_area": fields.Integer(
            description="Agricultural area in hectares",
            example="30"
        ),
        "vegetation_area": fields.Integer(
            description="Vegetation area in hectares",
            example="20"
        ),
        "farming_options": CustomJsonField(
            description="Farming options",
            example="['SOY', 'CORN']"
        )
    }
)
