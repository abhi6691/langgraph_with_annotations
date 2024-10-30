import boto3
import json
import os
import subprocess
import time

# Define parameters at the top for easy configuration
AWS_REGION = 'us-west-2'
ACCOUNT_ID = boto3.client('sts').get_caller_identity().get('Account')
FUNCTION_NAME = 'LangGraphLambdaFunction'
ROLE_NAME = 'LanggraphLambdaExecutionRole'
ECR_REPO_NAME = 'langgraph-lambda-repo'
DESCRIPTION = 'A Lambda function for hosting LangGraph applications with dynamic module loading'
TIMEOUT = 900
MEMORY_SIZE = 128
DOCKER_IMAGE_TAG = 'latest'
DOCKERFILE_PATH = './Dockerfile'
REQUIREMENTS_FILE = './requirements.txt'
LAMBDA_HANDLER_FILE = './src/lambda_function.py'
SLEEP_INTERVAL = 10

# Initialize AWS clients
lambda_client = boto3.client('lambda', region_name=AWS_REGION)
iam_client = boto3.client('iam')
ecr_client = boto3.client('ecr')

def create_lambda_role():
    try:
        assume_role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Service": "lambda.amazonaws.com"
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
        }

        # Create the IAM role
        response = iam_client.create_role(
            RoleName=ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description='Role for Lambda function hosting LangGraph applications'
        )

        # Attach the basic Lambda execution policy
        iam_client.attach_role_policy(
            RoleName=ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )

        print("IAM role created:", response)
        time.sleep(SLEEP_INTERVAL)  # Wait for role propagation

        return response['Role']['Arn']
    except iam_client.exceptions.EntityAlreadyExistsException:
        print("Role already exists. Retrieving existing role ARN.")
        role = iam_client.get_role(RoleName=ROLE_NAME)
        return role['Role']['Arn']

def create_ecr_repo():
    try:
        response = ecr_client.create_repository(repositoryName=ECR_REPO_NAME)
        print(f"ECR repository {ECR_REPO_NAME} created:", response)
        time.sleep(SLEEP_INTERVAL)  # Wait for ECR repo to be available
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        print(f"ECR repository {ECR_REPO_NAME} already exists.")
    
    return f"{ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/{ECR_REPO_NAME}:{DOCKER_IMAGE_TAG}"

def build_and_push_docker_image(image_uri):
    # Authenticate Docker with AWS ECR
    print("Authenticating Docker with AWS ECR...")
    subprocess.run(
        f"aws ecr get-login-password --region {AWS_REGION} | docker login --username AWS --password-stdin {ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com",
        shell=True, check=True
    )

    # Build the Docker image without cache
    print("Building Docker image with --no-cache...")
    subprocess.run([
        'docker', 'build', '--no-cache', '-t', image_uri, '-f', DOCKERFILE_PATH, '.'
    ], check=True)

    # Tag and push the Docker image to ECR
    print("Pushing Docker image to ECR...")
    subprocess.run([
        'docker', 'push', image_uri
    ], check=True)

def deploy_lambda_container(image_uri):
    def wait_for_update(function_name):
        while True:
            response = lambda_client.get_function(FunctionName=function_name)
            status = response['Configuration']['State']
            print(f"Current Lambda function status: {status}")

            # Break the loop if the function is Active
            if status == "Active":
                print("Lambda function is active and ready.")
                break
            elif status == "Failed":
                raise Exception("Lambda function update failed.")

            # Wait for a few seconds before polling again
            time.sleep(5)

    try:
        # Deploy the Lambda function with the container image
        response = lambda_client.create_function(
            FunctionName=FUNCTION_NAME,
            Role=create_lambda_role(),  # Create or get role ARN
            Code={'ImageUri': image_uri},
            PackageType='Image',
            Description=DESCRIPTION,
            Timeout=TIMEOUT,
            MemorySize=MEMORY_SIZE,
            Publish=True
        )
        print("Lambda function created:", response)
    except lambda_client.exceptions.ResourceConflictException:
        # If the function already exists, update it
        response = lambda_client.update_function_code(
            FunctionName=FUNCTION_NAME,
            ImageUri=image_uri,
            Publish=True
        )
        print("Lambda function update initiated:", response)

    # Wait for the function to reach the "Active" state
    wait_for_update(FUNCTION_NAME)

def main():
    # Check that required files exist
    if not os.path.exists(DOCKERFILE_PATH) or not os.path.exists(REQUIREMENTS_FILE) or not os.path.exists(LAMBDA_HANDLER_FILE):
        print("Error: Required files (Dockerfile, requirements.txt, lambda_function.py) not found.")
        return

    # Step 1: Create the ECR repository
    image_uri = create_ecr_repo()

    # Step 2: Build and push the Docker image to ECR
    build_and_push_docker_image(image_uri)

    # Step 3: Deploy the Lambda function using the container image
    deploy_lambda_container(image_uri)

if __name__ == "__main__":
    main()
