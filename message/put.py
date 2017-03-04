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
    # update the message in the database

    expressionAttributeNames = {}
    expressionAttributeValues = {':updated': timestamp}
    updateExpression = 'SET updated = :updated'

    if 'author' in data:
        expressionAttributeNames['#message_author'] = 'author'
        expressionAttributeValues[':author'] = data['author']
        updateExpression += ', #message_author = :author'

    if 'receivers' in data:
        expressionAttributeNames['#message_receivers'] = 'receivers'
        expressionAttributeValues[':receivers'] = data['receivers']
        updateExpression += ', #message_receivers = :receivers'

    if 'text' in data:
        expressionAttributeNames['#message_text'] = 'text'
        expressionAttributeValues[':text'] = data['text']
        updateExpression += ', #message_text = :text'

    if 'time' in data:
        expressionAttributeNames['#message_time'] = 'time'
        expressionAttributeValues[':time'] = data['time']
        updateExpression += ', #message_time = :time'

    if 'created' in data:
        expressionAttributeNames['#message_created'] = 'created'
        expressionAttributeValues[':created'] = data['created']
        updateExpression += ', #message_created = :created'

    if 'location' in data:
        expressionAttributeNames['#message_location'] = 'location'
        expressionAttributeValues[':location'] = data['location']
        updateExpression += ', #message_location = :location'

    if 'description' in data:
        expressionAttributeNames['#message_description'] = 'description'
        expressionAttributeValues[':description'] = data['description']
        updateExpression += ', #message_description = :description'

    if 'status' in data:
        expressionAttributeNames['#message_type'] = 'type'
        expressionAttributeValues[':type'] = data['type']
        updateExpression += ', #message_type = :type'

    if 'status' in data:
        expressionAttributeNames['#message_status'] = 'status'
        expressionAttributeValues[':status'] = data['status']
        updateExpression += ', #message_status = :status'

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames=expressionAttributeNames,
        ExpressionAttributeValues=expressionAttributeValues,
        UpdateExpression=updateExpression,
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
