import boto3
import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
daleteMethod = 'DELETE'
healthPath = '/health'
product = '/product'
products = '/products'



def lambda_handler(event, context):
    pass