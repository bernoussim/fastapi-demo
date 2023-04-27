from fastapi import FastAPI, status
import boto3
from pydantic import BaseModel, validator
from boto3.dynamodb.conditions import Attr


app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK, tags=["Home"])
def home():
    return {"message": "Hello World"}


ddb_resource = boto3.resource('dynamodb')


class Employee(BaseModel):
    employee_id: int
    first_name: str
    last_name: str
    country: str
    salary: int

    @validator('employee_id')
    def validate_employee_id(cls, v):
        if v > 9999 or v < 1000:
            raise ValueError('Employee ID must have 4 digits')
        return v


@app.get("/employees/{employee_id}", status_code=status.HTTP_200_OK, tags=["Employees"])
def get_employee(employee_id: int):
    response = ddb_resource.Table('employees').get_item(
        Key={'employee_id': employee_id}
    )
    return response['Item']


@app.post(
    "/employees",
    status_code=status.HTTP_201_CREATED,
    tags=["Employees"],
    summary="Create a new employee",
)
async def create_employee(employee: Employee):
    response = ddb_resource.Table('employees').put_item(Item=employee.dict())
    return response


@app.get("/employees", status_code=status.HTTP_200_OK, tags=["Employees"])
def get_employees(first_name: str):
    response = ddb_resource.Table('employees').scan(
        FilterExpression=Attr('first_name').eq(first_name)
    )
    return response['Items']
