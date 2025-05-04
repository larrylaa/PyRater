import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

def get_supabase_client() -> Client:
    return create_client(url, key)

def store_rating(rating: int, feedback: str, improvements: str, resume_text: str, user: str) -> str:
    try:
        supabase = get_supabase_client()
        response = (
            supabase.table("ratings")
            .insert({
                "rating": rating,
                "feedback": feedback,
                "improvements": improvements,
                "resume": resume_text,
                "user": user
            })
            .execute()
        )
        return f"Successfully added rating: {response.data}"
    except Exception as e:
        return f'An error occurred while storing the rating: {e}'
    
# TODO: add user pass enter functionality, will need a users table (assigned to: larry)
def check_if_user_exists(user: str) -> bool:
    try:
        supabase = get_supabase_client()
        response = (
            supabase.table("ratings")
            .select("*")
            .eq("user", user.lower())
            .execute()
        )
        if response and response.data:
            return True
        else:
            return False
    except Exception as e:
        print(f'An error occurred while checking for user: {e}')
        return False
    
def fetch_user_ratings(user: str) -> bool:
    try:
        supabase = get_supabase_client()
        response = (
            supabase.table("ratings")
            .select("*")
            .eq("user", user.lower())
            .execute()
        )
        if response and response.data:
            return response.data
    except Exception as e:
        print(f'An error occurred while fetching users resume ratings: {e}')
        return False