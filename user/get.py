import os
import json

import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch user from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    if 'login' in result['Item']:
        del result['Item']['login']
    if 'password' in result['Item']:
        del result['Item']['password']

    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
