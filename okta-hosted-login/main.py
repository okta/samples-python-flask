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
    return render_template("home.html", oidc=oidc)


@app.route("/login")
@oidc.require_login
def login():
    return redirect(url_for("profile"))


@app.route("/profile")
@oidc.require_login
def profile():
    info = oidc.user_getinfo(["sub", "name", "email"])

    return render_template("profile.html", profile=info, oidc=oidc)


@app.route("/logout", methods=["POST"])
def logout():
    oidc.logout()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)