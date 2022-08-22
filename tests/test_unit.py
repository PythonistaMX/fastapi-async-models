import os
from copy import deepcopy
from fastapi.testclient import TestClient
from pytest_asyncio import fixture
from data import DATOS_PRUEBA
from app.main import startup_event, app


@fixture
async def inicio(scope="module"):
    if os.path.exists("./db.sqlite3"):
        os.remove("./db.sqlite3")
    await startup_event()


def test_get_alumnos(inicio):
    client = TestClient(app)
    response = client.get("/api/")
    assert response.status_code == 200
    alumnos_respuesta = response.json()
    assert alumnos_respuesta == DATOS_PRUEBA


def test_get_alumno(inicio):
    client = TestClient(app)
    for alumno in DATOS_PRUEBA:
        response = client.get(f"/api/{alumno['cuenta']}")
        assert response.status_code == 200
        assert response.json() == alumno


def test_get_alumno_404(inicio):
    client = TestClient(app)
    response = client.get(f"/api/1234568")
    assert response.status_code == 404


def test_post_alumno(inicio):
    client = TestClient(app)
    alumno = deepcopy(DATOS_PRUEBA[0])
    cuenta = alumno.pop("cuenta")
    response = client.post(f"/api/1234567", json=alumno)
    assert response.status_code == 200


def test_post_alumno_409(inicio):
    client = TestClient(app)
    alumno = deepcopy(DATOS_PRUEBA[0])
    cuenta = alumno.pop("cuenta")
    response = client.post(f"/api/{cuenta}", json=alumno)
    assert response.status_code == 409


def test_put_alumno(inicio):
    client = TestClient(app)
    alumno = deepcopy(DATOS_PRUEBA[0])
    cuenta = alumno.pop("cuenta")
    response = client.put(f"/api/{cuenta}", json=alumno)
    assert response.status_code == 200


def test_put_alumno_404(inicio):
    client = TestClient(app)
    alumno = deepcopy(DATOS_PRUEBA[0])
    cuenta = alumno.pop("cuenta")
    response = client.put(f"/api/1234568", json=alumno)
    assert response.status_code == 404
 

def test_delete_alumno(inicio):
    client = TestClient(app)
    alumno = deepcopy(DATOS_PRUEBA[0])
    cuenta = alumno.pop("cuenta")
    response = client.delete(f"/api/1234568", json=alumno)
    assert response.status_code == 404
    response = client.delete(f"/api/{cuenta}", json=alumno)
    assert response.status_code == 200


def test_delete_alumno_404(inicio):
    client = TestClient(app)
    alumno = deepcopy(DATOS_PRUEBA[0])
    cuenta = alumno.pop("cuenta")
    response = client.delete(f"/api/1234568", json=alumno)
    assert response.status_code == 404 