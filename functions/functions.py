from main import handler

# Netlify Lambda function handler
def lambda_handler(event, context):
    return handler(event, context)