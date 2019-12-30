import json
import boto3

def lambda_handler(event, context):
    
    
    
    dynamodb = boto3.resource('dynamodb')
    tableName = "Caandy_Registration"
    table = dynamodb.Table(tableName)
    rfid=event['rfid']
    try:
        response = table.get_item(
            Key={
                'RFID':rfid,
            }
        )
        name=response['Item']['Name']
        email=response['Item']['Email']
        
        client = boto3.client('iot-data')
        response = client.publish(
        topic='candy_data',
        qos=0,
        payload=name
        )
    
    
    except:
        client = boto3.client('iot-data')
        response = client.publish(
        topic='candy_data',
        qos=0,
        payload="data not found"
        )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
