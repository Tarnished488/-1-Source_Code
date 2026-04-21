import json
import urllib3

# HTTP client for sending callback requests
http = urllib3.PoolManager()

def lambda_handler(event, context):

    # Parse input data (handle API Gateway format)
    if "body" in event:
        data = json.loads(event["body"])
    else:
        data = event

    title = data.get("title")
    description = data.get("description")
    filename = data.get("filename")
    submission_id = data.get("submissionId")  

    # Default result (assume valid)
    result = {
        "submissionId": submission_id,
        "status": "READY",
        "message": "All checks passed"
    }

    # Validation logic
    if not title or not description or not filename:
        result["status"] = "INCOMPLETE"
        result["message"] = "Missing required fields"

    elif len(description) < 30:
        result["status"] = "NEEDS REVISION"
        result["message"] = "Description too short"

    elif not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        result["status"] = "NEEDS REVISION"
        result["message"] = "Invalid file format"

    # Send result to Result Update Lambda
    try:
        update_url = "https://c4lljjdzqrahcygiyjjj3urbcy0nqylb.lambda-url.ap-southeast-2.on.aws/"  

        http.request(
            "POST",
            update_url,
            body=json.dumps(result),
            headers={"Content-Type": "application/json"},
            timeout=5.0
        )

        print("Callback sent:", result)

    except Exception as e:
        print("Callback failed:", str(e))

    # Return response
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }