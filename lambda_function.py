import json
import logging
import sys
import os

from Backend import Backend
from Language import Language

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

backend = Backend()

def lambda_handler(event, context):
    user = event["queryStringParameters"].get("user")
    platform = event["queryStringParameters"].get("platform")
    type = event["queryStringParameters"].get("type")
    set = event["queryStringParameters"].get("set")

    lang = Language(type)

    key = backend.makeKey(user, platform, type)

    if set == None:
        drinks = backend.get_user(key)
        drinks += 1
    else:
        try:
            drinks = int(set)
            if (drinks <= 0):
                drinks = 0
        except ValueError as e:
            drinks = backend.get_user(key)
            drinks += 1

    if type == None:
        type = "beer"

    if drinks >= 9:
        if type != 'slash':
            return {
                'statusCode': 200,
                'body': '@' + user + " hey, c'mon man.  Drink something other than " + type + " Kappa"
            }

    if drinks == 1:
        english = 'beverage'
        slashes  = 'time'
    else:
        english = 'beverages'
        slashes = 'times'

    backend.set_user(key, drinks)

    outputMessage = ''
    if type == 'slash':
        outputMessage = "dj needs a slash ... that's "
        if drinks == 1:
            outputMessage = outputMessage + 'once'
        elif drinks == 2:
            outputMessage = outputMessage + 'twice'
        else:
            outputMessage = outputMessage + str(drinks) + ' ' + slashes
            
        outputMessage = outputMessage + " now!"
    else:
        outputMessage = '@' + user + ' has ' + lang.get_imbibed() + ' ' + str(drinks) + ' ' + lang.get_alcoholic() + ' ' + english + ' ' + lang.get_session()

    return {
        'statusCode': 200,
        'body': outputMessage
    }
