import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('events')
    rule_name = 'new-event-pattern-rule'
    event_pattern = {
        "source": ["aws.codepipeline"],
        "detail-type": ["CodePipeline Pipeline Execution State Change"],
        "detail": {
            "state": ["SUCCEEDED"]
        }
    }

    response = client.put_rule(
        Name=rule_name,
        EventPattern=json.dumps(event_pattern),
        State='ENABLED',
        Description='Rule triggered by CodePipeline state change'
    )

    return response
