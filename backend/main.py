from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket

from typing import List, Optional
from PIL import Image 

import gridfs
import uvicorn
import os
import pprint
import io

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
    logger.error("DEVELOPMENT MODE")
    uri = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/"
else:
    debug = False
    allowed_origins = [f"http://{host_name}:{proxy_port}", f"https://{host_name}:{proxy_port}",
    f"http://{host_ip}:{proxy_port}", f"https://{host_ip}:{proxy_port}", f"http://{host_name}", f"https://{host_name}"]
    # with docker magic, docker replaces mongo (the container name) to the proper ip address magic bruh magic
    uri = f"mongodb://{mongo_username}:{mongo_password}@mongo:27017/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    global client, db, fs
    try:
        client = AsyncIOMotorClient(uri)
        db = client["users"]
        fs = AsyncIOMotorGridFSBucket(db)
        logger.error("MONGO CONNECTED") # uhhh error level log because it shows, but doesn't actually break stuff kinda hacky
    except:
        logger.error("ERROR: mongo connection failed, are your environment variables set?")

@app.get("/api/test")
async def test():
    return {"hello": "world"}

@app.get("/api/{username}/files")
async def files(username:str):
    # data = await fs.find({"user": username}).to_list(None)
    cursor = fs.find({"username": username})
    logger.error(await fs.find({"username": username}).to_list(None))
    test = []
    async for gridOut in cursor:
        # logger.error(pprint.pprint(gridOut))
        logger.error(pprint.pprint(gridOut.filename))
        test.append(gridOut.filename)
    # logger.error(pprint.pprint(data))
    logger.error(test)
    return {"username": username}

# TODO this can make a thumnail larger in size(data) for some reason look into
async def gen_thumbnail(file):
    imageBytes = io.BytesIO()
    image = Image.open(file)
    image.thumbnail((200,200))
    image.save(imageBytes, format=image.format)
    imageBytes = imageBytes.getvalue()
    # imageBytes.seek(0) # supposedly this is something you need to do? broke things for me https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
    return imageBytes

async def upload_raw_file(file: UploadFile, username):
    grid_in_og = fs.open_upload_stream(file.filename)
    await grid_in_og.write(file.file)
    await grid_in_og.set("username", username)
    await grid_in_og.set("thumbnail", False)
    await grid_in_og.close()

async def upload_thumb_file(file: UploadFile, username):
    thumbnail = await gen_thumbnail(file.file)
    grid_in_thumb = fs.open_upload_stream(file.filename)
    await grid_in_thumb.write(thumbnail)
    await grid_in_thumb.set("username", username)
    await grid_in_thumb.set("thumbnail", True)
    await grid_in_thumb.close()

@app.post("/api/upload")
async def upload(
    files: List[UploadFile] = File(...), 
    # can't use pydantic model here cause http doesn't allow multipart/form-data and json --> there are fastapi workarounds but messy
    username: str = Form(...), 
    token: Optional[str] = Form(None) # TODO eventually when implementing user tokens, change None (optional) to ... (required), note Form("some value") is a default
    ):
    # TODO not the most efficient --> multiprocessing?
    try: 
        for file in files:
            # original file --> for download
            await upload_raw_file(file, username)
            await upload_thumb_file(file, username)

        return {"success":True}
    except:
        logger.error("ERROR: Files not uploaded")
        raise HTTPException(status_code=500, detail="Upload failed")  

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  port=port, reload=debug, debug=debug)


