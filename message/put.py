import json
import time
import logging
import os
import decimalencoder
import boto3

dynamodb = boto3.resource('dynamodb')


def put(event, context):
    data = json.loads(event['body'])
    # if 'text' not in data or 'checked' not in data:
    #     logging.error("Validation Failed")
    #     raise Exception("Couldn't update the message item.")
    #     return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
``
    # update the message in the database

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#message_receivers': 'receivers',
          '#message_text': 'text',
          '#message_location': 'location',
          '#message_type': 'type',
          '#message_updated': 'updated',
          '#message_created': 'created',
          '#message_description': 'description',
          '#message_time': 'time',
          '#message_status': 'status'

        },
        ExpressionAttributeValues={
          'receivers': data.get('receivers', []),
          'text': data.get('text', ''),
          'time': data.get('time', None),
          'updated': timestamp,
          'created': timestamp,
          'location': data['location'],
          'description': data.get('description', ''),
          'status': "unread",
          'type': "private"
        },
        UpdateExpression='#message_receivers = : receivers'
                         '#message_text = : text'
                         '#message_location = : location'
                         '#message_type = : type'
                         '#message_updated = : updated'
                         '#message_created = : created'
                         '#message_description = : description'
                         '#message_time = : time'
                         '#message_status = : status',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response


    
