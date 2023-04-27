from fastapi import FastAPI
import boto3
from pydantic import BaseModel


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
