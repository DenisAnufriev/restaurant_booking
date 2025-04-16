from fastapi.testclient import TestClient

from app.main import app  # замените на актуальный импорт вашего FastAPI-приложения

client = TestClient(app)


def test_create_table(client):
    table_data = {
        "name": "Table A",
        "seats": 4,
        "location": "Main Hall"
    }
    response = client.post("/tables/", json=table_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Table A"
    assert data["seats"] == 4
    assert data["location"] == "Main Hall"
    assert "id" in data
