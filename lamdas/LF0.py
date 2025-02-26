import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Initialize Lex Client
lex_client = boto3.client("lex-runtime")

def lambda_handler(event, context):
    """
    API Gateway receives a message from the frontend, sends it to Lex, and returns the Lex response.
    """
    logger.debug(f"Received API event: {json.dumps(event)}")

    body = json.loads(event["body"])  # Get request body
    user_message = body.get("messages", [{}])[0].get("unstructured", {}).get("text", "")

    if not user_message:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request, no text provided."})
        }

    try:
        # Send message to Lex
        lex_response = lex_client.post_text(
            botName="DiningConciergeBot",
            botAlias="$LATEST",
            userId="user-test",
            inputText=user_message
        )

        lex_message = lex_response["message"]

        return {
            "statusCode": 200,
            "body": json.dumps({"messages": [{"type": "unstructured", "unstructured": {"text": lex_message}}]}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    except Exception as e:
        logger.error(f"Error communicating with Lex: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error, please try again later."})
        }
