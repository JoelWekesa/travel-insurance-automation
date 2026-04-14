import threading ## Import the threading module to run the scheduler in a separate thread - TWO PROCESS AT THE SAME TIME
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scheduler import run_test as run_scheduler ## Import the run_test function from the scheduler module

def start_scheduler():
    run_scheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):     
    thread = threading.Thread(target=start_scheduler, daemon=True)     
    thread.start()     
    yield

 
app = FastAPI(lifespan=lifespan)
# Mount the static files directory

app.mount("/screenshots", StaticFiles(directory="screenshots"), name="screenshots")

@app.get("/health")
async def root():
    return {"message": "Automation is running successfully!"}