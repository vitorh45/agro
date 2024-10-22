# Agro

## Contents of this file

 - Introduction
 - Requirements
 - Installation and usage
 - Endpoints
 - Tests
 - Live version
 - Postman collections

## Introduction

Agro is a project to simulate farmers registration

## Requirements

 - Python 3.11+
 - Postgres as database
 - Docker to create the images (optional)

## Installation and usage

To run the project locally, we need to follow some steps:

 - First we need to have python 3.11 installed. You can use the lib pyenv to control different python versions.
 - Is optional and recommended to use a virtualenv with the python 3.11. By doing that, you can isolate you projects environments.
 - Install the projects dependencies inside the SRC directory with run the command `pip install -r dependencies/requirements-dev.txt`.
 - Rename the `.env_sample` file to `.env`.
 - Having a Postgres running locally, create two databases called `agro` and `agro_test`. If you change the default Postgres port, change the value in the `.env` file.
 - Create the database tables running the migration command inside the src/api dir, whether running locally or with Docker: `flask db upgrade`
 - Run the project locally with `flask run`
 - If you want to run using Docker, run the command in the project root dir `docker-compose up`. It will build and start an image of the project and a Postgres as well. Make sure you don't have another postgres instance running in the port 5342.
- to run the unit tests and check the coverage, run the command in root dir `make test`

## Endpoints

Now that the project is running locally in the address http://localhost:5000 (or http://localhost:5001 with the docker image), we are going to do requests to interact with the application.

### Requests
- POST /api/v1/farmers: Pass in the request body all the necessary data. The `cpf_cnpj` accepts both types of data, cpf and cnpj. You must use a real cpf or cnpj. It's validated. The `state` must to be the acronym. The `farming_options` must to be one of SUGARCANE, COTTON, SOY, CORN or COFFEE. The total area must to be higher or equal to the sum of agricultural and vegetation areas. Example:
```
{
    "cpf_cnpj": "57698266000178",
    "name": "Fazendeiro 123",
    "farm_name": "Fazenda LOTR",
    "city": "Joao Pessoa",
    "state": "PB",
    "total_area": 100,
    "agricultural_area": 40,
    "vegetation_area": 50,
    "farming_options": ["SUGARCANE"]
}
```
- DELETE /api/v1/farmers?cpf_cnpj=00100200304: Pass in the url the `cpf_cnpj` parameter.
- PATCH /api/v1/farmers?cpf_cnpj=00100200304: This endpoint accepts all the fields used to create a farmer except the  `cpf_cnpj` in the request body. Example:
```
{
    "name": "Fazendeiro 123",
    "farm_name": "Fazenda LOTR",
    "city": "Joao Pessoa",
    "state": "PB",
    "total_area": 100,
    "agricultural_area": 40,
    "vegetation_area": 50,
    "farming_options": ["SUGARCANE"]
}
```
- GET /api/v1/farmers?limit=1&offset=1: To list all farmers. Accepts two parameters `limit` to limit the amount of items returned and `offset` to combine with `limit` and paginate the result in case of o great amount of items.

### Responses
- 200: if the request is successfull
- 201: if the creation request is successfull
- 400: general error. Examples: invalid `cpf_cnpj` in farmer creation. Wrong fields values in request body on farmer creation on update. Duplicated `cpf_cnpj` when creating a farmer.
- 404: if you try update or delete a farmer with an invalid `cpf_cnpj`

## Tests

To check all the endpoints and request data, access the online documentation. Consider you are running locally, access the endpoint `http://localhost:5000/docs/swagger`


## Live version

There a version deployed on Render.com. The base url is `https://agro-qxlx.onrender.com` and the swagger docs is `https://agro-qxlx.onrender.com/docs/swagger`. It's a small instance. Use it smart for simple tests purpose.


## Postman collections
There four files with Postman collection of requests and environments to test the requests locally with and without docker and the current live version. Import the files inside the Postman.