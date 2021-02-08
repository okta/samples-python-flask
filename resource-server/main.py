import json
import time

from flask import Flask, request
from flask_cors import CORS

from helpers import is_access_token_valid, config


app = Flask(__name__)
CORS(app)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
})


def is_authorized(request):
    """Get access token from authorization header."""
    try:
        token = request.headers.get("Authorization").split("Bearer ")[1]
        return is_access_token_valid(token, config["issuer"], config["client_id"])
    except Exception:
        return False


@app.route("/")
def home():
    return "Hello!  There's not much to see here." \
           "Please grab one of our front-end samples for use with this sample resource server"


@app.route("/api/messages")
def messages():
    if not is_authorized(request):
        return "Unauthorized", 401

    response = {
        'messages': [
            {
                'date': time.time(),
                'text': 'I am a robot.'
            },
            {
                'date': time.time()-3600,
                'text': 'Hello, World!'
            }
        ]
    }

    return json.dumps(response)


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
