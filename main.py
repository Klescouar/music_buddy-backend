from fastapi import FastAPI
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
openAiApiKey = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=openAiApiKey)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def get_suggestion(input: str):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a music expert, you know all music styles from the most underground to the most popular and from all times.",
            },
            {
                "role": "user",
                "content": f"Return an array of 10 suggestions that sounds like {input}. Suggestions should not be songs from the same group or artist. Suggestions should be very similar to {input}, same music style, same period."
                + "Each song will be a dict with title and artist keys like this. I just need the array, don't send me other information. Example of the return: [{'title': 'song title', 'artist': 'song artist'}]. if there are some apostrophes in titles or artist names, remove it and replace it with a space",
            },
        ],
    )
    return eval(completion.choices[0].message.content)
