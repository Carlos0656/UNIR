import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    # translate the text
    text = result['Item']['text']
    dest = event['pathParameters']['lng']
    translate = boto3.client('translate', region_name="us-east-1")
    res = translate.translate_text(Text=text, SourceLanguageCode="auto", TargetLanguageCode=dest)
    
    
    # send response with translated text
    result['Item']['text'] = res['TranslatedText']
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                                    cls=decimalencoder.DecimalEncoder)
    }

    return response
    