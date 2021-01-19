# Flask Sample Applications for Okta
This repository contains several sample applications that demonstrate various Okta use-cases in your Flask application.

> Requires Python version 3.6.0 or higher.

Please find the sample that fits your use-case from the table below.

| Sample                                  | Description |
|-----------------------------------------|-------------|
| [Okta-Hosted Login](/okta-hosted-login) | A Flask application that will redirect the user to the Okta-Hosted login page of your Org for authentication.  The user is redirected back to the Python application after authenticating. |
| [Custom Login Page](/custom-login)      | A Flask application that uses the Okta Sign-In Widget within the Flask application to authenticate the user. |
| [Resource Server](/resource-server)     | This is a sample API resource server that shows you how to authenticate requests with access tokens that have been issued by Okta. |

> ⚠️ Note: These examples require the use of API Access Management. This solution is not included by default for **organizations** (you will have this [error](https://support.okta.com/help/s/article/400-Bad-Request-The-requested-feature-is-not-enabled-in-this-environment?language=en_US)).
