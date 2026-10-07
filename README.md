
# Amit 2.0

Amit 2.0 is a personal AI-powered digital twin built with Python, Gradio, and the OpenAI API. It acts as a conversational assistant for a person’s professional profile, using a LinkedIn PDF and a short profile summary to answer questions about career background, experience, skills, and available opportunities.

Try it at https://amitg23-amit2-0.hf.space/

## What this project does

- Hosts a chat interface for visitors to ask questions about the person behind the website
- Uses profile context from `summary.txt` and `linkedin.pdf`
- Answers only career-related questions and redirects unrelated questions back to professional topics
- Captures interest and unanswered questions through the built-in tools
- Provides a polished, branded UI with custom styling and example prompts
- Records email address, if provided, to be contacted later

## Tech stack

- Python 3
- Gradio
- OpenAI Chat Completions API
- pypdf for reading the LinkedIn PDF
- python-dotenv for environment configuration
- requests for Pushover notifications

## Setup

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your credentials:

```env
OPENAI_API_KEY=your_openai_api_key
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

Notes:
- `OPENAI_API_KEY` is required for the chat assistant to work.
- `PUSHOVER_USER` and `PUSHOVER_TOKEN` are used by the project’s tool calls to notify when a user submits interest or asks a question the assistant cannot answer.

## Run the app

```bash
python app.py
```

Then open the local URL shown in the terminal (typically http://127.0.0.1:7860).

## How it works

- `context.py` reads the LinkedIn PDF and summary text, then injects them into the system prompt.
- `app.py` sends the chat history and system context to the OpenAI model.
- If the model decides it needs to call a tool, `tools.py` records the information or logs unanswered questions.
- `styles.py` adds branding and UI polish to the chat experience.

## Customize the project

To adapt this project for another person:

- Replace `linkedin.pdf` with the target person’s profile PDF
- Update `summary.txt` with the person’s bio and background
- Modify the app title and description in `app.py`
- Adjust the example prompts in `styles.py`

## Important notes

- This project is designed for a professional/portfolio use case and intentionally limits answers to career-related topics.
- If the AI does not know an answer, it is expected to record the question and respond honestly rather than guessing.
- For production use, consider adding better validation, persistence, and security around lead capture and API keys.

## License

This project is provided as-is for personal portfolio and demo purposes.
