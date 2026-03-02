import os
import sys
import base64
from pathlib import Path
import pymupdf
from typing import List



def clean_path(path: str) -> str:
    clean_path = Path(path).as_posix()
    return clean_path


def is_req_file_type(file_path: str) -> bool:
    req_types = [".pdf",".png",".jpg",".jpeg"]

    flag = False
    for req_type in req_types:
        flag = file_path.lower().endswith(req_type)
        if flag == True:
            break
    
    return flag

def is_pdf(file_path: str) -> bool:

    flag = file_path.lower().endswith(".pdf")
    return flag

def convert_pdf_to_base64_images(file_path: str) -> List[str]:
    docs = pymupdf.open(file_path)
    print("Number of pages =", len(docs))
    base64_images = []
    for page in docs:
        pix = page.get_pixmap() # convert pdf into image object
        pix_bytes = pix.tobytes() # convert image object to bytes
        b64_img = base64.b64encode(pix_bytes).decode('utf-8')
        base64_images.append(b64_img)

    return base64_images


def encode_image_base64(file_path: str) -> str:
    with open(file_path, "rb") as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')

        return img_base64