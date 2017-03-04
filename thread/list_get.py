import json
import os

import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def list_get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch all threads from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
