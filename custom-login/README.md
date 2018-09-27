# Flask + Okta Hosted Login Example
This example shows you how to use Flask to login to your application with a Custom Login page.  The login is achieved with the [Okta Sign In Widget][], which gives you more control to customize the login experience within your app.  After the user authenticates they are redirected back to the application with an authorization code that is then exchanged for an access token.

## Prerequisites

Before running this sample, you will need the following:

* An Okta Developer Account, you can sign up for one at https://developer.okta.com/signup/.
* An Okta Application, configured for Web mode. This is done from the Okta Developer Console and you can find instructions [here][OIDC WEB Setup Instructions].  When following the wizard, use the default properties.  They are are designed to work with our sample applications.

## Running This Example

To run this application, you first need to clone this repo and then enter into this directory:

```bash
git clone git@github.com:okta/samples-python-flask.git
cd samples-python-flask
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

You also need to gather the following information from the Okta Developer Console:

- **Client ID** and **Client Secret** - These can be found on the "General" tab of the Web application that you created earlier in the Okta Developer Console.
- **Issuer** - This is the URL of the authorization server that will perform authentication.  All Developer Accounts have a "default" authorization server.  The issuer is a combination of your Org URL (found in the upper right of the console home page) and `/oauth2/default`. For example, `https://dev-1234.oktapreview.com/oauth2/default`.

Now that you have the information needed from your organization, open the `okta-hosted-login` directory. Copy the [`client_secrets.json.dist`](client_secrets.json.dist) to `client_secrets.json` and fill in the information you gathered.

```json
{
  "web": {
    "auth_uri": "https://{yourOktaDomain}/oauth2/default/v1/authorize",
    "client_id": "{yourClientId}",
    "client_secret": "{yourClientSecret}",
    "redirect_uris": [
      "http://localhost:8080/authorization-code/callback"
    ],
    "issuer": "https://{yourOktaDomain}/oauth2/default",
    "token_uri": "https://{yourOktaDomain}/oauth2/default/v1/token",
    "token_introspection_uri": "https://{yourOktaDomain}/oauth2/default/v1/introspect",
    "userinfo_uri": "https://{yourOktaDomain}/oauth2/default/v1/userinfo"
  }
}
```

Now start the app server:

```
python main.py
```

Now navigate to http://localhost:8080 in your browser.

If you see a home page that prompts you to login, then things are working!  Clicking the **Log in** button will redirect you to the applicaitons custom sign-in page.

You can login with the same account that you created when signing up for your Developer Org, or you can use a known username and password from your Okta Directory.

[Okta Sign In Widget]: https://github.com/okta/okta-signin-widget
[OIDC WEB Setup Instructions]: https://developer.okta.com/authentication-guide/implementing-authentication/auth-code#1-setting-up-your-application