from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from invoice_reco import app


current_file = Path(__file__)
fixtures_dir = current_file.parent / "fixtures"

@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def test_invoice() -> bytes:
    with open(fixtures_dir / "test_invoice.png", "rb") as invoice_file:
        return invoice_file.read()


def test_not_found_route(test_client: TestClient):
    response = test_client.get("/not_found")
    assert response.status_code == 404


def test_create_file(test_client: TestClient, test_invoice: bytes):
    response = test_client.post(
        "/uploadfile/", files={"file": (str(fixtures_dir/"test_invoice.png"), test_invoice)}
    )
    assert response.status_code == 200


def test_invoice_reco(test_client: TestClient, test_invoice: bytes):
    response = test_client.post(
        "/invoice-reco/", files={"file": (str(fixtures_dir/ "test_invoice.pdf"), test_invoice)}
    )
    assert response.status_code == 200
    invoice_info = response.json()
    assert invoice_info["invoice_number"] == "FRINV2400001423431"
    assert invoice_info["order_date"] == "2024-01-06"
    assert invoice_info["vat_rate"] == 0.2
    assert invoice_info["total_excl_vat"] == 53.24
    assert invoice_info["total_incl_vat"] == 63.89
