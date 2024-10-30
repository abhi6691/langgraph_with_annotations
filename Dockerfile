# Stage 1: Build dependencies in a temporary container
FROM public.ecr.aws/lambda/python:3.11 AS builder

# Copy requirements file for installing dependencies
COPY requirements.txt /tmp/

# Install dependencies into a temporary location to reduce final image size
RUN pip install --no-cache-dir --target=/tmp/python -r /tmp/requirements.txt

# Stage 2: Final image with only the necessary files
FROM public.ecr.aws/lambda/python:3.11

# Copy only the necessary dependencies from the builder stage
COPY --from=builder /tmp/python ${LAMBDA_TASK_ROOT}

# Copy application code
COPY src/ ${LAMBDA_TASK_ROOT}

# Remove pip cache to save space
RUN rm -rf /root/.cache/pip \
    && find ${LAMBDA_TASK_ROOT} -name '*.pyc' -delete \
    && find ${LAMBDA_TASK_ROOT} -type d -name '__pycache__' -exec rm -rf {} +

# Set the Lambda function handler
CMD ["lambda_function.lambda_handler"]
