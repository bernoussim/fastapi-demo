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
