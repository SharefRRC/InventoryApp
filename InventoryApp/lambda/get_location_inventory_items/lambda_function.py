import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'
    index_name = 'location-index'

    try:
        item_location_id = int(event['pathParameters']['id'])

        response = dynamo_client.query(
            TableName=table_name,
            IndexName=index_name,
            KeyConditionExpression='item_location_id = :location_id',
            ExpressionAttributeValues={
                ':location_id': {'N': str(item_location_id)}
            }
        )

        items = response.get('Items', [])

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }