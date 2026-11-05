"""El adaptador HTTP cumple el contrato del Taller 3, verificado contra sus fixtures."""

import json
from collections import Counter
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from limpieza.adaptadores.http import app

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"


@pytest.fixture(scope="module")
def cliente():
    return TestClient(app)


def test_salud(cliente):
    respuesta = cliente.get("/salud")
    assert respuesta.status_code == 200
    assert respuesta.json() == {"etapa": 2, "nombre": "limpiar", "estado": "ok"}


def test_procesar_reproduce_el_resumen_de_referencia(cliente):
    entrada = json.loads((FIXTURES / "etapa_2_entrada.json").read_text(encoding="utf-8"))
    referencia = json.loads((FIXTURES / "etapa_2_salida.json").read_text(encoding="utf-8"))

    respuesta = cliente.post("/procesar", json=entrada)

    assert respuesta.status_code == 200
    salida = respuesta.json()
    assert salida["resumen"] == referencia["resumen"]
    assert len(salida["registros"]) == referencia["resumen"]["n_salida"]


def test_procesar_cumple_las_reglas_del_contrato(cliente):
    """Las mismas verificaciones que hace validar_etapa_2 en el muñeco."""
    entrada = json.loads((FIXTURES / "etapa_2_entrada.json").read_text(encoding="utf-8"))
    salida = cliente.post("/procesar", json=entrada).json()
    registros = salida["registros"]

    assert all(c == 1 for c in Counter(r["id_persona"] for r in registros).values())
    assert not any(r["ocupado"] == 1 and r["ingreso"] is None for r in registros)
    assert sum(1 for r in registros if r["ingreso_imputado"]) == salida["resumen"]["n_imputados"]
    assert max(r["ingreso"] for r in registros if r["ingreso"] is not None) <= 20_000_000


def test_procesar_rechaza_una_entrada_vacia(cliente):
    assert cliente.post("/procesar", json={"registros": []}).status_code == 422


def test_la_politica_viaja_en_la_peticion(cliente):
    entrada = json.loads((FIXTURES / "etapa_2_entrada.json").read_text(encoding="utf-8"))
    entrada["politica"] = {"percentil_atipicos": 0.9}
    salida = cliente.post("/procesar", json=entrada).json()
    assert "percentil 90" in salida["resumen"]["metodo_imputacion"]
