# Start with an official AWS Lambda base image for Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Copy function code and requirements into the container
COPY src/ ${LAMBDA_TASK_ROOT}
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install dependencies
RUN pip install -r requirements.txt

# Command to run the Lambda function
CMD ["lambda_function.lambda_handler"]

