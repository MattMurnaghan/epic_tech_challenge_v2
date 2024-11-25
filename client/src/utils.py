import os
from dotenv import load_dotenv

def load_env_vars() -> None: 
    try:
        load_dotenv()
    except Exception as e:
        print(f"Error loading .env file: {e}")
    return None


def load_urls(list_urls: list) -> dict:
    """
    Load environment variables for a given list of URLs.
    Ensures all URLs in the list are found in the .env file.
    """
    try:
        if not all(isinstance(url, str) for url in list_urls):
            raise ValueError("All items in list_urls must be strings.")
        
        urls = {url: os.getenv(url) for url in list_urls}

        # Check for missing URLs
        missing_urls = [key for key, value in urls.items() if value is None]
        if missing_urls:
            raise ValueError(f"Missing environment variables for: {', '.join(missing_urls)}")
        
        print(f"URLs loaded successfully for:\n {list_urls}")

    except Exception as e:
        print(f"Error loading URLs: {e}")
        return {}
    
    return urls