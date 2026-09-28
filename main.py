from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

from explanation_module import explain_topic
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import recommend_learning_path

app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)

templates = Jinja2Templates(directory="templates")

class TopicRequest(BaseModel):
    topic: str
    level: str = "beginner"

class QuestionRequest(BaseModel):
    question: str

class QuizRequest(BaseModel):
    topic: str
    num_questions: int = 5

class SummaryRequest(BaseModel):
    text: str

class PathRequest(BaseModel):
    goal: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    try:
        return templates.TemplateResponse(request=request, name="index.html")
    except:
        return HTMLResponse("""
        <html><body style="font-family:Arial; text-align:center; padding:50px;">
        <h1>🎉 EduGemini-AI is Running!</h1>
        <p>Server is return{"status":"EduGemini is Live"}!</p>
        <h3>Available APIs:</h3>
        <ul style="text-align:left; display:inline-block;">
        <li>POST /explain - {topic, level}</li>
        <li>POST /ask - {question}</li>
        <li>POST /quiz - {topic, num_questions}</li>
        <li>POST /summarize - {text}</li>
        <li>POST /learning-path - {goal}</li>
        </ul>
        <p>Use /docs for Swagger UI</p>
        <a href='/docs'>Go to /docs</a>
        </body></html>
        """)

@app.post("/explain")
async def explain(req: TopicRequest):
    result = explain_topic(req.topic, req.level)
    return {"result": result}

@app.post("/ask")
async def ask(req: QuestionRequest):
    result = answer_question(req.question)
    return {"result": result}

@app.post("/quiz")
async def quiz(req: QuizRequest):
    result = generate_quiz(req.topic, req.num_questions)
    return {"result": result}

@app.post("/summarize")
async def summarize(req: SummaryRequest):
    result = summarize_text(req.text)
    return {"result": result}

@app.post("/learning-path")
async def learning_path(req: PathRequest):
    result = recommend_learning_path(req.goal)
    return {"result": result}

@app.get("/docs-test")
async def test():
    return {"status": "working da mapla!"}