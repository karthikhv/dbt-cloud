<<<<<<< HEAD
Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
=======
# aws-s3-handlers
Serverless Data Ingestion Microservice (AWS S3 Handler)

This project contains a foundational AWS Lambda function designed to demonstrate event-driven architecture. The Lambda function is triggered automatically whenever a new file (object) is uploaded to a specified Amazon S3 bucket.

This type of function is a common starting point for real-time data ingestion pipelines, allowing subsequent processing steps to be dynamically executed based on the uploaded file's characteristics.

🚀 Key Functionality

Event Triggering: Automatically executes upon an S3 s3:ObjectCreated:* event.

Metadata Retrieval: Safely retrieves the bucket name and the URL-decoded file key (path).

Content Verification: Makes a lightweight call to S3 (s3.get_object) to determine the file's Content-Type (MIME type, e.g., image/png, application/pdf).

Logging: Logs the file name and its content type to AWS CloudWatch, confirming successful ingestion and verification.

🛠️ AWS Services Used

AWS Lambda: Serverless compute environment to run the Python code.

Amazon S3: Used for source data storage and as the event trigger mechanism.

Boto3 (Python SDK): Used within the Lambda function to interact with the S3 API.

Amazon CloudWatch: Used to capture the execution logs (print statements) and monitor function performance.

👨‍💻 How to Deploy

This code is intended to be deployed as an AWS Lambda function with the following configuration:

Runtime: Python 3.x

Handler: s3_event_handler.lambda_handler

IAM Role: The execution role for the Lambda function MUST have the s3:GetObject permission on the specific S3 bucket where the files will be uploaded.

Trigger: An S3 Trigger must be configured on the source bucket to invoke the Lambda function upon Object Create (All) events.

This script is a foundation. In a production environment, the next step would be to add logic to process the data, such as converting CSV to Parquet or sending a notification to another service.
>>>>>>> 24a6e6df01187c029042140b48b021bfc647d2a9
