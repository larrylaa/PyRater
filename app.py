from services.supabase_db import check_if_user_exists, fetch_user_ratings
from gui.resume_rater import start_rater
from gui.view_ratings import start_viewer
from gui.job_matcher import start_matcher

def handle_menu(username, is_new_user=False):
    while True:
        print("\n" + "=" * 40)
        if is_new_user:
            print(f'Hi {username}, welcome to PyRater!')
            print("1. Start Resume Rater")
            print("2. Start Job Matcher")
            print("3. Exit")
        else:
            print(f"Hi {username}, welcome back to PyRater!")
            print("1. Start Resume Rater")
            print("2. Start Job Matcher")
            print("3. View Ratings History")
            print("4. Exit")

        option = input("Enter an option: ").strip()

        if not option.isdigit():
            print("\n Invalid input. Please enter a number.")
            continue

        option = int(option)

        if is_new_user:
            match option:
                case 1:
                    start_rater(username)
                    break
                case 2:
                    start_matcher(username)
                    break
                case 3:
                    print("Thanks for using PyRater, bye!")
                    break
                case _:
                    print("Invalid option. Please try again.")
        else:
            match option:
                case 1:
                    start_rater(username)
                    break
                case 2:
                    start_matcher(username)
                    break
                case 3:
                    ratings = fetch_user_ratings(username.lower())
                    print(ratings)
                    start_viewer(username, ratings)
                    break
                case 4:
                    print("Thanks for using PyRater, bye!")
                    break
                case _:
                    print("Invalid option. Please try again.")

if __name__ == "__main__":
    username = input("Enter your username: ").strip()
    user_exists = check_if_user_exists(username.lower())
    handle_menu(username, is_new_user=not user_exists)
