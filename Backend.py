import botocore
import boto3
import logging
import json
import random
import time

from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Backend:
    """Encapsulates an Amazon DynamoDB table of boozy data."""
    def __init__(self):
        """
        :param dyn_resource: A Boto3 DynamoDB resource.
        """
        self.dyn_resource = boto3.resource('dynamodb', region_name='eu-west-2')
        self.table = self.dyn_resource.Table('twitch_booze')
        self.client = boto3.client('dynamodb', region_name='eu-west-2')

    def makeKey(self, user, platform, type):
        if user == None:
            user = "anonymous"

        if platform == None:
            platform = "twitch"

        if type == None:
            type = "beer"

        return user + ":" + platform + ":" + type 

    def get_user(self, key):
        try:
            response = self.client.get_item(
                TableName=self.table.name,
                Key={
                    'user': {'S': key}
                }, ConsistentRead=True, ProjectionExpression="drinks, expires")
        except ClientError as err:
            logger.warn(
                "Couldn't get user %s from table %s. Here's why: %s: %s",
                user, self.table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        else:
            if response.get('Item'):
                now = int(time.time())
                expires = int(response['Item']['expires']['N'])
                if now < expires:
                    return int(response['Item']['drinks']['N'])
                else:
                    """TODO: Hmm, this might be a waste of time, since we're just going to increment and replace this with 1"""
                    """self.delete_user(key)"""
                    """self.set_user(user, 0)"""
                    return 0
            else:
                return 0
            
    def set_user(self, key, drinks):
        now = int(time.time())
        expires = now + (8 * 3600)
        try:
            reponse = self.client.put_item(
                TableName=self.table.name,
                Item={
                    'user': {'S': key},
                    'drinks': {'N': str(drinks)},
                    'expires': {'N': str(expires)}
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't get user %s from table %s. Here's why: %s: %s",
                key, self.table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    def delete_user(self, key):
        try:
            response = self.client.delete_item(
                TableName=self.table.name,
                Key={
                    'user': {'S': key}
                }
            )
        except ClientError as err:
            logger.error(
                "Couldn't delete user %s from table %s. Here's why: %s: %s",
                user, self.table,
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
