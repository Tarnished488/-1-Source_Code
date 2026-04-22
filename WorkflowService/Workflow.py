import uuid
import urllib3
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
http = urllib3.PoolManager()

# Data Service endpoint running on the same host but different port
DATA_SERVICE_URL = "http://15.134.26.5:5002/data"

@app.route('/workflow/submit', methods=['POST'])
def submit():
    """
    Handles initial submission from Member A.
    Generates a unique ID and offloads storage to the Data Service.
    """
    data = request.json
    # Generate a unique Correlation ID for the entire lifecycle
    submission_id = str(uuid.uuid4())

    # Construct the data payload for persistence
    payload = {
        'submissionId': submission_id,
        'title': data.get('title'),
        'description': data.get('description'),
        'filename': data.get('filename'),
        'status': 'PENDING'
    }

    # Invoke Data Service to persist the record via internal REST call
    http.request(
   'POST',
        f"{DATA_SERVICE_URL}/save",
        body=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    return jsonify({"id": submission_id, "status": "PENDING"}), 200

@app.route('/workflow/status/<submission_id>', methods=['GET'])
def status(submission_id):
    """
    Facilitates status polling for Member A.
    Proxies the request to the Data Service to fetch the current record state.
    """
    # Query Data Service for the latest state of the specific submission
    resp = http.request('GET', f"{DATA_SERVICE_URL}/get/{submission_id}")

    # Return the raw response data and status code back to the frontend
    return resp.data, resp.status

if __name__ == '__main__':
    # Workflow Service listens on port 5001
    app.run(host='0.0.0.0', port=5001)