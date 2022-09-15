import json

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()
security = HTTPBasic()
app.mount("/img", StaticFiles(directory="../data/img"), name="static")
app.mount("/_app", StaticFiles(directory="../data/build/_app"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def load_reddit_data():
    with open("../data/reddit-posts.json") as f:
        return json.load(f)

@app.get("/api/data")
def read_root(credentials: HTTPBasicCredentials = Depends(security)):
    return load_reddit_data()

@app.get("/", response_class=HTMLResponse)
async def read_root(credentials: HTTPBasicCredentials = Depends(security)):
    with open("../data/build/index.html") as f:
        return "".join(f.readlines())
