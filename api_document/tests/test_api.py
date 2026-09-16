from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_customer_requests_and_cancels_trip():
    customer = client.post("/customers", json={"full_name": "Nguyen Van A", "phone": "0900000000", "email": "a@example.com"}).json()
    trip = client.post(f"/customers/{customer['id']}/trips", json={"customer_id": customer["id"], "pickup": "A", "dropoff": "B"}).json()
    assert trip["status"] == "requested"
    cancelled = client.post(f"/trips/{trip['id']}/cancel").json()
    assert cancelled["status"] == "cancelled"


def test_manager_assigns_available_driver():
    manager = client.post("/managers", json={"full_name": "Manager", "phone": "0911111111", "region": "HCM"}).json()
    driver = client.post("/drivers", json={"full_name": "Driver", "phone": "0922222222", "license_number": "B123"}).json()
    client.patch(f"/drivers/{driver['id']}/status", json={"status": "available"})
    customer = client.post("/customers", json={"full_name": "Customer", "phone": "0933333333", "email": "c@example.com"}).json()
    trip = client.post(f"/customers/{customer['id']}/trips", json={"customer_id": customer["id"], "pickup": "A", "dropoff": "B"}).json()
    assigned = client.post(f"/trips/{trip['id']}/assign/{driver['id']}").json()
    assert assigned["driver_id"] == driver["id"]
    assert client.get(f"/managers/{manager['id']}/dashboard").status_code == 200
