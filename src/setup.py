from stravalib import Client
from strava_config import CLIENT_ID, CLIENT_SECRET
from dotenv import set_key, find_dotenv

def get_authorization_url():
    """
    Get the authorization URL to fetch the temporary auth code.
    """
    client = Client()
    url = client.authorization_url(
        client_id=CLIENT_ID,
        redirect_uri="http://127.0.0.1:5000/authorization",
        scope=["read", "activity:read"], # read user's activity data that's visible to everybody and followers (for more on scope: https://developers.strava.com/docs/authentication/)
    )

    return url    


def get_access_token(temp_code: str):
    """
    Returns the access token (to create the Strava client) from the temporary code provided from the authorization URL.
    Call get_authorization_url() to get the authorization URL first.
    The code will be stored in the URL of the following format: http://127.0.0.1:5000/authorization?state=&code=ed7456e5dc0ebcc2f8ce9f6e2d6406064d0184de&scope=read,activity:read 
    """

    client = Client()
    
    token_response = client.exchange_code_for_token(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET, 
        code=temp_code
    )
    # The token response contains both an access_token and a refresh token.
    return token_response    

def main():
    # Redirect user to authorization URL
    auth_url = get_authorization_url()
    
    # Pause until they accept
    input(f"Go to the following URL to authorize the app to collect your data:\n {auth_url}. \nHit 'Enter' to proceed once you've authorized the app.")
    
    # Request for temp authorization code
    temp_code = input("Paste your temp authorization code here: ")
    
    # Get the access token, refresh token, and expiration time from the temp code
    token_response = get_access_token(temp_code=temp_code)
    
    # Write them out to the .env
    dotenv_path = find_dotenv()
    set_key(dotenv_path, "ACCESS_TOKEN", token_response["access_token"])
    set_key(dotenv_path, "REFRESH_TOKEN", token_response["refresh_token"])
    set_key(dotenv_path, "EXPIRES_AT", str(token_response["expires_at"]))
    print("Access token, refresh token, and expiration time successfully written to .env.")
    

if __name__ == "__main__":
    main()