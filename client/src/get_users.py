import requests

from client.src.auth.auth import get_jwt_token
from utils import load_env_vars, load_urls
from models.user import User, UserList, DbUser
from server.database.db_connect import get_session
from sqlmodel import select


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


def add_users_to_db(users: UserList):
    """
    Add users to the database.
    """
    try:
        with get_session() as session:
            for user in users:
                statement = select(DbUser).filter(
                    DbUser.email == user["email"])
                result = session.exec(statement)
                existing_user = result.first()
                if existing_user:
                    print(
                        f"User with email {user['email']} already exists. Skipping.")
                    continue
                new_user = DbUser(
                    id=user["id"],
                    username=user["username"],
                    email=user["email"],
                    username_character_count=user["username_character_count"]
                )
                session.add(new_user)
            session.commit()
            print("\nUsers added:\n")
            for user in users:
                print(f"username: {user['username']} \t- id: {user['id']}")
    except Exception as e:
        print(f"Error adding users to the database: {e}")


if __name__ == "__main__":
    sort_char = "M"

    print("\ngettings users from api:\n")
    users = get_user_list()

    print('\nfilter users by first letter of username = "M":\n')
    filtered_users = users.filter_by_username(sort_char).trim_user_info()

    for user in filtered_users:
        print(
            f"username {user['username']} contains {user['username_character_count']} characters.")

    print("\nAdding filtered users to the database:\n")
    add_users_to_db(filtered_users)
