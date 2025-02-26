# Lambda Functions

This folder contains all AWS Lambda functions used in the Dining Concierge chatbot application.

## Functions

### 1. LF0.py
- Handles chat interactions with the Lex bot.
- Integrates with Lex to process user messages.

### 2. LF1.py
- Validates user input and pushes dining requests to an SQS queue.
- Ensures correct format before sending data.

### 3. LF2.py
- Acts as a queue worker.
- Pulls requests from SQS, queries OpenSearch for restaurant recommendations, retrieves full details from DynamoDB, and sends an email with restaurant suggestions.

## Deployment
- Each Lambda function should be deployed individually.
- Ensure that the necessary IAM permissions are attached to each function.
- Set up triggers for SQS and Lex as required.
