import base64

from flask import Flask, render_template, url_for, redirect, session, json
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.update({
    'SECRET_KEY': 'SomethingNotEntirelySecret',
    'OIDC_CLIENT_SECRETS': './client_secrets.json',
    'OIDC_DEBUG': True,
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_SCOPES': ["openid", "profile"],
    'OVERWRITE_REDIRECT_URI': 'http://localhost:8080/authorization-code/callback',
    'OIDC_CALLBACK_ROUTE': '/authorization-code/callback'
})

oidc = OpenIDConnect(app)


@app.route("/")
def home():
    return render_template("home.html", oidc=oidc)


@app.route("/login")
def login():
    bu = oidc.client_secrets['issuer'].split('/oauth2')[0]
    cid = oidc.client_secrets['client_id']

    destination = 'http://localhost:8080/profile'
    state = {
        'csrf_token': session['oidc_csrf_token'],
        'destination': oidc.extra_data_serializer.dumps(destination).decode('utf-8')
    }

    return render_template("login.html", oidc=oidc, baseUri=bu, clientId=cid, state=base64.b64encode(json.dumps(state)))


@app.route("/profile")
def profile():
    info = oidc.user_getinfo(["sub", "name", "email", "locale"])

    return render_template("profile.html", profile=info, oidc=oidc)


@app.route("/logout", methods=["POST"])
def logout():
    oidc.logout()

    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
