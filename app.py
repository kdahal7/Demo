from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from extract import extract_text_from_pdf  # you'll need to handle URLs
from search import build_faiss_index, search_index
from decision import decide
import requests
import fitz

app = FastAPI()

# INPUT format for HackRx
class QueryRequest(BaseModel):
    documents: str
    questions: list[str]

# ENDPOINT REQUIRED BY HACKRX
@app.post("/hackrx/run")
def run_query(req: QueryRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Bearer token")

    # Download the document from given URL
    response = requests.get(req.documents)
    with open("temp.pdf", "wb") as f:
        f.write(response.content)

    text = extract_text_from_pdf("temp.pdf")
    chunks = text.split("\n\n")
    index, chunk_list = build_faiss_index(chunks)

    # Get answers to each question
    answers = []
    for question in req.questions:
        retrieved = search_index(index, chunk_list, question)
        answer = decide({"procedure": question, "policy_duration": 12}, retrieved)  # quick example input
        answers.append(answer["justification"])

    return {"answers": answers}

@app.get("/")
def home():
    return {"message": "FastAPI HackRx backend is running!"}
