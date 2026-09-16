from datetime import datetime, timezone
from itertools import count
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Human Mobility Operations API", version="1.0.0")

_store: dict[str, dict[str, dict[str, Any]]] = {
    "customers": {}, "drivers": {}, "managers": {}, "trips": {},
    "bookings": {}, "payments": {}, "ratings": {}, "support": {},
    "notifications": {}, "audit": {},
}
_sequences = {key: count(1) for key in _store}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create(resource: str, payload: dict[str, Any]) -> dict[str, Any]:
    item_id = f"{resource[:3]}-{next(_sequences[resource]):04d}"
    item = {"id": item_id, **payload, "created_at": now(), "updated_at": now()}
    _store[resource][item_id] = item
    return item


def get(resource: str, item_id: str) -> dict[str, Any]:
    item = _store[resource].get(item_id)
    if not item:
        raise HTTPException(404, f"{resource[:-1].title()} not found")
    return item


def update(resource: str, item_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    item = get(resource, item_id)
    item.update(payload, updated_at=now())
    return item


class CustomerIn(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str
    email: str
    preferred_language: str = "vi"

class DriverIn(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str
    license_number: str
    vehicle_id: str | None = None

class ManagerIn(BaseModel):
    full_name: str = Field(min_length=2)
    phone: str
    region: str

class TripIn(BaseModel):
    customer_id: str
    pickup: str
    dropoff: str
    scheduled_at: datetime | None = None
    passenger_count: int = Field(default=1, ge=1, le=8)

class StatusIn(BaseModel):
    status: str

class PaymentIn(BaseModel):
    booking_id: str
    amount: float = Field(gt=0)
    method: str

class RatingIn(BaseModel):
    booking_id: str
    customer_id: str
    driver_id: str
    score: int = Field(ge=1, le=5)
    comment: str | None = None

class SupportIn(BaseModel):
    customer_id: str
    subject: str
    message: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": app.title}


# Customer: register, profile, trip requests, cancellation, history.
@app.post("/customers", status_code=201)
def register_customer(data: CustomerIn):
    return create("customers", data.model_dump())

@app.get("/customers/{customer_id}")
def customer_profile(customer_id: str):
    return get("customers", customer_id)

@app.patch("/customers/{customer_id}")
def update_customer(customer_id: str, data: CustomerIn):
    return update("customers", customer_id, data.model_dump())

@app.get("/customers/{customer_id}/trips")
def customer_trips(customer_id: str):
    get("customers", customer_id)
    return [trip for trip in _store["trips"].values() if trip["customer_id"] == customer_id]

@app.post("/customers/{customer_id}/trips", status_code=201)
def request_trip(customer_id: str, data: TripIn):
    get("customers", customer_id)
    if data.customer_id != customer_id:
        raise HTTPException(400, "customer_id does not match path")
    return create("trips", {**data.model_dump(mode="json"), "status": "requested"})

@app.post("/trips/{trip_id}/cancel")
def cancel_trip(trip_id: str):
    trip = get("trips", trip_id)
    if trip["status"] in {"completed", "cancelled"}:
        raise HTTPException(409, "Trip cannot be cancelled")
    return update("trips", trip_id, {"status": "cancelled"})


# Driver manager: onboarding, availability, assignment, monitoring, performance.
@app.post("/managers", status_code=201)
def register_manager(data: ManagerIn):
    return create("managers", data.model_dump())

@app.get("/managers/{manager_id}/dashboard")
def manager_dashboard(manager_id: str):
    get("managers", manager_id)
    return {"active_drivers": len([x for x in _store["drivers"].values() if x.get("status") == "available"]), "open_trips": len([x for x in _store["trips"].values() if x.get("status") in {"requested", "assigned"}])}

@app.post("/drivers", status_code=201)
def onboard_driver(data: DriverIn):
    return create("drivers", {**data.model_dump(), "status": "pending_review"})

@app.patch("/drivers/{driver_id}/status")
def set_driver_status(driver_id: str, data: StatusIn):
    return update("drivers", driver_id, {"status": data.status})

@app.post("/trips/{trip_id}/assign/{driver_id}")
def assign_driver(trip_id: str, driver_id: str):
    trip = get("trips", trip_id)
    driver = get("drivers", driver_id)
    if driver.get("status") not in {"available", "online"}:
        raise HTTPException(409, "Driver is not available")
    update("drivers", driver_id, {"status": "busy"})
    return update("trips", trip_id, {"driver_id": driver_id, "status": "assigned"})

@app.get("/managers/{manager_id}/drivers")
def list_driver_team(manager_id: str, status: str | None = None):
    get("managers", manager_id)
    drivers = list(_store["drivers"].values())
    return [driver for driver in drivers if status is None or driver.get("status") == status]


# Trip lifecycle, payments, ratings, support and notifications.
@app.post("/trips/{trip_id}/status")
def update_trip_status(trip_id: str, data: StatusIn):
    return update("trips", trip_id, {"status": data.status})

@app.get("/trips/{trip_id}")
def trip_details(trip_id: str):
    return get("trips", trip_id)

@app.post("/payments", status_code=201)
def create_payment(data: PaymentIn):
    get("trips", data.booking_id)
    return create("payments", {**data.model_dump(), "status": "paid"})

@app.get("/payments/{payment_id}")
def payment_details(payment_id: str):
    return get("payments", payment_id)

@app.post("/ratings", status_code=201)
def rate_trip(data: RatingIn):
    get("trips", data.booking_id)
    return create("ratings", data.model_dump())

@app.post("/support/tickets", status_code=201)
def open_support_ticket(data: SupportIn):
    get("customers", data.customer_id)
    return create("support", {**data.model_dump(), "status": "open"})

@app.patch("/support/tickets/{ticket_id}")
def resolve_support_ticket(ticket_id: str, data: StatusIn):
    return update("support", ticket_id, {"status": data.status})

@app.get("/notifications")
def list_notifications(user_id: str = Query(...)):
    return [item for item in _store["notifications"].values() if item.get("user_id") == user_id]

@app.post("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str):
    return update("notifications", notification_id, {"read": True})
