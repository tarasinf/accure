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

    result = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#user_friends': 'friends',
          '#user_profile': 'profile',
          '#user_ownLocations': 'ownLocations',
        },
        ExpressionAttributeValues={
          ':friends': data.get('friends', []),
          ':profile': data.get('profile', {}),
          ':ownLocations': data.get('ownLocations', []),

          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #user_friends = :friends, '
                         '#user_profile = :profile, '
                         '#user_ownLocations = :ownLocations, '

                         'updatedAt = :updatedAt',
        ReturnValues='ALL_NEW',
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Attributes'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response
