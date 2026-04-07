import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    try:
        item_id = event['pathParameters']['id']

        response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression='item_id = :item_id',
            ExpressionAttributeValues={
                ':item_id': {'S': item_id}
            }
        )

        items = response.get('Items', [])

        if len(items) == 0:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(items[0], default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }