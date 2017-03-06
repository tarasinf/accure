import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def registration(event, context):
    data = json.loads(event['body'])
    if 'login' not in data or 'password' not in data:
        return {
            "statusCode": 400,
            "body": json.dumps({'error': "Couldn't create the user item without login or password."})
        }

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    token = 'token' + data['login'] + data['password']

    item = {
        'id': str(uuid.uuid1()),
        'token': token,
        'login': data['login'],
        'password': data['password'],
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    table.put_item(Item=item)

    del item['login']
    del item['password']

    return {
        "statusCode": 201,
        "body": json.dumps(item)
    }
