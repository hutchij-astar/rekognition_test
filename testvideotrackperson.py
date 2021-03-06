#Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import json
import sys


class VideoDetect:
    jobId = ''
    rek = boto3.client('rekognition', region_name='us-east-1')
    queueUrl = 'https://sqs.us-east-1.amazonaws.com/195459434260/RekognitionTestAstar'
    roleArn = 'arn:aws:iam::195459434260:role/AstarRekognitionServiceRole'
    topicArn = 'arn:aws:sns:us-east-1:195459434260:AmazonRekognitionAstarTesting'
    bucket = 'a-star.io.test'
    video = 'out.mp4'

    def main(self):

        jobFound = False
        sqs = boto3.client('sqs', region_name='us-east-1')
       

        #=====================================
        response = self.rek.start_person_tracking(Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}},
                                         NotificationChannel={'RoleArn': self.roleArn, 'SNSTopicArn': self.topicArn})
        #=====================================
        print('Start Job Id: ' + response['JobId'])
        dotLine=0
        while jobFound == False:
            sqsResponse = sqs.receive_message(QueueUrl=self.queueUrl, MessageAttributeNames=['ALL'],
                                          MaxNumberOfMessages=10)

            if sqsResponse:
                
                if 'Messages' not in sqsResponse:
                    if dotLine<20:
                        print('.', end='')
                        dotLine=dotLine+1
                    else:
                        print()
                        dotLine=0    
                    sys.stdout.flush()
                    continue

                for message in sqsResponse['Messages']:
                    notification = json.loads(message['Body'])
                    rekMessage = json.loads(notification['Message'])
                    print(rekMessage['JobId'])
                    print(rekMessage['Status'])
                    if str(rekMessage['JobId']) == response['JobId']:
                        print('Matching Job Found:' + rekMessage['JobId'])
                        jobFound = True
                        #=============================================
                        self.GetResultsTracking(rekMessage['JobId'])
                        #=============================================

                        sqs.delete_message(QueueUrl=self.queueUrl,
                                       ReceiptHandle=message['ReceiptHandle'])
                    else:
                        print("Job didn't match:" +
                              str(rekMessage['JobId']) + ' : ' + str(response['JobId']))
                    # Delete the unknown message. Consider sending to dead letter queue
                    sqs.delete_message(QueueUrl=self.queueUrl,
                                   ReceiptHandle=message['ReceiptHandle'])

        print('done')


    def GetResultsTracking(self, jobId):
        maxResults = 10
        paginationToken = ''
        finished = False

        while finished == False:
            response = self.rek.get_person_tracking(JobId=jobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken,
                                            SortBy='TIMESTAMP')

            print(response['VideoMetadata']['Codec'])
            print(str(response['VideoMetadata']['DurationMillis']))
            print(response['VideoMetadata']['Format'])
            print(response['VideoMetadata']['FrameRate'])

            for personDetection in response['Persons']:
                print('detection timestamp: ', str(personDetection['Timestamp']))
                print('person index: ', personDetection['Person']['Index'])
                if 'BoundingBox' in personDetection['Person']:
                    print('person bounds: ', personDetection['Person']['BoundingBox'])

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True





if __name__ == "__main__":

    analyzer=VideoDetect()
    analyzer.main()