import datetime
import typing as t
from pydantic import PlainSerializer
from sqlmodel import SQLModel, Field


class InvoiceInfo(SQLModel, table=True):
    id: t.Annotated[int | None, Field(primary_key=True)] = None
    invoice_number: t.Annotated[str, Field(min_length=1, max_length=255)]
    order_date: t.Annotated[datetime.date, PlainSerializer(lambda x: x.strftime("%Y-%m-%d"))]
    vat_rate: t.Annotated[float, Field(ge=0.0, le=1.0)]
    total_excl_vat: t.Annotated[float, Field(ge=0.0)]
    total_incl_vat: t.Annotated[float, Field(ge=0.0)]
