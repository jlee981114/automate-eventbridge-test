import boto3

def create_sagemaker_endpoint():
    sagemaker_client = boto3.client('sagemaker', region_name='us-east-1')

    # Define endpoint configuration
    response = sagemaker_client.create_endpoint_config(
        EndpointConfigName='MyEndpointConfig',
        ProductionVariants=[
            {
                'VariantName': 'AllTrafficVariant',
                'ModelName': 'MyModel',
                'InstanceType': 'ml.m5.large',
                'InitialInstanceCount': 1,
                'InitialVariantWeight': 1.0
            }
        ]
    )
    print("Endpoint configuration created:", response)

    # Create endpoint
    response = sagemaker_client.create_endpoint(
        EndpointName='MyEndpoint',
        EndpointConfigName='MyEndpointConfig'
    )
    print("Endpoint created:", response)

if __name__ == '__main__':
    create_sagemaker_endpoint()
