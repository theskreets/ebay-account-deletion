from flask import Flask, request, jsonify
import hashlib
import os

app = Flask(__name__)

VERIFICATION_TOKEN = os.getenv("VERIFICATION_TOKEN")
ENDPOINT_URL = os.getenv("ENDPOINT_URL")

@app.route("/ebay/account-deletion", methods=["GET", "POST"])
def handle_account_deletion():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            return jsonify({"error": "Missing challenge_code"}), 400

        to_hash = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        hashed = hashlib.sha256(to_hash.encode("utf-8")).hexdigest()
        return jsonify({"challengeResponse": hashed}), 200

    data = request.get_json()
    if not data or data.get("verificationToken") != VERIFICATION_TOKEN:
        return jsonify({"error": "Invalid verification token"}), 403

    print("✅ Received account deletion:", data)
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(port=5000)
