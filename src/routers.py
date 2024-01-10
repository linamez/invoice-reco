import logging
import datetime as dt
from fastapi import APIRouter, UploadFile
from src import openai
from src.models import InvoiceInfo
from src.db import create_db_and_tables, add_invoice_info


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

create_db_and_tables()


@router.post("/uploadfile/")
async def upload_file(file: UploadFile) -> dict:
    logger.info(f"Received file: {file.filename}")
    return {"filename": file.filename}


@router.post("/invoice/reco/")
def invoice_reco(file: UploadFile) -> InvoiceInfo:
    prompt = """This image is an invoice. Extract the required information to fill the following JSON object:
    
    {
        invoice_number: string,
        order_date: datetime.date,
        vat_rate: float,    # between 0 and 1
        total_excl_vat: float,
        total_incl_vat: float,
    }
    """
    data = openai.call_gpt4vision(prompt, file.file.read())
    logger.info(data)

    # ensure the order date is earlier than today
    order_date = dt.datetime.strptime(f"{data['order_date']}", "%Y-%m-%d")
    if order_date > dt.datetime.now():
        raise ValueError("The order date cannot be later than today.")

    invoice_info = InvoiceInfo(
        invoice_number=data.get("invoice_number", ""),
        order_date=order_date,
        vat_rate=data.get("vat_rate", 0.0),
        total_excl_vat=data.get("total_excl_vat", 0.0),
        total_incl_vat=data.get("total_incl_vat", 0.0),
    )

    # add invoice info to database
    add_invoice_info(invoice_info)
    return invoice_info
