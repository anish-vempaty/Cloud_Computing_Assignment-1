import requests
import json
from datetime import datetime

# Replace this with your actual Yelp API Key
API_KEY = "KEY"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}
BASE_URL = "https://api.yelp.com/v3/businesses/search"

# Locations and Cuisines to scrape
LOCATIONS = ["New York City", "Manhattan", "Jersey City"]
CUISINES = ["Chinese", "Indian", "Mexican"]
RESTAURANTS_PER_CUISINE = 20  # Yelp allows max 50 per request

# Store results
restaurant_data = []

def get_restaurants(cuisine, location):
    """Fetch restaurants from Yelp API based on cuisine & location."""
    params = {
        "term": f"{cuisine} restaurants",
        "location": location,
        "limit": RESTAURANTS_PER_CUISINE
    }
    
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("businesses", [])
    else:
        print(f"Yelp API Error ({response.status_code}): {response.json()}")
        return []

# Scrape restaurants
for location in LOCATIONS:
    for cuisine in CUISINES:
        print(f"🔍 Fetching {cuisine} restaurants in {location}...")
        restaurants = get_restaurants(cuisine, location)

        for restaurant in restaurants:
            restaurant_data.append({
                "business_id": restaurant["id"],
                "name": restaurant["name"],
                "address": restaurant["location"]["address1"],
                "city": restaurant["location"]["city"],
                "state": restaurant["location"]["state"],
                "zip_code": restaurant["location"]["zip_code"],
                "cuisine": cuisine,
                "rating": restaurant["rating"],
                "review_count": restaurant["review_count"],
                "latitude": restaurant["coordinates"]["latitude"],
                "longitude": restaurant["coordinates"]["longitude"],
                "insertedAtTimestamp": datetime.utcnow().isoformat()
            })

# Save to JSON file
with open("restaurants.json", "w") as file:
    json.dump(restaurant_data, file, indent=4)

print(f"Successfully scraped {len(restaurant_data)} restaurants!")
