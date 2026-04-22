from flask import Flask, request, jsonify
import boto3

app = Flask(__name__)
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('PostersTable')

# save
@app.route('/data/save', methods=['POST'])
def save_data():
    data = request.json
    table.put_item(Item=data)
    return jsonify({"status": "success"}), 200

# load
@app.route('/data/get/<submission_id>', methods=['GET'])
def get_data(submission_id):
    response = table.get_item(Key={'submissionId': submission_id})
    return jsonify(response.get('Item', {})), 200

# update
@app.route('/data/update', methods=['PATCH'])
def update_data():
    data = request.json
    table.update_item(
        Key={'submissionId': data['submissionId']},
        UpdateExpression="set #s = :s, #m = :m",
        ExpressionAttributeNames={'#s': 'status', '#m': 'message'},
        ExpressionAttributeValues={':s': data['status'], ':m': data['message']}
    )
    return jsonify({"status": "updated"}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)