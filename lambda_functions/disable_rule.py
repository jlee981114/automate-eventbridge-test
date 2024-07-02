import boto3

def lambda_handler(event, context):
    client = boto3.client('events')
    old_rule_name = 'old-event-pattern-rule'

    response = client.disable_rule(
        Name=old_rule_name
    )

    return response