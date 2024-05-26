import sys

def handler(event, context):
    return 'Hello from AWS Lambda usando Python'+ sys.version + '!'