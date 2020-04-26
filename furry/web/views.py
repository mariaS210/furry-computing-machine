from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.

import google.oauth2.credentials
import google_auth_oauthlib.flow

import json
import os

def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}

def authorize(request):
    with open('client_secret.json', 'w') as fp:
        fp.write(os.environ.get("CLIENT_SECRET"))
    
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json',
        ['https://www.googleapis.com/auth/classroom.courses'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.
    flow.redirect_uri = 'https://furry-computing-machine.herokuapp.com/web/content'

    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    response = HttpResponseRedirect(authorization_url)
    x = dir(response)
    request.session['state'] = state
    return response


def callback(request):
    state = request.session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)

    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    # Store credentials in the session.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    credentials = flow.credentials
    path = reverse("content")
    response = HttpResponseRedirect(path)
    request.session['credentials'] = credentials_to_dict(credentials)
    return response

def revoke(request):
    return HttpResponse("Revoke!")

def clear(request):
    return HttpResponse("Cleared!")

def content(request):
    credentials = request.session["credentials"]
    if not credentials:
        return HttpResponseRedirect(reverse('authorize'))

    # Load credentials from the session.
    credentials = google.oauth2.credentials.Credentials(
        **request.session['credentials'])

    classroom = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    classes = classroom.list().execute()

    # Save credentials back to session in case access token was refreshed.
    # ACTION ITEM: In a production app, you likely want to save these
    #              credentials in a persistent database instead.
    request.session['credentials'] = credentials_to_dict(credentials)

    return HttpResponse("Content: {}".format(json.dumps(classes)))