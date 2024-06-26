import boto3
import json
import logging

from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = '13-exemplo-product-inventory'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath = '/health'
productPath = '/product'
productsPath = '/products'



def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == productPath:
        response = getProduct(event["queryStringParameters"]["productid"])
    elif httpMethod == getMethod and path == productsPath:
        response = getProducts()
    elif httpMethod == postMethod and path == productPath:
        response = saveProduct(json.loads(event["body"]))
    elif httpMethod == patchMethod and path == productPath:
        requestBody = json.loads(event["body"])
        response = modifyProduct(requestBody["productid"], requestBody["updateKey"], requestBody["updateValue"])
    elif httpMethod == deleteMethod and path == productPath:
        requestBody = json.loads(event["body"])
        response = deleteProduct(requestBody["productid"])
    else:
        response = buildResponse(404, "Not Found")
    return response 

def getProduct(productid):
    try:
        response = table.get_item(
            Key={
                "productid": productid
            }
        )
        if "Item" in response:
            return buildResponse(200, response["Item"])
        else:
            return buildResponse(404, {"Message": "Productid: {0}s not found".format(productid)})
    except:
        logger.exception("Do your custom error handling here. I am just gonna log it our here!!")

def getProducts():
    try:
        response = table.scan()
        result = response["Items"]

        while "LastEvaluateKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            result.extend(response["Items"])

        body = {
            "products": response
        }
        return buildResponse(200, body)
    except:
        logger.exception("Do your custom error handling here. I am just gonna log it our here!!")

def saveProduct(requestBody):
    try: 
        table.put_item(Item=requestBody)
        body = {
            "Operation": "SAVE",
            "Message": "SUCCESS",
            "Item": requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception("Do your custom error handling here. I am just gonna log it our here!!")

def modifyProduct(productid, updateKey, updateValue):
    try:
        response = table.update_item(
            Key={
                "productid": productid
            },

            UpdateExpression="set {0}s = :value".format(updateKey),
            ExpressionAttributeValues={
                ":value": updateValue
            },
            ReturnValues="UPDATED_NEW"
        )
        body = {
            "Operation": "UPDATE",
            "Message": "SUCCESS",
            "UpdatedAttributes": response
        }
        return buildResponse(200, body)
    except:
        logger.exception("Do your custom error handling here. I am just gonna log it our here!!")

def deleteProduct(productid):
    try:
        response = table.delete_item(
            Key={
                "productid": productid
            },
            ReturnValues="ALL_OLD"
        )
        body = {
            "Operation": "DELETE",
            "Message": "SUCCESS",
            "deltedItem": response
        }
        return buildResponse(200, body)
    except:
        logger.exception("Do your custom error handling here. I am just gonna log it our here!!")
    

def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers':{
            'Content-Type': 'application/json',
            'Acess-Control-Allow-Origin': '*'
        }
    }

    if body is not None:
        response['body'] = json.dumps(body)
    
    return response


