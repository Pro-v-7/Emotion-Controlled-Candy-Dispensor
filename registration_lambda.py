import json
import boto3

def lambda_handler(event, context):
    # TODO implement
    
    client = boto3.client('iot-data')
    
    dynamodb = boto3.resource('dynamodb')
    tableName = "Caandy_Registration"
    table = dynamodb.Table(tableName)
    
    #RRFID=event['RFID']
  
    table.put_item(
        Item={
            'RFID':event['RFID'],
            'Name':event['Name'],
            'Email':event['Email']
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'headers':json.dumps( {
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Headers':'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
            'Access-Control-Allow-Credentials' : True,
            'Content-Type': 'application/json'
        })
    }
