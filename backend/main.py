from fastapi import FastAPI, HTTPException, File, UploadFile, Depends, Form, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.logger import logger
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from collections import defaultdict

from typing import List, Optional
from PIL import Image, ImageOps, ExifTags  # for image related processing, currently resizing images (pil keeps aspect ratio)

import gridfs # mongo specification
import uvicorn
import os # env variables
import pprint # TODO remove debugging
import io # for getting bytes data, convert image file to bytes --> resizing for thumnails then writing
import zipfile # for zipping images and sending back to user
import bson

app = FastAPI()

# configuration
# values from docker file from docker compose from .env
port = os.environ.get('FASTAPI_PORT')
prod = True if os.environ.get("FASTAPI_PROD") == "true" else False
proxy_port = os.environ.get('FASTAPI_PROXY')
host_ip = os.environ.get('FASTAPI_HOST_IP')
host_name = os.environ.get('FASTAPI_HOST_NAME')
mongo_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
mongo_password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
accepted_extensions_list = ["jpg", "jpeg", "JPG", "JPEG", "png", "PNG"]

if os.environ.get("FASTAPI_PROD") == "true": # production
    allowed_origins = [f"https://{host_name}:{proxy_port}", f"https://{host_ip}:{proxy_port}", f"https://{host_ip}", f"https://{host_name}"] # todo check if these last ones are needed
    logger.error("CONTAINER PRODUCTION MODE")
    # with docker magic, docker replaces mongo (the container name) to the proper ip address magic bruh magic
    uri = f"mongodb://{mongo_username}:{mongo_password}@mongo:27017/"
elif os.environ.get("FASTAPI_PROD") == "false": # assumming running with docker container
    # todo cleanup
    allowed_origins = [f"https://{host_name}:{proxy_port}", f"https://{host_ip}:{proxy_port}", f"https://{host_ip}", f"https://{host_name}"] # todo check if these last ones are needed
    logger.error("CONTAINER DEVELOPMENT MODE")
    uri = f"mongodb://{mongo_username}:{mongo_password}@mongo:27017/"
else: # running file itself
    port = 8000
    # TODO, assuming values are what you are using
    mongo_username = "root"
    mongo_password = "rootpassword"
    # todo cleanup
    allowed_origins = ["http://localhost:3000"]
    logger.error("DEVELOPMENT MODE")
    uri = f"mongodb://{mongo_username}:{mongo_password}@localhost:27017/" # note localhost difference

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    global client, db, fs, accepted_extensions
    accepted_extensions = {x:1 for x in accepted_extensions_list}
    try:
        client = AsyncIOMotorClient(uri)
        db = client["users"]
        fs = AsyncIOMotorGridFSBucket(db)
        # below isn't a good indication of connection because fs isn't created --> lazy creation I think --> so possibly do one operation on fs?
        logger.error("MONGO CONNECTED") # uhhh error level log because it shows, but doesn't actually break stuff kinda hacky
    except:
        logger.error("ERROR: mongo connection failed, are your environment variables set?")
        raise Exception("ERROR: mongo connection failed")

@app.get("/api/test")
async def test():
    return {"hello": "world"}

