import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Initialize AWS Clients
sqs_client = boto3.client("sqs")

# Update with your SQS Queue URL
queue_url = "https://sqs.us-east-1.amazonaws.com/123456789012345/DiningRequestsQueueexample"

# Valid locations and cuisines
VALID_LOCATIONS = ["jersey city", "new york", "brooklyn"]
VALID_CUISINES = ["chinese", "indian", "mexican"]

def lambda_handler(event, context):
    """
    Main Lambda handler for Lex V1.
    """
    logger.debug(f"Received event: {json.dumps(event)}")

    intent_name = event["currentIntent"]["name"]

    if intent_name == "GreetingIntent":
        return respond("Hi there! How can I assist you today?")
    
    elif intent_name == "ThankYouIntent":
        return respond("You're welcome! Let me know if you need anything else.")

    elif intent_name == "DiningSuggestionsIntent":
        return handle_dining_suggestions(event)

    return respond("Sorry, I didn't understand that.")

def handle_dining_suggestions(event):
    """
    Process DiningSuggestionsIntent and validate user inputs.
    """
    slots = event["currentIntent"]["slots"]

    location = slots.get("Location")
    cuisine = slots.get("Cuisine")
    dining_time = slots.get("DiningTime")
    num_people = slots.get("NumPeople")
    email = slots.get("Email")

    # Validate slots
    validation_result = validate_slots(location, cuisine, dining_time, num_people, email)

    # If validation fails, ask for missing slot
    if not validation_result["isValid"]:
        return elicit_slot(event, validation_result["violatedSlot"], validation_result["message"])

    # Push data to SQS Queue
    message_body = {
        "location": location,
        "cuisine": cuisine,
        "dining_time": dining_time,
        "num_people": num_people,
        "email": email
    }

    try:
        sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
        return respond(f"Thank you! I will email restaurant suggestions for {cuisine} food in {location} at {dining_time} for {num_people} people to {email}.")
    except Exception as e:
        logger.error(f"Error sending message to SQS: {str(e)}")
        return respond("Sorry, we encountered an error processing your request.")

def validate_slots(location, cuisine, dining_time, num_people, email):
    """
    Validate user input slots.
    """

    if not location:
        return {"isValid": False, "violatedSlot": "Location", "message": "Which city are you looking for restaurants in?"}
    
    if location.lower() not in VALID_LOCATIONS:
        return {"isValid": False, "violatedSlot": "Location", "message": f"Sorry, we only support recommendations in {', '.join(VALID_LOCATIONS)}. Please enter a valid city."}

    if not cuisine:
        return {"isValid": False, "violatedSlot": "Cuisine", "message": "What type of cuisine do you prefer?"}
    
    if cuisine.lower() not in VALID_CUISINES:
        return {"isValid": False, "violatedSlot": "Cuisine", "message": f"Sorry, we only support {', '.join(VALID_CUISINES)} cuisine. Please choose another option."}

    if not dining_time:
        return {"isValid": False, "violatedSlot": "DiningTime", "message": "What time would you like to dine?"}

    if not num_people:
        return {"isValid": False, "violatedSlot": "NumPeople", "message": "How many people will be dining?"}

    if not email:
        return {"isValid": False, "violatedSlot": "Email", "message": "Can you provide your email to receive restaurant recommendations?"}

    return {"isValid": True, "violatedSlot": None, "message": None}

def elicit_slot(event, slot_to_elicit, message):
    """
    Ask Lex to prompt the user for missing information.
    """
    return {
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": event["currentIntent"]["name"],
            "slots": event["currentIntent"]["slots"],
            "slotToElicit": slot_to_elicit,
            "message": {"contentType": "PlainText", "content": message}
        }
    }

def respond(message):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {"contentType": "PlainText", "content": message}
        }
    }
