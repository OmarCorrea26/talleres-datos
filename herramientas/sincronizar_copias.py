"""Refresca las copias de proyectos que el Taller 5 toma de los talleres anteriores.

El Taller 5 empaqueta en contenedores el servicio del Taller 4, el pipeline del
Taller 2 y el muñeco del Taller 3. Para que su zip sea autónomo, esos proyectos
viven copiados en ``05-docker/material/``. La fuente de verdad sigue siendo el
taller de origen: después de cambiar algo allá, se corre este script y las
copias se regeneran. Encima de cada copia se aplican los archivos propios de
Docker que están en ``05-docker/material/_docker/<nombre>/``.

Uso:
    python herramientas/sincronizar_copias.py
"""

from __future__ import annotations

import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESTINO = RAIZ / "05-docker" / "material"
SOBRECAPAS = DESTINO / "_docker"

EXCLUIR = {"__pycache__", ".pytest_cache", ".venv", ".telemetry", ".viz", "*.egg-info", "salida", "dist"}

# nombre de la copia -> (carpeta de origen, elementos a copiar; None = todo)
COPIAS = {
    "script-del-taller-2": (RAIZ / "02-orquestacion-con-kedro" / "material", ["modulo_1", "datos"]),
    "servicio-limpieza": (RAIZ / "04-arquitectura" / "material" / "etapa-limpiar", None),
    "pipeline-kedro": (RAIZ / "02-orquestacion-con-kedro" / "material" / "encuesta-hogares", None),
    "muneco": (
        RAIZ / "03-apis-y-git-colaborativo",
        ["contrato", "datos", "ensamblador", "etapas", "fixtures", "tests", "conftest.py", "pytest.ini", "requirements.txt", "LICENSE"],
    ),
}


def _ignorar(_directorio: str, nombres: list[str]) -> set[str]:
    return {n for n in nombres if n in EXCLUIR or n.endswith(".egg-info")}


def copiar(nombre: str, origen: Path, elementos: list[str] | None):
    destino = DESTINO / nombre
    if destino.exists():
        shutil.rmtree(destino)
    if elementos is None:
        shutil.copytree(origen, destino, ignore=_ignorar)
    else:
        destino.mkdir(parents=True)
        for elemento in elementos:
            fuente = origen / elemento
            if fuente.is_dir():
                shutil.copytree(fuente, destino / elemento, ignore=_ignorar)
            else:
                shutil.copy2(fuente, destino / elemento)
    sobrecapa = SOBRECAPAS / nombre
    if sobrecapa.exists():
        shutil.copytree(sobrecapa, destino, dirs_exist_ok=True)
    (destino / "ORIGEN.md").write_text(
        f"# Copia generada\n\nEste proyecto es una copia de `{origen.relative_to(RAIZ).as_posix()}` "
        f"con los archivos de `05-docker/material/_docker/{nombre}/` encima. "
        "No lo edites aquí: cambia el original o la sobrecapa y corre "
        "`python herramientas/sincronizar_copias.py`.\n",
        encoding="utf-8",
    )
    print(f"{nombre}: copiado desde {origen.relative_to(RAIZ)}")


def main():
    for nombre, (origen, elementos) in COPIAS.items():
        copiar(nombre, origen, elementos)


if __name__ == "__main__":
    main()
