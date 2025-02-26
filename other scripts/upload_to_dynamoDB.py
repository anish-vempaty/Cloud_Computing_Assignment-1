import json
import boto3
from decimal import Decimal
from datetime import datetime

# ✅ Load JSON file
with open("restaurants.json", "r") as file:
    restaurant_data = json.load(file)

# ✅ Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("yelp-restaurants")

def convert_to_decimal(item):
    """Convert float values to Decimal for DynamoDB compatibility."""
    for key, value in item.items():
        if isinstance(value, float):
            item[key] = Decimal(str(value))
    return item

def upload_to_dynamodb():
    """Batch upload restaurants to DynamoDB."""
    with table.batch_writer() as batch:
        for restaurant in restaurant_data:
            item = {
                "id": restaurant["business_id"],  # ✅ Using `business_id` as `id`
                "name": restaurant["name"],
                "address": restaurant.get("address", "Unknown"),
                "city": restaurant.get("city", "Unknown"),
                "state": restaurant.get("state", "Unknown"),
                "zip_code": restaurant.get("zip_code", "Unknown"),
                "cuisine": restaurant["cuisine"],
                "rating": Decimal(str(restaurant.get("rating", 0))),  # Ensure Decimal format
                "review_count": Decimal(str(restaurant.get("review_count", 0))),
                "latitude": Decimal(str(restaurant.get("latitude", 0.0))),
                "longitude": Decimal(str(restaurant.get("longitude", 0.0))),
                "insertedAtTimestamp": datetime.utcnow().isoformat()
            }
            batch.put_item(Item=item)
    
    print(f"✅ Uploaded {len(restaurant_data)} restaurants to DynamoDB.")

# ✅ Run upload
upload_to_dynamodb()
