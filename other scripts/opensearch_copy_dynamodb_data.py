import boto3
import json
from opensearchpy import OpenSearch, RequestsHttpConnection

# ✅ AWS Resources
DYNAMODB_TABLE = "yelp-restaurants"
OPENSEARCH_HOST = "search-resturant-search-somethingsomething.aos.us-east-1.on.aws"
OPENSEARCH_INDEX = "restaurants"

# ✅ OpenSearch Client
opensearch_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": 443}],
    http_auth=("Username", "Password"),  # Use OpenSearch login credentials
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)

# ✅ DynamoDB Client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE)

def get_dynamodb_data():
    """Retrieve all restaurant data from DynamoDB."""
    response = table.scan()  # Scan entire table (use with caution for large datasets)
    return response.get("Items", [])

def send_to_opensearch(data):
    """Insert restaurant data into OpenSearch."""
    for restaurant in data:
        doc = {
            "RestaurantID": restaurant["id"],  # Adjust key names if needed
            "Cuisine": restaurant["cuisine"]
        }
        
        # Send data to OpenSearch
        response = opensearch_client.index(index=OPENSEARCH_INDEX, body=doc)
        print(f"Inserted {restaurant['id']} → {response}")

if __name__ == "__main__":
    restaurants = get_dynamodb_data()
    print(f"Retrieved {len(restaurants)} restaurants from DynamoDB.")
    
    send_to_opensearch(restaurants)
    print("✅ Data transfer complete!")
