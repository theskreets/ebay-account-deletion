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

@app.route("/")
def home():
    return "✅ TCGTrack backend is running. Nothing to see here."


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

