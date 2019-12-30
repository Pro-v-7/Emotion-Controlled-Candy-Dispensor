from __future__ import print_function
  
import json
import boto3
import base64
print('Loading function')
  
def lambda_handler(event, context):
  
    # Parse the JSON message 
    
  
    # Print the parsed JSON message to the console; you can view this text in the Monitoring tab in the Lambda console or in the CloudWatch Logs console
    
    
    
    BUCKET = "amazon-rekognition"
    KEY = "test.jpg"
    FEATURES_BLACKLIST = ("Landmarks", "Emotions", "Pose", "Quality", "BoundingBox", "Confidence")
    i=base64.b64decode(str(event['m']))
    def detect_faces(bucket, key, attributes=['ALL'], region="us-east-1"):
        rekognition = boto3.client("rekognition",region)
        response = rekognition.detect_faces(
                Image={'Bytes': i},
                Attributes=attributes,
        )
        return response['FaceDetails']

    for face in detect_faces(BUCKET, KEY):
        print ("Face ({Confidence}%)".format(**face))

        # emotions
        max=0
        for emotion in face['Emotions']:
                if(max<emotion['Confidence']):
                        max=emotion['Confidence']
                        em=emotion['Type']
                print ("  {Type} : {Confidence}%".format(**emotion))
        #print(em)
        # quality
        
        
        
    
    
    
    
    # Create an MQTT client
    
    client = boto3.client('iot-data')
    response = client.publish(
    topic='emotion_fetch',
    qos=0,
    payload=em
    )
