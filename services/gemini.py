import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

rate_prompt = """
Evaluate the uploaded document and return a rating out of 100 in the following format:
rating;;reason;;suggested improvements
- If the document does not appear to be a resume, return 0;;The file you uploaded is not a resume.;;None.
- Otherwise, briefly justify the rating based on resume quality, and list concise, actionable improvement suggestions.
- Be BRUTALLY honest with scoring, no sugarcoating anything rate them on content also.
"""

match_prompt = """
You are given two documents: one is a resume and the other is a job description. Analyze both and return a match rating out of 100 based on how well the resume aligns with the job description.

Return your response in the following format (DO NOT SAY ANYTHING BEFORE OR AFTER, JUST THIS FORMAT):
rating;;reason;;suggested improvements

Guidelines:
- If the uploaded resume is not a resume, return: 0;;The uploaded file is not a valid resume.;;None.
- If the uploaded job description is not a job description, return: 0;;The uploaded file is not a valid job description.;;None.

- Otherwise, provide:
  - A numerical rating from 0 to 100.
  - A brief explanation justifying the score (why the resume is or isn't a strong fit).
  - A short list of actionable improvement suggestions to better tailor the resume for the job, and/or suggestions on how they can get more relevant experience.
  - Be BRUTALLY honest with scoring, like if you were an HR tech recruiter in a tough market with tons of qualified candidates, put a large emphasis on keyword/skill match
  - Reduce score significantly if they aren't a good match, based on relevant experience (heavily weight on professional job experience)
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
                rate_prompt
            ],
        )
        
        feedback_arr = response.text.split(";;")

        return feedback_arr

    except FileNotFoundError as e:
        return "Provided file does not exist!"
    
    except Exception as e:
        return f'An error occured: {e}'
    
def gemini_match(resume_path, job_description_path):
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
        resume = client.files.upload(file=resume_path)
        job_description = client.files.upload(file=job_description_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                resume,
                job_description,
                "\n\n",
                match_prompt
            ],
        )
        
        feedback_arr = response.text.split(";;")

        return feedback_arr

    except FileNotFoundError as e:
        return "Provided file does not exist!"
    
    except Exception as e:
        return f'An error occured: {e}'