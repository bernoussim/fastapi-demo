from fastapi import FastAPI
import boto3

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}


ddb_resource = boto3.resource('dynamodb')


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    response = ddb_resource.Table('employees').get_item(
        Key={'employee_id': employee_id}
    )
    return response['Item']


@app.post("/employees")
def create_employee(
    employee_id: int, first_name: str, last_name: str, country: str, salary: int
):
    response = ddb_resource.Table('employees').put_item(
        Item={
            'employee_id': employee_id,
            'first_name': first_name,
            'last_name': last_name,
            'country': country,
            'salalry': salary,
        }
    )
    return response
