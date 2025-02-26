# Other Scripts

This folder contains additional scripts used for data collection and processing.

## Scripts

### 1. `yelp-api.py`
- Fetches restaurant data from the Yelp API.
- Stores restaurant data in a JSON file for further processing.

### 2. `upload_to_dynamoDB.py`
- Uploads restaurant data to the `yelp-restaurants` DynamoDB table.
- Reads from a JSON file and inserts data into the database.

### 3. `opensearch_copy_dynamodb_data.py`
- Copies restaurant data from DynamoDB to OpenSearch.
- Extracts only necessary fields (RestaurantID and Cuisine) to store in OpenSearch.

## Usage
- Run each script locally with valid API keys and credentials.
- Ensure that your AWS credentials are correctly configured for DynamoDB and OpenSearch access and configured in your local AWS cli.
