from fastapi import APIRouter, FastAPI, status, Depends
import boto3
from pydantic import BaseModel, validator
from boto3.dynamodb.conditions import Attr
from providers.tax_retriever import TaxRateRetrieverSSM, TaxRateRetrieverDDB
from domains.employee import Employee as _employee


router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, tags=["Home"])
def home():
    return {"message": "Hello World"}


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


def initialize_ddb():
    ddb = boto3.resource('dynamodb')
    return ddb


@router.get(
    "/employees/{employee_id}",
    status_code=status.HTTP_200_OK,
    tags=["Employees"],
)
def get_employee(employee_id: int, ddb=Depends(initialize_ddb)):
    response = ddb.Table('employees').get_item(Key={'employee_id': employee_id})
    return response['Item']


@router.post(
    "/employees",
    status_code=status.HTTP_201_CREATED,
    tags=["Employees"],
    summary="Create a new employee",
)
async def create_employee(employee: Employee, ddb=Depends(initialize_ddb)):
    response = ddb.Table('employees').put_item(Item=employee.dict())
    return response


@router.get("/employees", status_code=status.HTTP_200_OK, tags=["Employees"])
def get_employees(first_name: str, ddb=Depends(initialize_ddb)):
    response = ddb.Table('employees').scan(
        FilterExpression=Attr('first_name').eq(first_name)
    )
    return response['Items']


@router.get(
    "/employee/netsalary/{employee_id}",
    status_code=status.HTTP_200_OK,
    tags=["Employees"],
)
def get_netsalary(
    employee_id: int, ddb=Depends(initialize_ddb), tr=Depends(TaxRateRetrieverDDB)
):
    response = ddb.Table('employees').get_item(Key={'employee_id': employee_id})
    employee = _employee(**response['Item'])
    tax_rate = tr.get_tax_rate(employee.country)
    net_salary = employee.calculate_net_salary(tax_rate)
    return net_salary
