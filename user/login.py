import json
import os

import decimalencoder
import boto3
from boto3.dynamodb.conditions import Attr
dynamodb = boto3.resource('dynamodb')


def login(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    data = json.loads(event['body'])

    if 'login' in data and 'password' in data:

        result = table.scan(
            FilterExpression=Attr('login').eq(data['login'])
                             & Attr('password').eq(data['password']),
        )
        item = result['Items'][0]
        del item['login']
        del item['password']

        return {
            "statusCode": 200,
            "body": json.dumps(item, cls=decimalencoder.DecimalEncoder)
        }
    return {
        "statusCode": 400,
        "body": json.dumps({'error': 'This user does not exist or wrong pass'}, cls=decimalencoder.DecimalEncoder)
    }
