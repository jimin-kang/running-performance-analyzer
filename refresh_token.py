import os
from stravalib import Client
from strava_config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN
from dotenv import set_key, find_dotenv
import json

def refresh_access_token(refresh_token: str):
    """
    Use the refresh token to generate a new access token.
    """
    client = Client()
    return client.refresh_access_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        refresh_token=refresh_token,
    )    

def main():
    # Get the new access token & expiration time
    refresh_token_response = refresh_access_token(refresh_token=REFRESH_TOKEN)
    print(json.dumps(refresh_token_response, indent=4))

    # Write them out to the .env
    dotenv_path = find_dotenv()
    set_key(dotenv_path, "ACCESS_TOKEN", refresh_token_response["access_token"])
    set_key(dotenv_path, "REFRESH_TOKEN", refresh_token_response["refresh_token"])
    set_key(dotenv_path, "EXPIRES_AT", str(refresh_token_response["expires_at"]))
    print("Access token, refresh token, and expiration time successfully written to .env.")


if __name__ == "__main__":
    main()