# 🍽️ Dining Concierge Chatbot - Cloud Computing Assignment 1 (NYU)

This project is a **serverless, microservice-driven web application** that implements a **Dining Concierge Chatbot**. The chatbot interacts with users, collects dining preferences, and provides personalized restaurant recommendations via email.

## 🚀 Features
- **Frontend**: React-based UI hosted on **AWS S3**.
- **Chatbot**: Built using **Amazon Lex** to handle user queries.
- **Backend**: Uses **AWS Lambda**, **API Gateway**, **DynamoDB**, and **OpenSearch**.
- **Asynchronous Processing**: **SQS queues** for message handling and **Lambda functions** for processing.
- **Data Storage**: Restaurants' data is stored in **DynamoDB** and indexed in **OpenSearch**.
- **Email Notifications**: Sends restaurant recommendations via **Amazon SNS**.

---

## 📂 Repository Structure

```
├── frontend/               # Frontend code (React app)
├── lambdafunctions/        # AWS Lambda functions (LF0, LF1, LF2)
├── otherscripts/           # Scripts for data processing (Yelp API, DynamoDB, OpenSearch)
└── README.md               # Project documentation
```

### 🔹 `frontend/`
- **Contains:** React-based chatbot UI.
- **Deployment:** Hosted in **AWS S3** with CORS enabled.

### 🔹 `lambdafunctions/`
- **LF0.py**: API Gateway & Lex integration.
- **LF1.py**: Pushes user dining requests to **SQS**.
- **LF2.py**: Processes messages from SQS, fetches restaurants from **OpenSearch & DynamoDB**, and sends recommendations via **SNS**.

### 🔹 `otherscripts/`
- **`yelp-api.py`**: Scrapes restaurant data from **Yelp API**.
- **`upload_to_dynamoDB.py`**: Uploads restaurant data to **DynamoDB**.
- **`opensearch_copy_dynamodb_data.py`**: Copies restaurant data from **DynamoDB to OpenSearch**.

---

## 🛠️ Setup Instructions

### 1️⃣ Deploy the Frontend
1. Navigate to the `frontend/` folder.
2. Deploy the frontend to an **S3 bucket**:
   ```sh
   aws s3 sync ./build s3://your-s3-bucket-name --acl public-read
   ```
3. Enable **Static Website Hosting** in **S3 settings**.

### 2️⃣ Set Up AWS Services
- Create an **Amazon Lex bot** with intents:
  - `GreetingIntent`
  - `DiningSuggestionsIntent`
  - `ThankYouIntent`
- Create an **API Gateway** and integrate with **LF0 (Lex Handler)**.
- Set up **SQS**, **SNS**, and **DynamoDB** tables.

### 3️⃣ Deploy Lambda Functions
1. Navigate to `lambdafunctions/`.
2. Deploy each function using AWS CLI:
   ```sh
   zip function.zip LF1.py
   aws lambda update-function-code --function-name LF1 --zip-file fileb://function.zip
   ```
3. Attach required IAM permissions for **SQS, SNS, DynamoDB, and OpenSearch**.

### 4️⃣ Upload and Index Restaurant Data
1. Fetch restaurant data from Yelp:
   ```sh
   python otherscripts/yelp-api.py
   ```
2. Upload data to DynamoDB:
   ```sh
   python otherscripts/upload_to_dynamoDB.py
   ```
3. Copy restaurant data to OpenSearch:
   ```sh
   python otherscripts/opensearch_copy_dynamodb_data.py
   ```

---

## 📌 Contributors
- **Anish Vempaty**
- **Spandan Mishra**

## 📜 License
This project is for **NYU Cloud Computing Course (Spring 2025)**.
