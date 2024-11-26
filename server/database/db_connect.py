from sqlmodel import SQLModel, Session, create_engine
from models.user import DbUser
from dotenv import load_dotenv
import os, sys

load_dotenv()
try:
    DATABASE_URL = (
        f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )
except Exception as e:
    print(f"Error loading environment variables: {e}")
    print("Cannot create database URL, exiting...")
    exit(1)

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


# Dependency to provide a database session
def get_session():
    try:
        with Session(engine) as session:
            yield session
    except Exception as e:
        print(f"Error establishing database session: {e}")
        raise e

# Function to initialize the database
def init_db():
    """
    Create all tables defined using SQLModel.
    """
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    try:
        confirm = input("This will initialize the database, are you sure? (y/n): ")
        if confirm.lower() != "y":
            print("Exiting...")
            exit(0)
        init_db()
        print("Database initialized successfully!")
        exit(0)
    except Exception as e:
        print(f"Error initializing the database: {e}")
        exit(1)