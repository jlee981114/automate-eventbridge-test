import boto3
import json

def lambda_handler(event, context):
    client = boto3.client('events')
    s3_client = boto3.client('s3')
    
    # Replace with your S3 bucket name where the rule name is stored
    bucket_name = 'justin-lambda-functions-bucket'  
    # Name of the file where the rule name is saved in S3
    rule_file = 'latest_rule.json'  
    
    try:
        # Retrieve the rule name from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=rule_file)
        rule_info = json.loads(response['Body'].read().decode('utf-8'))
        old_rule_name = rule_info['rule_name']
        
        # Disable and delete the old rule
        client.disable_rule(Name=old_rule_name)
        client.delete_rule(Name=old_rule_name)
        
        print(f"Disabled and deleted old rule: {old_rule_name}")
        
    except s3_client.exceptions.NoSuchKey:
        return {"message": "No rule found to disable or delete"}
    
    return {"message": "Old rule disabled and deleted"}
