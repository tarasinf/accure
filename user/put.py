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
    #     raise Exception("Couldn't update the user item.")
    #     return

    timestamp = int(time.time() * 1000)

    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # update the user in the database

    expressionAttributeNames = {}
    expressionAttributeValues = {':updatedAt': timestamp}
    updateExpression = 'SET updatedAt = :updatedAt'

    if 'friends' in data:
        expressionAttributeNames['#user_friends'] = 'friends'
        expressionAttributeValues[':friends'] = data['friends']
        updateExpression += ', #user_friends = :friends'

    if 'FCMToken' in data:
        expressionAttributeNames['#user_FCMToken'] = 'FCMToken'
        expressionAttributeValues[':FCMToken'] = data['FCMToken']
        updateExpression += ', #user_FCMToken = :FCMToken'

    if 'firstName' in data:
        expressionAttributeNames['#user_firstName'] = 'firstName'
        expressionAttributeValues[':firstName'] = data['firstName']
        updateExpression += ', #user_firstName = :firstName'

    if 'lastName' in data:
        expressionAttributeNames['#user_lastName'] = 'lastName'
        expressionAttributeValues[':lastName'] = data['lastName']
        updateExpression += ', #user_lastName = :lastName'

    if 'avatar' in data:
        expressionAttributeNames['#user_avatar'] = 'avatar'
        expressionAttributeValues[':avatar'] = data['avatar']
        updateExpression += ', #user_avatar = :avatar'
    if 'ownLocations' in data:
        expressionAttributeNames['#user_ownLocations'] = 'ownLocations'
        expressionAttributeValues[':ownLocations'] = data['ownLocations']
        updateExpression += ', #user_ownLocations = :ownLocations'


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
