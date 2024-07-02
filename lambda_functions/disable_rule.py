import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('events')
    s3_client = boto3.client('s3')
    
    # Replace with your S3 bucket name where the rule name is stored
    bucket_name = 'justin-lambda-functions-bucket'  
    # Name of the file where the rule name is saved in S3
    rule_file = 'latest_rule.json'  
    
    # Retrieve the rule name from S3
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=rule_file)
        rule_info = json.loads(response['Body'].read().decode('utf-8'))
        old_rule_name = rule_info['rule_name']
    except s3_client.exceptions.NoSuchKey:
        return {"message": "No rule found to disable"}
    
    # Disable the old rule
    response = client.disable_rule(
        Name=old_rule_name
    )

    return response
