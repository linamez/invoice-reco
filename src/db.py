from sqlmodel import SQLModel, Session, create_engine
from src.models import InvoiceInfo


sqlite_file_name = "invoice_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def add_invoice_info(invoice_info: InvoiceInfo) -> None:
    with Session(engine) as session:
        session.add(invoice_info)
        session.commit()
        session.refresh(invoice_info)
