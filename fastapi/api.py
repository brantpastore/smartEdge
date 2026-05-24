# cd /home/bpastore/Github/smartEdge/fastapi
# source ../.venv/bin/activate
# python -m uvicorn api:app --reload

import fastapi
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application!"}


@app.post("/flip")
def flip_frame():
    # Implement logic to flip the webcam frame
    return {"message": "Frame flipped successfully!"}

@app.post("/blur")
def blur_frame():
    # Implement logic to blur the webcam frame
    return {"message": "Frame blurred successfully!"}

@app.post("/capture")
def capture_frame():
    # Implement logic to capture the current webcam frame and save it
    return {"message": "Frame captured successfully!"}
