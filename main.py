import os
from typing import BinaryIO

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from utag.utag import UTagReader

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



def getDataFromTaggedFile(file: BinaryIO, savePath: str):
    os.makedirs(os.path.dirname(savePath), exist_ok=True)
    utagreader = UTagReader()
    utagreader.fromTaggedFile(file)
    utagreader.toJSONFile(savePath)


@app.post("/get_data_from_tagged_file")
async def get_data_from_tagged_file(file: UploadFile, savePath: str):
    return getDataFromTaggedFile(file.file, savePath)