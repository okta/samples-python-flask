import asyncio
import json
import time

from flask import Flask, request
from flask_cors import CORS
from flask_oidc import OpenIDConnect

from okta_jwt_verifier import JWTVerifier


app = Flask(__name__)
CORS(app)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ["openid", "profile", "email"],
    'OIDC_CALLBACK_ROUTE': '/authorization-code/callback',
    'OIDC_RESOURCE_SERVER_ONLY': True
})


loop = asyncio.get_event_loop()


async def is_valid_token(request):
    """Gets token from request headers and validate it.

    Token is inside Authorization header: 'Authorization': 'Bearer {TOKEN}'
    """
    token = request.headers.get('Authorization').split()[1]
    client_secrets = json.load(open('./client_secrets.json'))
    client_id = client_secrets['web']['client_id']
    issuer = client_secrets['web']['issuer']
    jwt_verifier = JWTVerifier(issuer, client_id)
    try:
        await jwt_verifier.verify_access_token(token)
    except Exception:
        return False
    return True


def patched_validate_token(token, *args, **kwargs):
    return loop.run_until_complete(is_valid_token(request))


oidc = OpenIDConnect(app)
oidc.validate_token = patched_validate_token


@app.route("/")
def home():
    return "Hello!  There's not much to see here." \
           "Please grab one of our front-end samples for use with this sample resource server"


@app.route("/api/messages")
@oidc.accept_token(require_token=True)
def messages():
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
