from datetime import datetime, timedelta


def test_create_reservation(client):
    table = client.post("/tables/", json={"name": "Test Table", "seats": 2, "location": "Main Hall"}).json()

    reservation_data = {
        "customer_name": "test1",
        "table_id": table["id"],
        "reservation_time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "duration_minutes": 60
    }
    response = client.post("/reservations/", json=reservation_data)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "test1"
    assert data["table_id"] == table["id"]
    assert data["table_location"] == "Main Hall"


def test_get_reservations(client):
    table = client.post("/tables/", json={"name": "Test Table", "seats": 2, "location": "Main Hall"}).json()

    reservation_data = {
        "customer_name": "test2",
        "table_id": table["id"],
        "reservation_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        "duration_minutes": 45
    }
    client.post("/reservations/", json=reservation_data)

    response = client.get("/reservations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(res["customer_name"] == "test2" for res in data)
    assert any(res["table_location"] == "Main Hall" for res in data)


def test_delete_reservation(client):
    table = client.post("/tables/", json={"seats": 2, "location": "Main Hall"}).json()

    reservation_data = {
        "customer_name": "test3",
        "table_id": table["id"],
        "reservation_time": (datetime.utcnow() + timedelta(hours=3)).isoformat(),
        "duration_minutes": 30
    }
    reservation = client.post("/reservations/", json=reservation_data).json()

    delete_response = client.delete(f"/reservations/{reservation['id']}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Резервация столика удалена"

    response = client.get("/reservations")
    data = response.json()
    assert all(res["id"] != reservation["id"] for res in data)
