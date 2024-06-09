from google_auth_oauthlib.flow import InstalledAppFlow



SCOPES = ['https://www.googleapis.com/auth/calendar.events']

flow = InstalledAppFlow.from_client_secrets_file(
    'google_creds/client_secret_679422190818-aker0lqkeq3b81vgcf96i3hgfkoovbsu.apps.googleusercontent.com.json',
    scopes=SCOPES,
)

credentials = flow.run_local_server(port=8000)

# Save the credentials to a file
with open('google_creds/token.json', 'w') as token_file:
    token_file.write(credentials.to_json())
    



# http://localhost:8000/?state=O68F7tnD0BN8EWG9A0kIwHYoaCpNIV&code=4/0AfJohXkBhyD54bQV70nX8SqyHXVUfOuNUgGj8wjIGD1Tt_eStkhNaGlA3T6wIkd9HEBkyg&scope=https://www.googleapis.com/auth/calendar.events



# http://localhost:8000/?state=C2cKadpj7ioWHbIBIUEo6EHwTYf12C&code=4/0AfJohXnCQuV3mftz9RM6yoiPxOq44VEGANBreoB2LtXJGM1f9KF0OW2L5FUD5s-2bpL56Q&scope=https://www.googleapis.com/auth/calendar.events