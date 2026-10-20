from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from planner import Brief, create_plan
from database import init_db, list_plans, get_plan

app = FastAPI(title="GenAI Event Planner")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
def _startup(): init_db()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/plan")
def plan(brief: Brief):
    return create_plan(brief)

@app.get("/api/plans")
def plans(): return list_plans()

@app.get("/api/plans/{pid}")
def one_plan(pid: int):
    p = get_plan(pid)
    if not p: raise HTTPException(404)
    return p