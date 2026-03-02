from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from services.invoice_pipeline import process_invoice
from services.storage_service import (
    fetch_all_invoices,
    fetch_invoice_by_id
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/extract-invoice", response_class=HTMLResponse)
async def extract_invoice(request: Request, file:UploadFile =File(...)):

    result = process_invoice(file)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "invoice": result["invoice"],
            "images": result["images"],
            "mongo_id": result["mongo_id"]
        }
    ) 



@router.get("/invoices", response_class=HTMLResponse)
def invoice_history(request: Request):
    invoices = fetch_all_invoices()  # We will create this

    return templates.TemplateResponse(
        "history.html",
        {
            "request": request,
            "invoices": invoices
        }
    )


@router.get("/invoice/{invoice_id}", response_class=HTMLResponse)
def invoice_detail(request: Request, invoice_id: str):
    invoice = fetch_invoice_by_id(invoice_id)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "invoice": invoice,
            "images": invoice["base64_images"],
            "mongo_id": invoice_id
        }
    )