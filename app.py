from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

# Create Flask app
app = Flask(__name__)

# Generate a key for Fernet encryption/decryption
# Ideally, this should be stored securely and should not be regenerated each time the app runs.
key = Fernet.generate_key()
cipher = Fernet(key)


# POST route to encrypt data
@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        # Get data from the POST request
        data = request.get_json()

        # Extract the text to be encrypted
        text = data.get("text", "")

        if not text:
            return jsonify({"error": "No text provided"}), 400

        # Encrypt the text using Fernet
        encrypted_text = cipher.encrypt(text.encode()).decode()

        return jsonify({
            "encrypted_text": encrypted_text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# POST route to decrypt data
@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        # Get data from the POST request
        data = request.get_json()

        # Extract the encrypted text
        encrypted_text = data.get("encrypted_text", "")

        if not encrypted_text:
            return jsonify({"error": "No encrypted text provided"}), 400

        # Decrypt the text using Fernet
        decrypted_text = cipher.decrypt(encrypted_text.encode()).decode()

        return jsonify({
            "decrypted_text": decrypted_text
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
