import json
import logging
import os
import time
import uuid

import boto3
dynamodb = boto3.resource('dynamodb')


def post(event, context):
    data = json.loads(event['body'])
    if 'author' not in data or 'location' not in data:
        logging.error("Validation Failed")
        raise Exception("Couldn't create the mesagge item.")
        return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    item = {
        'id': str(uuid.uuid1()),
        'author': data['author'],
        'receivers': data.get('receivers', []),
        'text': data.get('text', ''),
        'time': data.get('time', None),
        'updated': timestamp,
        'created': timestamp,
        'location': data['location'],
        'description': data.get('description', ''),
        'status': "unread",
        'type': "private"
    }

    # write the todo to the database
    table.put_item(Item=item)

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(item)
    }

    return response