@app.get("/api/{username}/download")
async def download(username:str):
    # data = await fs.find({"user": username}).to_list(None)
    zipped_file = io.BytesIO()
    cursor = fs.find({
        "username": username,
        "raw": True,
        })
    # data = {}
    with zipfile.ZipFile(zipped_file, mode='w', compression=zipfile.ZIP_DEFLATED) as files_zip:
        async for gridOut in cursor:
            files_zip.writestr(gridOut.filename, gridOut.read())
    response = StreamingResponse(iter([zipped_file.getvalue()]), media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=images.zip"
    return response

@app.get("/api/{username}/files")
async def files(username:str, request: Request):
    # data = await fs.find({"user": username}).to_list(None)
    cursor = fs.find({
        "username": username,
        "processed": True,
        })
    data = defaultdict(dict)
    # logger.error(pprint.pprint(request.headers))
    
    # host is a mandatory field
    if "x-forwarded-proto" in request.headers:
        # TODO check if this breaks with nginx reverse proxy
        base = f"{request.headers['x-forwarded-proto']}://{request.headers['host']}" 
    else:
        # assumption that client is using http and not https
        base = f"http://{request.headers['host']}" 

    async for gridOut in cursor:
        file_id = str(gridOut._id)
        # we do a check here since we want the thumbnail in one dict as the original
        # TODO maybe instead of this store in metadata? so then simpler check
        if hasattr(gridOut, "parentID"):
            logger.error("thumbnail")
            parent_file_id = str(gridOut.parentID) 
            thumb_data = {
                "thumb_id": file_id,
                "thumbnail": f"{base}/api/{username}/{file_id}",
                "thumbnailWidth": gridOut.metadata["width"],
                "thumbnailHeight": gridOut.metadata["height"],
            }
            data[parent_file_id].update(thumb_data)
        else:
            original_data = {
                "_id": file_id,
                "filename": gridOut.filename,
                "src": f"{base}/api/{username}/{file_id}",
                "width": gridOut.metadata["width"],
                "height": gridOut.metadata["height"],
                "uploadDate": gridOut.upload_date,
            }
            data[file_id].update(original_data)
        # logger.error(pprint.pprint(data))
    return data

# TODO this can make a thumnail larger in size(data) for some reason look into
async def preprocess_thumb_file(file, filename:str):
    imageBytes = io.BytesIO()
    image = Image.open(file)
    file_format = image.format
    image = ImageOps.exif_transpose(image)
    binary_exif = image.getexif()
    # todo save parsed version of exif data and store in metadata
    # exif_data = image.getexif()
    metadata = {}
    # metadata = {
    #     ExifTags.TAGS[k]: v
    #     for k, v in exif_data.items()
    #     if k in ExifTags.TAGS and type(v) is not bytes
    # }
    image.thumbnail((500,500))
    width, height = image.size
    metadata["width"] = width
    metadata["height"] = height
    image.save(imageBytes, format=file_format)
    imageBytes = imageBytes.getvalue()
    # imageBytes.seek(0) # supposedly this is something you need to do? broke things for me https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
    return imageBytes, metadata

async def preprocess_file(file, filename:str):
    imageBytes = io.BytesIO()
    image = Image.open(file)
    file_format = image.format
    image = ImageOps.exif_transpose(image)
    binary_exif = image.getexif()
    # todo save parsed version of exif data and store in metadata
    # exif_data = image.getexif()
    metadata = {}
    # metadata = {
    #     ExifTags.TAGS[k]: v
    #     for k, v in exif_data.items()
    #     if k in ExifTags.TAGS and type(v) is not bytes
    # }
    width, height = image.size
    metadata["width"] = width
    metadata["height"] = height
    image.save(imageBytes, format=file_format, exif=binary_exif)
    imageBytes = imageBytes.getvalue()
    # imageBytes.seek(0) # supposedly this is something you need to do? broke things for me https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
    return imageBytes, metadata

# TODO could use pil method with quality=100, default is 75
async def upload_raw_file(file: UploadFile, username):
    grid_in = fs.open_upload_stream(file.filename)
    await grid_in.write(file.file)
    await grid_in.set("username", username)
    await grid_in.set("raw", True)
    await grid_in.set("processed", False)
    await grid_in.set("thumbnail", False)
    await grid_in.close()
    return grid_in._id

async def upload_processed_thumb_file(file: UploadFile, name:str, ext:str, username: str, parent_file_id: bson.objectid.ObjectId):
    new_name = f"{name}_thumb.{ext}"
    # TODO exif unsued
    thumbnail, metadata = await preprocess_thumb_file(file.file, new_name)
    grid_in = fs.open_upload_stream(new_name, metadata=metadata)
    await grid_in.write(thumbnail)
    await grid_in.set("username", username)
    await grid_in.set("raw", False)
    await grid_in.set("processed", True)
    await grid_in.set("thumbnail", True)
    await grid_in.set("parentID", parent_file_id)
    await grid_in.close()
    return grid_in._id

async def upload_processed_file(file: UploadFile, name:str, ext:str, username: str):
    new_name = f"{name}_processed.{ext}"
    # TODO exif unsued
    image, metadata = await preprocess_file(file.file, new_name)
    grid_in = fs.open_upload_stream(new_name, metadata=metadata)
    await grid_in.write(image)
    await grid_in.set("username", username)
    await grid_in.set("raw", False)
    await grid_in.set("processed", True)
    await grid_in.set("thumbnail", False)
    await grid_in.close()
    return grid_in._id


@app.get("/api/{username}/{file_id}")
async def get_file(username:str, file_id:str):
    data = await fs.find({"user": username}).to_list(None)
    gridout = await fs.open_download_stream(bson.objectid.ObjectId(file_id))
    if gridout.username != username: #should check tokens or UID for each user once that's implemented
        raise HTTPException(status_code=403, detail="Access forbidden")  
    return StreamingResponse(gridout.__iter__())

prod=False
@app.post("/api/upload")
async def upload(
    files: List[UploadFile] = File(...), 
    # can't use pydantic model here cause http doesn't allow multipart/form-data and json --> there are fastapi workarounds but messy
    username: str = Form(...), 
    token: Optional[str] = Form(None) # TODO eventually when implementing user tokens, change None (optional) to ... (required), note Form("some value") is a default
    ):
    # TODO not the most efficient --> multiprocessing?
    # try: 
    #     for file in files:
    #         name = file.filename.rsplit(".", 1)[0]
    #         ext = file.filename.rsplit(".", 1)[1]
    #         logger.error(file.filename)
    #         if ext not in accepted_extensions:
    #             # TODO check if status codes are right, 406 == not acceptable this right?
    #             raise HTTPException(status_code=406, detail="File extension not accepted")  

    #         # TODO could merge processedfile and thumb file later for optimizations
    #         await upload_raw_file(file, username)
    #         parent_file_id = await upload_processed_file(file, name, ext, username)
    #         await upload_processed_thumb_file(file, name, ext, username, parent_file_id)
    #     return {"success":True}
    # except:
    #     logger.error("ERROR: Files not uploaded")
    #     raise HTTPException(status_code=500, detail="Upload failed")  
    logger.error(accepted_extensions)
    for file in files:
        name = file.filename.rsplit(".", 1)[0]
        ext = file.filename.rsplit(".", 1)[1]
        logger.error(file.filename)
        if ext not in accepted_extensions:
            # TODO check if status codes are right, 406 == not acceptable this right?
            raise HTTPException(status_code=406, detail="File extension not accepted")  

        # TODO could merge processedfile and thumb file later for optimizations
        await upload_raw_file(file, username)
        parent_file_id = await upload_processed_file(file, name, ext, username)
        await upload_processed_thumb_file(file, name, ext, username, parent_file_id)
    return {"success":True}
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",  port=port, reload=not prod, debug=not prod)


