#!/usr/bin/python3

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

client = boto3.client('iam')
try:
    response = client.list_users()
    print(response)
except:
    response = client.list_users()
    print(response)
