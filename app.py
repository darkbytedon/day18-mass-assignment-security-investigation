from flask import Flask, request, jsonify

app = Flask(__name__)

users = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "role": "user",
        "is_admin": False
    }
}

@app.get("/api/profile")
def get_profile():
    return jsonify(users["alice"])

@app.patch("/api/profile")
def update_profile():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Invalid or empty request"}), 400

    # Only email is allowed to be updated.
    allowed_fields = {"email"}

    # Reject unexpected fields.
    unexpected_fields = set(data.keys()) - allowed_fields

    if unexpected_fields:
        return jsonify({
            "error": "You cannot update these fields",
            "rejected_fields": sorted(unexpected_fields)
        }), 400

    # Validate email input.
    if not isinstance(data["email"], str) or not data["email"].strip():
        return jsonify({"error": "Invalid email"}), 400

    # Update only the permitted field.
    users["alice"]["email"] = data["email"].strip()

    return jsonify({
        "message": "Profile updated successfully",
        "profile": users["alice"]
    })

if __name__ == "__main__":
    app.run(debug=True)
