from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import uvicorn
import pandas as pd
import numpy as np
import os

app = FastAPI()

# values from docker file from docker compose from .env
port = os.environ.get('FASTAPI_PORT')
proxy_port = os.environ.get('FASTAPI_PROXY')
host_ip = os.environ.get('FASTAPI_HOST_IP')
host_name = os.environ.get('FASTAPI_HOST_NAME')

if os.environ.get("FASTAPI_PROD") == "false" or os.environ.get("FASTAPI_PROD") == None:
    port = 8000
    debug = True
    allowed_origins = [f"http://localhost:{proxy_port}", 
    f"https://localhost:{proxy_port}", f"http://{host_name}:{proxy_port}", 
    f"https://{host_name}:{proxy_port}",f"http://{host_ip}:{proxy_port}", 
    f"https://{host_ip}:{proxy_port}", "https://localhost:643", "http://localhost:3000"]
else:
    debug = False
    allowed_origins = [f"http://{host_name}:{proxy_port}", f"https://{host_name}:{proxy_port}",
    f"http://{host_ip}:{proxy_port}", f"https://{host_ip}:{proxy_port}", f"http://{host_name}", f"https://{host_name}"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/test")
async def test():
    return {"hello": "world"}

@app.post("/api/upload")
async def upload(files: List[UploadFile] = File(...)):
    return {"filenames": [file.filename for file in files]}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  port=port, reload=debug, debug=debug)


