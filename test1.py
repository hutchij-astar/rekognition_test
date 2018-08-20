#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import json
import io

if __name__ == "__main__":
    fileName='R0010500.JPG'
    bucket='a-star.io.c1044160-8f74-11e8-a719-19bfb3b4cca6'
    
    client=boto3.client('rekognition', region_name='us-east-1')

    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})

    if len(response['Labels'])>0:
        print('Detected labels for ' + fileName)    
        outname = fileName.replace('.JPG', '_labels.json')
        with open(outname, 'w') as outfile:
            json.dump(response['Labels'], outfile) 
        for label in response['Labels']:
            print (label['Name'] + ' : ' + str(label['Confidence']))
    else:
        print('No labels detected')

    response = client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
 
    if len(response['TextDetections'])>0:
        print('Detected text for ' + fileName)  
        outname = fileName.replace('.JPG', '_text.json')
        with open(outname, 'w') as outfile:
            json.dump(response['TextDetections'], outfile)  
        for td in response['TextDetections']:
            print(td)
            #print (td['DetectedText'] + ' : ' + str(td['Confidence']))
    else:
        print('No text detected')

    response = client.detect_faces( Attributes =  [ "ALL" ], Image={'S3Object':{'Bucket':bucket,'Name':fileName}})
 
    if len(response['FaceDetails'])>0:
        outname = fileName.replace('.JPG', '_face.json')
        with open(outname, 'w') as outfile:
            json.dump(response['TextDetections'], outfile)         
        print('Detected faces for ' + fileName)    
        for face in response['FaceDetails']:
            print (str(face['Confidence']))
    else:
        print('No faces detected')