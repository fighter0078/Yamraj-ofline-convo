from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Replace these with your real tokens
PAGE_ACCESS_TOKEN = "YOUR_PAGE_ACCESS_TOKEN"
VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"

def send_message(recipient_id, text):
    """Send a message to the user via Facebook Messenger."""
    url = 'https://graph.facebook.com/v13.0/me/messages'
    headers = {'Content-Type': 'application/json'}
    params = {'access_token': PAGE_ACCESS_TOKEN}
    data = {
        'recipient': {'id': recipient_id},
        'message': {'text': text}
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    print("Message sent:", response.text)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification for Facebook
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args.get('hub.challenge')
        return 'Invalid verification token', 403

    if request.method == 'POST':
        # Handle incoming messages
        data = request.get_json()
        print("Received data:", data)

        for entry in data.get('entry', []):
            for event in entry.get('messaging', []):
                if 'message' in event:
                    sender_id = event['sender']['id']
                    message_text = event['message'].get('text')
                    if message_text:
                        send_message(sender_id, f"You said: {message_text}")
        return 'ok', 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
