import json
import urllib3
import boto3

# Initialize HTTP Manager
http = urllib3.PoolManager()

def lambda_handler(event, context):
    # 1. Log the full event for debugging in CloudWatch
    print("Full Event Received: " + json.dumps(event))
    
    for record in event['Records']:
        # Process only NEW records added to DynamoDB
        if record['eventName'] == 'INSERT':
            try:
                # 2. Extract the NewImage from DynamoDB Stream
                new_image = record['dynamodb']['NewImage']
                
                # 3. Clean and structure the data to send to Member C
                # We extract the 'S' (String) value from DynamoDB's format
                forward_data = {
                    "submissionId": new_image.get('submissionId', {}).get('S'),
                    "title": new_image.get('title', {}).get('S'),
                    "description": new_image.get('description', {}).get('S'),
                    "filename": new_image.get('filename', {}).get('S')
                }
                
                # Validation: Ensure submissionId exists before forwarding
                if not forward_data["submissionId"]:
                    print("Error: Missing submissionId in record, skipping...")
                    continue

                # 4. Target Member C's URL
                member_c_url = "https://urtr25eg3vabtnoiqkk2gpnk7i0lhter.lambda-url.ap-northeast-1.on.aws/"
                
                print(f"Forwarding sanitized data to Member C: {json.dumps(forward_data)}")
                
                # 5. Cross-account data forwarding (POST request)
                response = http.request(
                    'POST',
                    member_c_url,
                    body=json.dumps(forward_data),
                    headers={'Content-Type': 'application/json'},
                    timeout=5.0
                )
                
                print(f"Member C response status: {response.status}")
                
            except Exception as e:
                print(f"Error processing record: {str(e)}")
      
                
    return {
        'statusCode': 200,
        'body': json.dumps('Workflow notification processed successfully')
    }