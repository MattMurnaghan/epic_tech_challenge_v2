from sqlmodel import SQLModel, Field
from typing import Optional, List
from pprint import pprint
import uuid


class User(SQLModel, table=True):
    """
    SQLModel class to handle the user data object for both the database and the API

    API:
        All fields are handled and stored in memory when ingesting data from the API

    Database:
        Database fields are marked for persistence by using the Field class from SQLModel
        Fields:
            id: UUID - Primary key for the user object
            username: str - Username of the user
            email: str - Email of the user
            username_character_count: int - Number of characters in the username

        username_character_count is a calculated field that is set to the length of the
        username when the object is created
    """

    id: Optional[uuid.UUID] = Field(default=uuid.uuid4(), primary_key=True)
    username: str = Field(index=True)
    email: str = Field(unique=True)
    username_character_count: int = Field(default=0)
    session: Optional[int] = None
    _links: Optional[dict] = None

    def __init__(self, **kwagrs):
        super().__init__(**kwagrs)
        self.username_character_count = len(self.username)


class UserList:
    """
    Class for handling the list of User objects retrieved from the API.
    """

    def __init__(self, users: List[User]):
        self.users = users

    def filter_by_username(self, first_char: str) -> "UserList":
        """
        Filter users by usernames starting with a specific character.
        Returns a new UserList instance.
        """
        filtered_users = [
            user for user in self.users if user.username.startswith(first_char)
        ]
        return UserList(filtered_users)

    def sort_by_username(self, descending: bool = False) -> "UserList":
        """
        Sort users alphabetically by username.
        Parameters:
            descending (bool): If True, sorts in descending order. Default is False (ascending).
        Returns:
            A new UserList instance with the users sorted by username.
        """
        sorted_users = sorted(
            self.users, key=lambda user: user.username, reverse=descending
        )
        return UserList(sorted_users)

    def trim_user_info(self) -> List[dict]:
        """
        Return a list of dictionaries containing trimmed user information:
        id, email, username, and username_character_count.
        """
        return [
            {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "username_character_count": user.username_character_count,
            }
            for user in self.users
        ]

    def show_users(self, trimmed = False) -> None:
        """
        Print the username and email of each user in the list.
        """
        if trimmed:
            pprint(self.trim_user_info())
        else:
            pprint(self.users)
        return None
