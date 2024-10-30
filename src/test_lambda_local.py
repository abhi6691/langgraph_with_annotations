import boto3
import json
import argparse

# Initialize the Lambda client
lambda_client = boto3.client('lambda')

def test_lambda(query):
    # Define the event with the query from the command line
    event = {
        "query": query
    }

    try:
        # Invoke the deployed Lambda function
        response = lambda_client.invoke(
            FunctionName='LangGraphLambdaFunction',  # The name of the deployed Lambda function
            InvocationType='RequestResponse',
            Payload=json.dumps(event)
        )

        # Read and parse the response payload
        response_payload = response['Payload'].read()
        response_data = json.loads(response_payload)
        
        # Print the response for verification
        print("Lambda Response:", json.dumps(response_data, indent=2))

    except Exception as e:
        print("Error invoking Lambda function:", e)

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Invoke Lambda function with a query.")
    parser.add_argument("query", type=str, help="The query to send to the Lambda function")

    # Parse command line arguments
    args = parser.parse_args()

    # Call test_lambda with the query argument
    test_lambda(args.query)
