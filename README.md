# PyRater

A Python application that uses the Google Gemini API to rate resumes and provide feedback.

## Running Locally

### 1. Setup

#### Clone the Repository

```bash
git clone https://github.com/larrylaa/PyRater.git
```

#### Environment Configuration

- Get the `.env` file from the project owner, or create your own with your Supabase and Gemini API keys.
- Place the `.env` file in the root of the cloned project directory.
- Ensure it is named as **.env** (has to have a . in front to work)

#### Install Python and Virtual Environment Tool

If you don’t already have `virtualenv` installed:

```bash
pip install virtualenv
```

#### Create and Activate a Virtual Environment

**Windows:**

```bash
python -m venv env
env\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv env
source env/bin/activate
```

---

### 2. Install Dependencies

After activating the virtual environment, install requirements using the below command.

```bash
pip install -r requirements.txt
```

---

### 3. Run the Application

Make sure your virtual environment is still activated, then run:

```bash
python app.py
```

---

## Tech Stack

- Python
- Tkinter
- Google Gemini API
- Supabase API
- Virtualenv
