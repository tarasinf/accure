import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def post(event, context):
    data = json.loads(event['body'])
    if 'firstName' not in data or 'lastName' not in data :
        logging.error("Validation Failed")
        raise Exception("Couldn't create the user item without firstName or lastName.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'friends': data.get('friends', []),
        'profile': {
            'firstName': data['firstName'],
            'lastName': data['lastName'],
            'avatar': data.get('avatar', None)
        },
        'ownLocations': data.get('ownLocations', []),
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
