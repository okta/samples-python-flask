import base64
import requests

from flask import Flask, render_template, url_for, redirect, session, json, request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from helpers import is_access_token_valid, is_id_token_valid, config
from user import User


app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})


login_manager = LoginManager()
login_manager.init_app(app)


# Parameter state should be something not guessable
APP_STATE = 'ApplicationState+CSRFProtection'
NONCE = 'SampleNonce'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    bu = config['issuer'].split('/oauth2')[0]
    cid = config['client_id']

    return render_template("login.html",
                           baseUri=bu,
                           clientId=cid,
                           state=APP_STATE,
                           nonce=NONCE)


@app.route("/authorization-code/callback")
def callback():
    if request.args.get("state") != APP_STATE:
        return "The state is unexpected.", 403
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    if not is_access_token_valid(access_token, config["issuer"], config["client_id"]):
        return "Access token is invalid", 403

    if not is_id_token_valid(id_token, config["issuer"], config["client_id"], NONCE):
        return "ID token is invalid", 403

    # Authorization flow successful, get userinfo and login user
    userinfo_response = requests.get(config["userinfo_uri"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)

    return redirect(url_for("profile"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


def base64_to_str(data):
    return str(base64.b64encode(json.dumps(data).encode('utf-8')), 'utf-8')


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
