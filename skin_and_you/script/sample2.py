from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

flow = InstalledAppFlow.from_client_secrets_file(
    'google_creds/client_secret_679422190818-aker0lqkeq3b81vgcf96i3hgfkoovbsu.apps.googleusercontent.com.json',
    scopes=['https://www.googleapis.com/auth/calendar.events'],
)

# Retrieve the authorization code (from your OAuth callback view, for example)
authorization_code = '4/0AfJohXkBhyD54bQV70nX8SqyHXVUfOuNUgGj8wjIGD1Tt_eStkhNaGlA3T6wIkd9HEBkyg'

# Exchange the authorization code for tokens
credentials = flow.fetch_token(
    # 'https://oauth2.googleapis.com/token',
    authorization_response='your_redirect_uri?code=' + authorization_code,
)

# Save the credentials to a file
with open('google_creds/token.json', 'w') as token_file:
    token_file.write(credentials.to_json())
    
    
    
    # https://developers.google.com/identity/protocols/oauth2/web-server#creatingclient