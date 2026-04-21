import json
from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)


WORKFLOW_BASE_URL = "http://15.134.26.5:5001"
WORKFLOW_SUBMIT_URL = f"{WORKFLOW_BASE_URL}/workflow/submit"
WORKFLOW_STATUS_URL_TEMPLATE = f"{WORKFLOW_BASE_URL}/workflow/status/{{submission_id}}"


def build_result_data(payload, http_status_code, default_status="PENDING"):
    if isinstance(payload, dict) and "body" in payload:
        outer_status_code = payload.get("statusCode", http_status_code)
        raw_body = payload.get("body", "{}")

        if isinstance(raw_body, str):
            try:
                body_data = json.loads(raw_body)
            except json.JSONDecodeError:
                body_data = {"raw_body": raw_body}
        elif isinstance(raw_body, dict):
            body_data = raw_body
        else:
            body_data = {"raw_body": str(raw_body)}

        return {
            "http_status_code": http_status_code,
            "service_status_code": outer_status_code,
            "submission_id": body_data.get("id", body_data.get("submissionId")),
            "status": body_data.get("status", default_status),
            "message": body_data.get("message", "No message returned"),
            "raw_response": payload
        }

    submission_id = payload.get("id") if isinstance(payload, dict) else None
    if isinstance(payload, dict):
        submission_id = payload.get("submissionId", submission_id)

    message = "Submission accepted by workflow service"
    if isinstance(payload, dict):
        message = payload.get("message", payload.get("error", message))

    return {
        "http_status_code": http_status_code,
        "service_status_code": http_status_code,
        "submission_id": submission_id,
        "status": payload.get("status", default_status) if isinstance(payload, dict) else default_status,
        "message": message,
        "raw_response": payload
    }


def parse_response_payload(response, default_status="PENDING"):
    payload = response.json()
    return build_result_data(payload, response.status_code, default_status=default_status)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    filename = request.form.get("filename", "").strip()

    payload = {
        "title": title,
        "description": description,
        "filename": filename
    }

    try:
        response = requests.post(
            WORKFLOW_SUBMIT_URL,
            json=payload,
            timeout=10
        )

        print("===== DEBUG POST RESPONSE =====", flush=True)
        print("status code:", response.status_code, flush=True)
        print("response text:", response.text, flush=True)

        response.raise_for_status()
        result_data = parse_response_payload(response)
        result_data["submitted_payload"] = payload

        return render_template(
            "result.html",
            error=None,
            result=result_data
        )

    except requests.exceptions.RequestException as e:
        return render_template(
            "result.html",
            error=f"can not connect Workflow Service：{e}",
            result=None
        )
    except Exception as e:
        return render_template(
            "result.html",
            error=f"wrong：{e}",
            result=None
        )


@app.route("/status/<submission_id>", methods=["GET"])
def status(submission_id):
    try:
        response = requests.get(
            WORKFLOW_STATUS_URL_TEMPLATE.format(submission_id=submission_id),
            timeout=10
        )
        response.raise_for_status()
        result_data = parse_response_payload(response, default_status="PENDING")
        return jsonify(result_data)
    except requests.exceptions.RequestException as e:
        return jsonify({
            "ok": False,
            "error": f"can not have status：{e}"
        }), 502
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": f"can not have status：{e}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
