from fastapi import FastAPI
import boto3
from pydantic import BaseModel, validator


app = FastAPI()


@app.get("/")
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


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    response = ddb_resource.Table('employees').get_item(
        Key={'employee_id': employee_id}
    )
    return response['Item']


@app.post("/employees")
def create_employee(employee: Employee):
    response = ddb_resource.Table('employees').put_item(Item=employee.dict())
    return response
