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
        "source": ["aws.codepipeline"],
        "detail-type": ["CodePipeline Pipeline Execution State Change"],
        "detail": {
            "state": ["SUCCEEDED"]
        }
    }

    try:
        # Create the EventBridge rule
        response = client.put_rule(
            Name=rule_name,
            EventPattern=json.dumps(event_pattern),
            State='ENABLED',
            Description='Rule triggered by CodePipeline state change'
        )

        # Save the rule name to S3
        s3_client.put_object(
            Bucket=bucket_name,
            Key=rule_file,
            Body=json.dumps({"rule_name": rule_name})
        )

        print(f"Rule {rule_name} created and saved to S3.")

    except Exception as e:
        print(f"Error creating rule or saving to S3: {e}")

    return response
