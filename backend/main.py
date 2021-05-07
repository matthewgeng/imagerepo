from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
from PIL import Image 

import gridfs
import uvicorn
import os
import pprint

app = FastAPI()

# values from docker file from docker compose from .env
port = os.environ.get('FASTAPI_PORT')
proxy_port = os.environ.get('FASTAPI_PROXY')
host_ip = os.environ.get('FASTAPI_HOST_IP')
host_name = os.environ.get('FASTAPI_HOST_NAME')
mongo_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")

if os.environ.get("FASTAPI_PROD") == "false" or os.environ.get("FASTAPI_PROD") == None:
    port = 8000
    debug = True
    # TODO, assuming these are mongo user and pass
    mongo_username = "root"
    mongo_password = "rootpassword"

    allowed_origins = [f"http://localhost:{proxy_port}", 
    f"https://localhost:{proxy_port}", f"http://{host_name}:{proxy_port}", 
    f"https://{host_name}:{proxy_port}",f"http://{host_ip}:{proxy_port}", 
    f"https://{host_ip}:{proxy_port}", "http://localhost:3000"]
    logger.warn("MODE: development")
else:
    debug = False
    allowed_origins = [f"http://{host_name}:{proxy_port}", f"https://{host_name}:{proxy_port}",
    f"http://{host_ip}:{proxy_port}", f"https://{host_ip}:{proxy_port}", f"http://{host_name}", f"https://{host_name}"]


uri = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=1000)
    db = client["users"]
    fs = gridfs.GridFS(db)
except:
    logger.error("mongo connection failed, are your environment variables set?")

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
async def upload(
    files: List[UploadFile] = File(...), 
    username: str = Form(...), 
    token: Optional[str] = Form(None) # TODO eventually when implementing user tokens, change None (optional) to ... (required), note Form("some value") is a default
    ):
    # TODO not the most efficient --> multiprocessing?
    try: 
        for file in files:
            # original file --> for download
            fs.put(file.file, filename=file.filename, user=username)
        return {"success":True}
    except:
        raise HTTPException(status_code=500, detail="Upload failed")  

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  port=port, reload=debug, debug=debug)


