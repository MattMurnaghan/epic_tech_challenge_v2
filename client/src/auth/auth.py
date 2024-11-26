# retrieve jwt token from the freefakeapi.io
import requests
import os
from utils import load_env_vars, load_urls

# load environment variables - handle errors
load_env_vars()

# load urls from .env file - handle errors
urls = load_urls(["BASE_URL", "AUTH"])

# get jwt token from freefakeapi.io - write to token.txt
def get_jwt_token():
    url = urls["BASE_URL"] + urls["AUTH"]
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "username": os.getenv("API_USERNAME"),
        "password": os.getenv("API_PASSWORD")
    }

    response = requests.post(url, headers=headers, json=body)
    return response.json()["token"]

if __name__ == "__main__":
    token = get_jwt_token()
    print(f"JWT Token received")
    
    # Define the path to the auth folder
    token_file_path = os.path.join(os.path.dirname(__file__), "token.txt")
    
    # Write the token to token.txt
    with open(token_file_path, "w") as file:
        file.write(token)
        print(f"Token successfully written to {token_file_path}")