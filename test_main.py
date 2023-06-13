import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html; charset=utf-8"


if __name__ == "__main__":
    pytest.main([__file__])

