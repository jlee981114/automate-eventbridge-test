import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('events')
    s3_client = boto3.client('s3')
    
    # Replace with your S3 bucket name where the rule name will be stored
    bucket_name = 'justin-lambda-functions-bucket'  
    # Name of the file where the rule name is saved in S3
    rule_file = 'latest_rule.json'
    
    # Name of the new rule to be created - change this for different projects
    rule_name = 'new-event-pattern-rule'  
    event_pattern = {
        "source": ["aws.codepipeline"],  # Update this to match your event source
        "detail-type": ["CodePipeline Pipeline Execution State Change"],  # Update this to match your event detail type
        "detail": {
            "state": ["SUCCEEDED"]  # Update this to match your event details
        }
    }

    try:
        # Check if an old rule exists and disable it
        try:
            response = s3_client.get_object(Bucket=bucket_name, Key=rule_file)
            rule_info = json.loads(response['Body'].read().decode('utf-8'))
            old_rule_name = rule_info['rule_name']
            
            client.disable_rule(Name=old_rule_name)
            client.delete_rule(Name=old_rule_name)
            print(f"Disabled and deleted old rule: {old_rule_name}")
        except s3_client.exceptions.NoSuchKey:
            print("No existing rule to disable or delete.")
        
        # Create the new EventBridge rule
        response = client.put_rule(
            Name=rule_name,
            EventPattern=json.dumps(event_pattern),
            State='ENABLED',
            Description='Rule triggered by CodePipeline state change'  # Update this description as needed
        )

        # Save the new rule name to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=rule_file,
            Body=json.dumps({"rule_name": rule_name})
        )

        print(f"Rule {rule_name} created and saved to S3.")
    
    except Exception as e:
        print(f"Error creating rule or saving to S3: {e}")

    return response
