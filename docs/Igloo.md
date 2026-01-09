# Igloo API Access Instructions

## Prerequisites

- You must have access to [The Source](https://source.redhat.com/) via SSO

## Instructions

1. Register for the [Igloo Developer Program](https://customercare.igloosoftware.com/support/developers/registration)
    - Company Name: `Red Hat`
    - Igloo URL: `https://source.redhat.com/`
1. After signing up, an Igloo service team member will reach out to provide you your API Key
1. Open an incognito window and visit [The Source sign in page](http://source.redhat.com/?signin)
1. Click "Not an associate?", then click "I forgot my password"
1. Enter your Red Hat email and click Continue. You will receive an email with a link to reset your password.
1. Enter a new password and click Continue.
    - If you get an error at this step, please wait and try again the following day
1. Return to [The Source sign in page](http://source.redhat.com/?signin), click "Not an associate?", check that you can sign in with your new credentials.

## Environment Variables

Once you have your credentials, add the following to your `.env` file:

```sh
IGLOO_ENDPOINT="https://source.redhat.com/"
IGLOO_API_KEY="<your-api-key>"
IGLOO_ACCESS_KEY="<your-access-key>"
IGLOO_USER="<your-redhat-email>"
IGLOO_PASS="<your-password>"
IGLOO_COMMUNITY_KEY="<igloo-community-key>"
```

The Igloo community key can be found by visiting [The Source](https://source.redhat.com/), opening the developer console (F12), and entering `Igloo.community`.
The community key is the two digit number in the "key" field.
