import boto3
import json
from ulid import ULID

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    try:
        body = json.loads(event['body'])

        item_id = str(ULID())
        item_name = body['item_name']
        item_description = body['item_description']
        item_qty_on_hand = int(body['item_qty_on_hand'])
        item_price = str(body['item_price'])
        item_location_id = int(body['item_location_id'])

        dynamo_client.put_item(
            TableName=table_name,
            Item={
                'item_id': {'S': item_id},
                'item_name': {'S': item_name},
                'item_description': {'S': item_description},
                'item_qty_on_hand': {'N': str(item_qty_on_hand)},
                'item_price': {'N': item_price},
                'item_location_id': {'N': str(item_location_id)}
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Item added successfully',
                'item_id': item_id
            })
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }