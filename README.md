Simple langgraph application with a single query node. Uses OpenAI model to answer the questions.

### Setup
1. Update `api_key` in `customer_app.py`
2. Execute `python3 lambda_deployer.py`
3. Execute `python3 src/test_lambda_local.py "What are Bedrock Agents?"`