from flask import Flask, request
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'YOUR_PAGE_ACCESS_TOKEN'
VERIFY_TOKEN = 'my_verify_token'

@app.route('/', methods=['GET'])
def verify():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        return challenge
    return 'Verification token mismatch', 403

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    for entry in data.get('entry', []):
        for message in entry.get('messaging', []):
            sender_id = message['sender']['id']
            if 'message' in message:
                text = message['message'].get('text')
                reply(sender_id, "Բարև, ինչով կարող եմ օգնել ձեզ?")
    return "ok", 200

def reply(sender_id, message_text):
    payload = {
        'recipient': {'id': sender_id},
        'message': {'text': message_text}
    }
    auth = {'access_token': PAGE_ACCESS_TOKEN}
    requests.post('https://graph.facebook.com/v18.0/me/messages',
                  params=auth, json=payload)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

