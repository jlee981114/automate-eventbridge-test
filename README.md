# AWS Lambda and EventBridge Automation with GitHub Actions

This repository contains a sample setup to automate the creation and management of EventBridge rules using GitHub Actions, Lambda, and CloudFormation.

## Folder Structure

- `.github/workflows/deploy.yml`: GitHub Actions workflow file.
- `notebooks/test_notebook.ipynb`: Sample Jupyter notebook for SageMaker inference.
- `lambda_functions/`: Directory containing Lambda function code.
  - `lambda_function.py`: Lambda function to create EventBridge rules.
  - `disable_rule.py`: Lambda function to disable old EventBridge rules.
- `cloudformation_template.yaml`: CloudFormation template to deploy Lambda functions.
- `requirements.txt`: Dependencies for Lambda functions.
- `README.md`: This file.

## Setup Instructions

1. **Configure GitHub Secrets**:
   - Add your AWS credentials to GitHub Secrets (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`).

2. **Modify Parameters**:
   - Update the `cloudformation_template.yaml` and `deploy.yml` files with your specific details (S3 bucket, IAM roles, etc.).

3. **Deploy**:
   - Push changes to the `main` branch to trigger the GitHub Actions workflow.
