"""Empaqueta un taller: genera la guía en .docx y un .zip listo para enviar.

Cada carpeta de taller tiene un archivo ``taller.toml`` con el título, el
subtítulo y el nombre del archivo de salida, y una carpeta ``guia/`` con los
capítulos en Markdown numerados (``00-portada.md``, ``01-introduccion.md``,
etc.). El Markdown es la fuente de verdad; este script lo concatena, convierte
los llamados de atención de GitHub (``> [!TIP]``) en estilos de Word y produce:

* ``dist/<taller>/<nombre>.docx``  la guía completa, con tabla de contenido.
* ``dist/<taller>.zip``            el taller entero, con la guía en docx adentro
                                   y sin las carpetas que no deben llegar a
                                   quien lo recibe (``facilitador/``, entornos,
                                   caches).

Uso:
    python herramientas/empaquetar.py                 # todos los talleres
    python herramientas/empaquetar.py 03-apis-y-git-colaborativo
    python herramientas/empaquetar.py --con-facilitador 03-apis-y-git-colaborativo
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
import tomllib
import zipfile
from pathlib import Path

import docx
import pypandoc
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

RAIZ = Path(__file__).resolve().parent.parent
DIST = RAIZ / "dist"

EXCLUIR_SIEMPRE = {".venv", "__pycache__", ".pytest_cache", ".ipynb_checkpoints", "dist", ".git"}
EXCLUIR_ALUMNOS = {"facilitador"}

# Tipo de alerta de GitHub -> (nombre del estilo en Word, color de fondo, color del borde)
ESTILOS_ALERTA = {
    "TIP": ("Alerta Tip", "D5E8F0", "2E75B6"),
    "WARNING": ("Alerta Atencion", "FFF2CC", "BF9000"),
    "IMPORTANT": ("Alerta Checkpoint", "E2EFD9", "548235"),
    "NOTE": ("Alerta Concepto", "EDE7F6", "7030A0"),
    "CAUTION": ("Alerta Atencion", "FFF2CC", "BF9000"),
}

SALTO_DE_PAGINA = '\n\n```{=openxml}\n<w:p><w:r><w:br w:type="page"/></w:r></w:p>\n```\n\n'


# ----------------------------------------------------------------- markdown
def alertas_a_divs(markdown: str) -> str:
    """Convierte bloques ``> [!TIPO]`` en divs con ``custom-style`` para Word."""
    lineas = markdown.splitlines()
    salida: list[str] = []
    i = 0
    while i < len(lineas):
        coincidencia = re.match(r"^> \[!(\w+)\]\s*$", lineas[i])
        if not coincidencia:
            salida.append(lineas[i])
            i += 1
            continue
        tipo = coincidencia.group(1).upper()
        estilo = ESTILOS_ALERTA.get(tipo, ESTILOS_ALERTA["NOTE"])[0]
        cuerpo: list[str] = []
        i += 1
        while i < len(lineas) and lineas[i].startswith(">"):
            cuerpo.append(re.sub(r"^>\s?", "", lineas[i]))
            i += 1
        salida.append("")
        salida.append(f'::: {{custom-style="{estilo}"}}')
        salida.extend(cuerpo)
        salida.append(":::")
        salida.append("")
    return "\n".join(salida)


def dimensionar_imagenes(markdown: str) -> str:
    """Limita el ancho de las imágenes en Word sin ensuciar el Markdown de GitHub.

    Varias imágenes en una misma línea se reparten el ancho; una sola ocupa
    menos de la mitad de la página, que es lo que pide una captura de pantalla
    o un diagrama pequeño.
    """
    patron = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")

    def ajustar_linea(linea: str) -> str:
        cantidad = len(patron.findall(linea))
        if cantidad == 0 or linea.lstrip().startswith("```"):
            return linea
        ancho = "28%" if cantidad >= 3 else "40%" if cantidad == 2 else "45%"
        return patron.sub(lambda m: f"![{m.group(1)}]({m.group(2)}){{width={ancho}}}", linea)

    return "\n".join(ajustar_linea(linea) for linea in markdown.splitlines())


def armar_markdown(carpeta_guia: Path) -> str:
    capitulos = sorted(p for p in carpeta_guia.glob("*.md"))
    piezas = [dimensionar_imagenes(alertas_a_divs(p.read_text(encoding="utf-8"))) for p in capitulos]
    return SALTO_DE_PAGINA.join(piezas)


# -------------------------------------------------------------- referencia
def _sombrear(estilo, fondo: str, borde: str):
    p_pr = estilo.element.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fondo)
    p_pr.append(shd)
    bordes = OxmlElement("w:pBdr")
    izquierdo = OxmlElement("w:left")
    izquierdo.set(qn("w:val"), "single")
    izquierdo.set(qn("w:sz"), "24")
    izquierdo.set(qn("w:space"), "6")
    izquierdo.set(qn("w:color"), borde)
    bordes.append(izquierdo)
    p_pr.append(bordes)
    estilo.paragraph_format.left_indent = Pt(8)
    estilo.paragraph_format.space_before = Pt(4)
    estilo.paragraph_format.space_after = Pt(4)


def crear_referencia(destino: Path) -> Path:
    """Genera el reference.docx de pandoc con los estilos de alerta y código."""
    base = destino / "referencia.docx"
    subprocess.run(
        [pypandoc.get_pandoc_path(), "-o", str(base), "--print-default-data-file", "reference.docx"],
        check=True,
    )
    documento = docx.Document(str(base))
    estilos = documento.styles
    normal = estilos["Normal"]
    normal.font.name = "Calibri"
    normal.font.size = Pt(11)
    for nombre, fondo, borde in ESTILOS_ALERTA.values():
        if nombre in [s.name for s in estilos]:
            continue
        estilo = estilos.add_style(nombre, docx.enum.style.WD_STYLE_TYPE.PARAGRAPH)
        estilo.base_style = normal
        _sombrear(estilo, fondo, borde)
    for nombre in ("Source Code", "Verbatim Char"):
        try:
            estilo = estilos[nombre]
        except KeyError:
            continue
        estilo.font.name = "Consolas"
        estilo.font.size = Pt(9.5)
    try:
        _sombrear(estilos["Source Code"], "F2F2F2", "BFBFBF")
    except KeyError:
        pass
    for nivel, tamano in (("Heading 1", 20), ("Heading 2", 15), ("Heading 3", 12.5)):
        estilo = estilos[nivel]
        estilo.font.color.rgb = RGBColor(0x1F, 0x2A, 0x44)
        estilo.font.size = Pt(tamano)
        estilo.font.bold = True
    documento.save(str(base))
    return base


# ------------------------------------------------------------------- docx
def _sombrear_celda(celda, fondo: str):
    tc_pr = celda._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fondo)
    tc_pr.append(shd)


def _bordear_tabla(tabla, color: str = "BFBFBF"):
    tbl_pr = tabla._tbl.tblPr
    bordes = OxmlElement("w:tblBorders")
    for lado in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borde = OxmlElement(f"w:{lado}")
        borde.set(qn("w:val"), "single")
        borde.set(qn("w:sz"), "4")
        borde.set(qn("w:space"), "0")
        borde.set(qn("w:color"), color)
        bordes.append(borde)
    tbl_pr.append(bordes)


def embellecer_docx(ruta: Path):
    """Retoques que pandoc no hace solo: bordes y encabezado en tablas, fondo del código."""
    documento = docx.Document(str(ruta))
    for tabla in documento.tables:
        _bordear_tabla(tabla)
        for celda in tabla.rows[0].cells:
            _sombrear_celda(celda, "D9E2F3")
            for parrafo in celda.paragraphs:
                for run in parrafo.runs:
                    run.bold = True
    for parrafo in documento.paragraphs:
        if parrafo.style.name == "Source Code":
            p_pr = parrafo._p.get_or_add_pPr()
            shd = OxmlElement("w:shd")
            shd.set(qn("w:val"), "clear")
            shd.set(qn("w:color"), "auto")
            shd.set(qn("w:fill"), "F2F2F2")
            p_pr.append(shd)
    documento.save(str(ruta))


def generar_docx(taller: Path, config: dict, carpeta_salida: Path) -> Path:
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    salida = carpeta_salida / f"{config['nombre_archivo']}.docx"
    with tempfile.TemporaryDirectory() as tmp:
        temporal = Path(tmp)
        referencia = crear_referencia(temporal)
        markdown = armar_markdown(taller / "guia")
        entrada = temporal / "guia.md"
        entrada.write_text(markdown, encoding="utf-8")
        pypandoc.convert_file(
            str(entrada),
            "docx",
            format="markdown+pipe_tables+fenced_divs+raw_attribute+backtick_code_blocks+link_attributes-smart",
            outputfile=str(salida),
            extra_args=[
                f"--reference-doc={referencia}",
                f"--resource-path={taller / 'guia'}",
                "--toc",
                "--toc-depth=2",
                "-M", "toc-title=Contenido",
                "-M", f"title={config['titulo']}",
                "-M", f"subtitle={config.get('subtitulo', '')}",
                "-M", f"date={config.get('fecha', '')}",
                "-M", "lang=es",
            ],
        )
    embellecer_docx(salida)
    return salida


# -------------------------------------------------------------------- zip
def generar_zip(taller: Path, docx_generado: Path, con_facilitador: bool) -> Path:
    destino = DIST / f"{taller.name}.zip"
    excluir = set(EXCLUIR_SIEMPRE) | (set() if con_facilitador else EXCLUIR_ALUMNOS)
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as zf:
        for archivo in sorted(taller.rglob("*")):
            relativo = archivo.relative_to(taller)
            if archivo.is_dir() or excluir & set(relativo.parts):
                continue
            zf.write(archivo, Path(taller.name) / relativo)
        zf.write(docx_generado, Path(taller.name) / docx_generado.name)
    return destino


# ------------------------------------------------------------------- main
def talleres_disponibles() -> list[Path]:
    return sorted(p for p in RAIZ.iterdir() if p.is_dir() and (p / "taller.toml").exists())


def empaquetar(taller: Path, con_facilitador: bool):
    config = tomllib.loads((taller / "taller.toml").read_text(encoding="utf-8"))
    carpeta = DIST / taller.name
    if carpeta.exists():
        shutil.rmtree(carpeta)
    generado = generar_docx(taller, config, carpeta)
    comprimido = generar_zip(taller, generado, con_facilitador)
    print(f"{taller.name}: {generado.relative_to(RAIZ)} y {comprimido.relative_to(RAIZ)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("talleres", nargs="*", help="carpetas de taller; vacío = todas")
    parser.add_argument("--con-facilitador", action="store_true", help="incluye la carpeta facilitador/ en el zip")
    args = parser.parse_args()
    DIST.mkdir(exist_ok=True)
    seleccion = [RAIZ / t for t in args.talleres] if args.talleres else talleres_disponibles()
    for taller in seleccion:
        if not (taller / "taller.toml").exists():
            raise SystemExit(f"{taller} no tiene taller.toml")
        empaquetar(taller, args.con_facilitador)


if __name__ == "__main__":
    main()
