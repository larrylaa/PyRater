# TODO: GEMINI RATING LOGIC
# from dotenv import load_dotenv
# from google import genai
# from pathlib import Path
# import os

# load_dotenv()

# media = Path("resumes")

# # TODO: CONNECT SUPABASE
# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# def gemini_call(file_name):
#     try:
#         client = genai.Client(api_key=GEMINI_API_KEY)
#         resume = client.files.upload(file=media / file_name)

#         response = client.models.generate_content(
#             model="gemini-2.0-flash",
#             contents=[
#                 resume,
#                 "\n\n",
#                 "Can you rate this resume out of 100 concisely. Return the answer in this format rating/100;;reason if it does not look like a resume give it a 0 and for the reason put not a resume",
#             ],
#         )
        
#         feedback_arr = response.text.split(";;")
#         rating = feedback_arr[0].strip()
#         feedback = feedback_arr[1].strip()

#         if feedback.lower() == "not a resume":
#             return "Provided file is not a resume!"

#         return f'I would rate this resume {rating}.'

#     except FileNotFoundError as e:
#         return "Provided file does not exist!"
    
#     except Exception as e:
#         return f'An error occured: {e}'