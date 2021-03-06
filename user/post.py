import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def post(event, context):
    data = json.loads(event['body'])
    if 'firstName' not in data or 'lastName' not in data:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Couldn't create the user item without firstName or lastName."})
        }

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    token = ''

    item = {
        'id': str(uuid.uuid1()),
        'FCMToken': data.get('FCMToken', None),
        'token': token,
        'login': data['login'],
        'password': data['password'],
        'friends': data.get('friends', []),
        'firstName': data.get('firstName', None),
        'lastName': data.get('lastName', None),
        'avatar': data.get('avatar', None),
        'ownLocations': data.get('ownLocations', []),
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps(item)
    }
