import json
import os

import decimalencoder
import boto3
from boto3.dynamodb.conditions import Key, Attr
dynamodb = boto3.resource('dynamodb')


def list_get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    if event.get('queryStringParameters', False) and event['queryStringParameters'].get('user_id'):

        result = table.scan(
            FilterExpression=Attr('receivers').contains(event['queryStringParameters']['user_id'])
        )
    else:
        result = table.scan()

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'], cls=decimalencoder.DecimalEncoder)
    }

    return response
