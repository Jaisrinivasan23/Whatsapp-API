from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# Your Meta Page Access Token
PAGE_ACCESS_TOKEN = ''
VERIFY_TOKEN = ''

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verification process for the Facebook Webhook
        verify_token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if verify_token == VERIFY_TOKEN:
            return challenge
        return 'Verification token mismatch', 403

    if request.method == 'POST':
        # Handling messages from users
        data = request.get_json()
        for entry in data.get('entry', []):
            for messaging_event in entry.get('messaging', []):
                sender_id = messaging_event['sender']['id']
                if 'message' in messaging_event:
                    message_text = messaging_event['message'].get('text', '')
                    process_user_message(sender_id, message_text)
        return 'OK', 200

def process_user_message(sender_id, message_text):
    # Example auto-reply logic
    if message_text.lower() == 'hi' or message_text.lower() == 'hii':
        send_message(sender_id, 'Hi there!')
    elif message_text.lower() == 'how are you?':
        send_message(sender_id, "I'm doing well, thank you!")
    elif message_text.lower() == 'bye':
        send_message(sender_id, 'Goodbye!')
    elif message_text.lower() == 'help':
        send_message(sender_id, 'How can I help you?')
    elif message_text.lower() == 'what is your name?':
        send_message(sender_id, 'I am a bot, created by your_name')

def send_message(recipient_id, message_text):
    url = f'https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}'
    payload = {
        'recipient': {'id': recipient_id},
        'message': {'text': message_text}
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        logging.error(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")
    
if __name__ == '__main__':
    app.run(debug=True)
