from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

# Make sure this exactly matches what you enter in the eBay Developer Portal
VERIFICATION_TOKEN = "N4a7cB1xL9Z0Qw2eVtX6RmYu83KdFgHo"
ENDPOINT_URL = "https://3911-24-158-188-105.ngrok-free.app/ebay/account-deletion"

@app.route("/ebay/account-deletion", methods=["GET", "POST"])
def handle_account_deletion():
    if request.method == "GET":
        challenge_code = request.args.get("challenge_code")
        if not challenge_code:
            return jsonify({"error": "Missing challenge_code"}), 400

        # Concatenate and hash: challengeCode + verificationToken + endpoint
        to_hash = challenge_code + VERIFICATION_TOKEN + ENDPOINT_URL
        hashed = hashlib.sha256(to_hash.encode("utf-8")).hexdigest()

        return jsonify({"challengeResponse": hashed}), 200

    # Handle real POST notifications here if needed later
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    app.run(port=5000)
