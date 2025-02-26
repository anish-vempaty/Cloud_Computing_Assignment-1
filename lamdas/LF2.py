import json
import boto3
import logging
import requests
import random
from requests.auth import HTTPBasicAuth
from boto3.dynamodb.conditions import Key

# OpenSearch Configuration
OS_USERNAME = "Username"  # Your OpenSearch username
OS_PASSWORD = "Password"  # Your OpenSearch password
OPENSEARCH_HOST = "search-resturant-search-somethingsomethingsome.aos.us-east-1.on.aws"
OPENSEARCH_URL = f"https://{OPENSEARCH_HOST}/restaurants/_search"

# AWS Clients
sqs_client = boto3.client("sqs")
sns_client = boto3.client("sns")
dynamodb = boto3.resource("dynamodb")

# AWS Resources
QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012345/DiningRequestsQueueexample"
DYNAMO_TABLE = "yelp-restaurants"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:123456789012345:DiningRecommendationsexample"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def query_opensearch(cuisine):
    """
    🔍 Search for restaurant IDs in OpenSearch by cuisine using requests, with randomization.
    """
    headers = {"Content-Type": "application/json"}
    query = {
        "size": 10,  # Get more than needed and shuffle
        "query": {
            "function_score": {
                "query": {
                    "match": {
                        "Cuisine": cuisine
                    }
                },
                "random_score": {}  # Adds randomness to OpenSearch ranking
            }
        }
    }

    try:
        response = requests.get(
            OPENSEARCH_URL,
            headers=headers,
            auth=HTTPBasicAuth(OS_USERNAME, OS_PASSWORD),
            json=query
        )

        if response.status_code != 200:
            logger.error(f"OpenSearch query failed: {response.status_code} - {response.text}")
            return []

        hits = response.json().get("hits", {}).get("hits", [])
        restaurant_ids = [hit["_source"]["RestaurantID"] for hit in hits]

        logger.info(f"OpenSearch found {len(restaurant_ids)} restaurants for cuisine {cuisine}")
        return restaurant_ids

    except Exception as e:
        logger.error(f"OpenSearch query error: {e}")
        return []

def query_dynamodb(restaurant_ids):
    """
    Retrieve restaurant details from DynamoDB using IDs from OpenSearch.
    """
    table = dynamodb.Table(DYNAMO_TABLE)
    restaurants = []

    for rid in restaurant_ids:
        try:
            response = table.query(
                KeyConditionExpression=Key("id").eq(rid)
            )
            restaurants.extend(response.get("Items", []))

        except Exception as e:
            logger.error(f"Error fetching restaurant ID {rid} from DynamoDB: {e}")

    # Shuffle the results before returning to randomize selection
    random.shuffle(restaurants)
    logger.info(f"Found {len(restaurants)} restaurants in DynamoDB.")
    
    # Return only the top 5 randomly shuffled restaurants
    return restaurants[:5]

def send_email(email, cuisine, location, dining_time, num_people, recommendations):
    """
    Format and send restaurant recommendations via SNS.
    """
    if not recommendations:
        message = f"Sorry, we couldn't find any {cuisine} restaurants in {location}."
    else:
        message = (
            f"Hello! Here are some {cuisine} restaurant recommendations in {location} "
            f"for {num_people} people at {dining_time}:\n\n"
        )
        for idx, restaurant in enumerate(recommendations, start=1):
            message += (
                f"{idx}. {restaurant['name']} - {restaurant['address']} "
                f"(Rating: {restaurant.get('rating', 'N/A')}/5, Reviews: {restaurant.get('review_count', 'N/A')})\n"
            )

        message += "\nEnjoy your meal!"

    sns_client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Your Restaurant Recommendations"
    )

    logger.info(f"📩 Email sent to {email}")

def lambda_handler(event, context):
    """
    Main Lambda function for processing dining requests automatically from SQS.
    """
    logger.info(f"📝 Event received: {json.dumps(event)}")

    if "Records" not in event:
        logger.info("⚠ No messages in the queue.")
        return {"statusCode": 200, "body": "No messages to process."}

    for record in event["Records"]:
        body = json.loads(record["body"])

        if "Type" in body and body["Type"] == "Notification":
            logger.info("⚠ Skipping SNS notification message.")
            continue  # Ignore SNS messages

        email = body["email"]
        cuisine = body["cuisine"].title()
        location = body["location"].title()
        dining_time = body["dining_time"]
        num_people = body["num_people"]

        # Query OpenSearch to get restaurant IDs
        restaurant_ids = query_opensearch(cuisine)

        # Query DynamoDB for restaurant details
        recommendations = query_dynamodb(restaurant_ids)

        # Send email with restaurant suggestions
        send_email(email, cuisine, location, dining_time, num_people, recommendations)

    return {"statusCode": 200, "body": "Processed SQS messages and sent emails."}