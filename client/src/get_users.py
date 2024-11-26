import requests

from client.src.auth.auth import get_jwt_token
from client.src.utils import load_env_vars, load_urls

load_env_vars()

urls = load_urls(["BASE_URL", "USERS", "USERS_ID"])


def get_user_list() -> dict:
    headers = {"Authorization": f"Bearer {get_jwt_token()}"}
    response = requests.get(urls["BASE_URL"] + urls["USERS"], headers=headers)
    return response.json()


def get_users_by_filtered_name(first_char: str = None) -> dict:
    headers = {"Authorization": f"Bearer {get_jwt_token()}"}
    response = requests.get(urls["BASE_URL"] + urls["USERS"], headers=headers)
    user_list = response.json()
    if first_char is None:
        return user_list
    filtered_users = [
        user for user in user_list if user["username"].startswith(first_char)
    ]
    return filtered_users


def get_id_user_email_from_user_list(user_list: list) -> list:
    """
    Extracts the id and email from a user object in a supplied list of users
    """
    for user in user_list:
        if "id" not in user or "email" not in user or "username" not in user:
            raise ValueError(
                "User object malformed - must contain 'id', 'email', and 'username' keys"
            )
    return [
        {"id": user["id"], "email": user["email"], "username": user["username"]}
        for user in user_list
    ]


def count_username_chars(user: dict) -> None:
    """
    Counts the number of characters in the username of a user object
    """
    if "username" not in user:
        raise ValueError("User object malformed - must contain 'username' key")
    print(f"username {user['username']} contains {len(user['username'])} characters.")


if __name__ == "__main__":
    # retrieve users beginning with the letter "M"
    first_char = "M"
    filtered_user_list = get_users_by_filtered_name(first_char=first_char)
    trimmed_user_list = get_id_user_email_from_user_list(user_list=filtered_user_list)
    for user in trimmed_user_list:
        count_username_chars(user)
