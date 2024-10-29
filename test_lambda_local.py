import json
from lambda_function import lambda_handler

def test_lambda():
    # Simulate an event as if it were coming from an AWS Lambda invocation
    event = {
        "query": "What is LangGraph?"
    }
    context = {}  # Context is usually empty for simple tests

    # Call the Lambda handler directly
    response = lambda_handler(event, context)

    # Print the response for verification
    print("Lambda Response:", json.dumps(response, indent=2))

if __name__ == "__main__":
    test_lambda()

