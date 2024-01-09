import logging
from datetime import datetime
from fastapi import APIRouter, UploadFile
from pydantic import BaseModel
from src import openai

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


router = APIRouter()


@router.post("/uploadfile/")
async def upload_file(file: UploadFile):
    logger.info(f"Received file: {file.filename}")
    return {"filename": file.filename}


class InvoiceInfo(BaseModel):
    invoice_number: str
    order_date: datetime
    vat_rate: float
    total_excl_vat: float
    total_incl_vat: float


@router.post("/invoice/reco/")
def invoice_reco(file: UploadFile) -> InvoiceInfo:
    prompt = """This image is an invoice. Extract the required information to fill the following JSON object:
    
    {
        invoice_number: string,
        order_date: datetime,
        vat_rate: float,    # between 0 and 1
        total_excl_vat: float,
        total_incl_vat: float,
    }
    """
    data = openai.call_gpt4vision(prompt, file.file.read())
    logger.info(data)

    return InvoiceInfo(
        invoice_number=data.get("invoice_number", ""),
        order_date=data.get("order_date", ""),
        vat_rate=data.get("vat_rate", 0.0),
        total_excl_vat=data.get("total_excl_vat", 0.0),
        total_incl_vat=data.get("total_incl_vat", 0.0),
    )
