from fastapi import Depends, FastAPI, HTTPException
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
import os
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

app = FastAPI()
openAiApiKey = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=openAiApiKey)
models.Base.metadata.create_all(bind=engine)

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/history/", response_model=schemas.History)
def create_history_for_user(
    user_id: int, history: schemas.HistoryCreate, db: Session = Depends(get_db)
):
    return crud.create_user_history(db=db, history=history, user_id=user_id)


@app.get("/history/", response_model=list[schemas.History])
def read_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    history = crud.get_history(db, skip=skip, limit=limit)
    return history
