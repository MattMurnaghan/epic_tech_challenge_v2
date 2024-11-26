import requests
from pprint import pprint

from client.src.auth.auth import get_jwt_token
from utils import load_env_vars, load_urls
from models.user import User, UserList, DbUser
from server.database.db_connect import get_session


load_env_vars()
urls = load_urls(["BASE_URL", "USERS", "USERS_ID"])


def get_user_list() -> UserList:
    """
    Retrieve user data from the API and parse it into User SQLModel instances.
    """
    headers = {"Authorization": f"Bearer {get_jwt_token()}"}
    response = requests.get(urls["BASE_URL"] + urls["USERS"], headers=headers)
    response.raise_for_status() 
    api_users = response.json()
    users = UserList([User(**user_data) for user_data in api_users])
    return users

if __name__ == "__main__":
    sort_char = "M"

    print("\ngettings users from api:\n")
    users = get_user_list()

    print('\nfilter users by first letter of username = "M":\n')
    filtered_users = users.filter_by_username(sort_char).trim_user_info()

    for user in filtered_users:
        print(f"username {user['username']} contains {len(user['username'])} characters.")
