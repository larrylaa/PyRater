import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
prompt = """
Evaluate the uploaded document and return a rating out of 100 in the following format:
rating;;reason;;suggested improvements
- If the document does not appear to be a resume, return 0;;The file you uploaded is not a resume.;;None.
- Otherwise, briefly justify the rating based on resume quality, and list concise, actionable improvement suggestions.
"""


def gemini_rate(resume_path):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        resume = client.files.upload(file=resume_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                resume,
                "\n\n",
                prompt
            ],
        )
        
        feedback_arr = response.text.split(";;")

        return feedback_arr

    except FileNotFoundError as e:
        return "Provided file does not exist!"
    
    except Exception as e:
        return f'An error occured: {e}'