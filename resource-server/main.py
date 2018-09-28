import json
import time

from flask import Flask, render_template, url_for, redirect
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ["openid", "profile", "email"],
    'OIDC_CALLBACK_ROUTE': '/authorization-code/callback'
})

oidc = OpenIDConnect(app)


@app.route("/")
def home():
    return "Please grab one of our front-end samples for use with this sample resource server"


@app.route("/api/messages")
@oidc.accept_token(True)
def messages():
    api_response = []

    messages = dict()

    message1 = dict()
    message1['date'] = time.time()
    message1['text'] = 'I am a robot.'
    api_response.append(message1)

    message2 = dict()
    message2['date'] = time.time()-3600
    message2['text'] = 'Hello, World!'
    api_response.append(message2)

    messages["messages"] = api_response

    return json.dumps(messages)


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
