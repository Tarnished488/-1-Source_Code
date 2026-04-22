import json
import urllib3

# Initialize the HTTP pool manager for REST calls
http = urllib3.PoolManager()

def lambda_handler(event, context):
    """
    Result Update Function:
    Acts as a bridge between Member C's validation results and our EC2 Data Service.
    It handles the AWS Lambda Function URL event structure by extracting the nested body.
    """
    print("Received raw event: " + json.dumps(event))
    
    # Target endpoint: Data Service running on port 5002
    DATA_SERVICE_ENDPOINT = "http://15.134.26.5:5002/data/update"
    
    try:
        # Step 1: Extract the actual business logic payload
        # AWS Lambda Function URL wraps the request body in a string under the 'body' key
        if 'body' in event and isinstance(event['body'], str):
            actual_payload = json.loads(event['body'])
            print(f"Parsed payload from body: {json.dumps(actual_payload)}")
        else:
            # Fallback if the event is already the dictionary (e.g., from a direct test)
            actual_payload = event
            print("Using event as payload directly")

        # Step 2: Forward the purified data to the Data Service via PATCH
        response = http.request(
            'PATCH',
            DATA_SERVICE_ENDPOINT,
            body=json.dumps(actual_payload),
            headers={'Content-Type': 'application/json'},
            timeout=5.0
        )
        
        print(f"Data Service Response Status: {response.status}")
        
        # Step 3: Return success response to the caller (Member C)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Database update request forwarded successfully',
                'data_service_status': response.status
            })
        }
        
    except Exception as e:
        print(f"Error processing update: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal Error',
                'details': str(e)
            })
        }