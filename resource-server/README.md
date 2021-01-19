# Flask Resource Server Example

This sample application authenticates requests against your Flask application, using access tokens.

The access tokens are obtained via the [Implicit Flow][].  As such, you will need to use one of our front-end samples with this project.  It is the responsibility of the front-end to authenticate the user, then use the obtained access tokens to make requests to this resource server.

> Requires Python version 3.6.0 or higher.

## Prerequisites

Before running this sample, you will need the following:

* An Okta Developer Account, you can sign up for one at https://developer.okta.com/signup/.
* An Okta Application, configured for Singe-Page App (SPA) mode. This is done from the Okta Developer Console and you can find instructions [here][OIDC SPA Setup Instructions].  When following the wizard, use the default properties.  They are are designed to work with our sample applications.
* One of our front-end sample applications to demonstrate the interaction with the resource server:
  * [Okta Angular Sample Apps][]
  * [Okta React Sample Apps][]
  * [Okta Vue Sample Apps][]

A typical resource-server requires a frontend and a backend application, so you will need to start each process:

## Running This Example
To run this application, you first need to clone this repo and then enter into this directory:

```bash
git clone git@github.com:okta/samples-python-flask.git
cd samples-python-flask/resource-server
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Now you need to gather the following information from the Okta Developer Console that belongs to your front-end application:
- **Client ID**  - The client ID of the SPA application that you created earlier. This can be found on the "General" tab of an application, or the list of applications. This identifies the application that tokens will be minted for.
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

Next, Start the resource server example:

```bash
python main.py
```

Finally, install the [front-end sample project of your choice](#prerequisites) and run the sample application.
Once the front-end sample is running, you can navigate to http://localhost:8080 in your browser and log in to the front-end application.  Once logged in, you can navigate to the "Messages" page to see the interaction with the resource server.


[Implicit Flow]: https://developer.okta.com/authentication-guide/implementing-authentication/implicit
[Okta Angular Sample Apps]: https://github.com/okta/samples-js-angular
[Okta Vue Sample Apps]: https://github.com/okta/samples-js-vue
[Okta React Sample Apps]: https://github.com/okta/samples-js-react
[OIDC SPA Setup Instructions]: https://developer.okta.com/authentication-guide/implementing-authentication/implicit#1-setting-up-your-application
