from services.supabase_db import check_if_user_exists, fetch_user_ratings
from gui.resume_rater import start_rater
from gui.view_ratings import start_viewer
from gui.job_matcher import start_matcher

if __name__ == "__main__":
    # TODO: ADD AUTH LOGIC
    username = str(input("Enter your username: "))
    if check_if_user_exists(username.lower()):
        print(f"Hi {username}, welcome back to PyRater!")

        print("Select a menu option below.")
        print("1. Start Resume Rater")
        print("2. Start Job Matcher")
        print("3. View Ratings History")
        print("4. Exit")

        option = int(input("Enter an option: "))
        match option:
            case 1:
                start_rater(username)
            case 2:
                # TODO: FOR LARRY 
                start_matcher(username)
            case 3:
                ratings = fetch_user_ratings(username.lower())
                # TODO: FOR ELIJAH
                start_viewer(username, ratings)
            case _:
                print("Invalid option entered, please re-run the app and try again.")
                exit()
    else:
        print(f'Hi {username}, welcome to PyRater!')
        start_rater(username)
