import datetime
from typing import Annotated
from sqlmodel import SQLModel, Field


class InvoiceInfo(SQLModel, table=True):
    id: Annotated[int | None, Field(primary_key=True)] = None
    invoice_number: Annotated[str, Field(min_length=1, max_length=255)]
    order_date: datetime.date
    vat_rate: Annotated[float, Field(ge=0.0, le=1.0)]
    total_excl_vat: Annotated[float, Field(ge=0.0)]
    total_incl_vat: Annotated[float, Field(ge=0.0)]
