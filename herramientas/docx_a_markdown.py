"""Convierte una guía de taller en formato .docx a Markdown.

Las guías de los talleres se escribieron originalmente en Word con una
convención fija: encabezados con estilos Heading 1 a 3, bloques de código en
tablas de una celda con fondo gris y fuente Consolas, y llamados de atención
(Tip, Atención, Checkpoint, Concepto) en tablas de una celda con fondo de color.
Este script recorre el documento en orden y traduce cada una de esas piezas a
su equivalente en Markdown de GitHub: encabezados, bloques de código cercados,
alertas y tablas.

Uso:
    python herramientas/docx_a_markdown.py guia.docx salida.md --img carpeta_img
"""

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import docx
from docx.document import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.text.run import Run

COLOR_CODIGO = {"F2F2F2"}
COLOR_ALERTA = {
    "D5E8F0": "TIP",
    "D9E2F3": "TIP",
    "E2EFDA": "TIP",
    "E2EFD9": "IMPORTANT",
    "FFF2CC": "WARNING",
    "FCE4D6": "WARNING",
    "EDE7F6": "NOTE",
}
ETIQUETAS_ALERTA = {
    "tip": "TIP",
    "atención": "WARNING",
    "atencion": "WARNING",
    "checkpoint": "IMPORTANT",
    "concepto": "NOTE",
}
NOMBRE_ALERTA = {"TIP": "Tip", "WARNING": "Atención", "IMPORTANT": "Checkpoint", "NOTE": "Concepto"}
FUENTES_CODIGO = {"Consolas", "Courier New", "Cascadia Code"}

INICIOS_SHELL = (
    "cd ", "pip ", "python ", "py ", "git ", ".venv", "source ", "uvicorn ", "pytest",
    "mkdir ", "dir", "ls", "code ", "kedro ", "Set-ExecutionPolicy", "Remove-Item",
    "curl ", "Invoke-", "winget ", "del ", "type ", "cat ", "echo ", "docker ", "where ",
    "which ", "deactivate", "jupyter ", "Rscript ", "bash ", ".\\", "./",
)


def color_de_celda(celda) -> str | None:
    tc_pr = celda._tc.tcPr
    if tc_pr is None:
        return None
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        return None
    fill = shd.get(qn("w:fill"))
    return fill.upper() if fill else None


def es_fuente_codigo(run) -> bool:
    nombre = run.font.name
    if nombre is None:
        r_pr = run._r.rPr
        if r_pr is not None and r_pr.rFonts is not None:
            nombre = r_pr.rFonts.get(qn("w:ascii"))
    return nombre in FUENTES_CODIGO


class Conversor:
    def __init__(self, documento: Document, carpeta_img: Path, prefijo_img: str):
        self.doc = documento
        self.carpeta_img = carpeta_img
        self.prefijo_img = prefijo_img
        self.contador_img = 0
        self.imagenes_vistas: dict[str, str] = {}
        self.lineas: list[str] = []
        self.en_lista_numerada = False

    # ------------------------------------------------------------------ runs
    def _texto_run(self, run) -> str:
        texto = run.text
        drawing = run._r.find(".//" + qn("w:drawing"))
        if drawing is not None:
            return self._extraer_imagen(drawing)
        if not texto:
            return ""
        if es_fuente_codigo(run):
            return f"`{texto}`"
        negrita = bool(run.bold)
        cursiva = bool(run.italic)
        if negrita and cursiva:
            return f"***{texto}***"
        if negrita:
            return f"**{texto}**"
        if cursiva:
            return f"*{texto}*"
        return texto

    def _extraer_imagen(self, drawing) -> str:
        blip = drawing.find(".//" + qn("a:blip"))
        if blip is None:
            return ""
        r_id = blip.get(qn("r:embed"))
        parte = self.doc.part.related_parts[r_id]
        huella = hashlib.sha1(parte.blob).hexdigest()
        if huella not in self.imagenes_vistas:
            self.contador_img += 1
            extension = Path(str(parte.partname)).suffix or ".png"
            nombre = f"{self.prefijo_img}_{self.contador_img:02d}{extension}"
            self.carpeta_img.mkdir(parents=True, exist_ok=True)
            (self.carpeta_img / nombre).write_bytes(parte.blob)
            self.imagenes_vistas[huella] = nombre
        return f"![]({self.carpeta_img.name}/{self.imagenes_vistas[huella]})"

    def _texto_parrafo(self, parrafo: Paragraph) -> str:
        piezas: list[str] = []
        for hijo in parrafo._p.iterchildren():
            if hijo.tag == qn("w:r"):
                piezas.append(self._texto_run(Run(hijo, parrafo)))
            elif hijo.tag == qn("w:hyperlink"):
                texto = "".join(self._texto_run(Run(r, parrafo)) for r in hijo.findall(qn("w:r")))
                r_id = hijo.get(qn("r:id"))
                destino = self.doc.part.rels[r_id].target_ref if r_id else None
                if destino and destino != texto.strip("`"):
                    piezas.append(f"[{texto}]({destino})")
                else:
                    piezas.append(texto)
        texto = "".join(piezas)
        # Word parte una misma frase en varios runs; unimos las marcas contiguas.
        texto = re.sub(r"\*\*\s*\*\*", "", texto)
        texto = re.sub(r"`\s*`", "", texto)
        return texto.strip()

    # ------------------------------------------------------------- párrafos
    def _nivel_lista(self, parrafo: Paragraph):
        p_pr = parrafo._p.pPr
        if p_pr is None or p_pr.numPr is None:
            return None
        num_id = p_pr.numPr.numId.val if p_pr.numPr.numId is not None else None
        ilvl = p_pr.numPr.ilvl.val if p_pr.numPr.ilvl is not None else 0
        formato = "bullet"
        try:
            numbering = self.doc.part.numbering_part.element
            num = numbering.find(f".//{qn('w:num')}[@{qn('w:numId')}='{num_id}']")
            abs_id = num.find(qn("w:abstractNumId")).get(qn("w:val"))
            abstracto = numbering.find(f".//{qn('w:abstractNum')}[@{qn('w:abstractNumId')}='{abs_id}']")
            lvl = abstracto.find(f"{qn('w:lvl')}[@{qn('w:ilvl')}='{ilvl}']")
            formato = lvl.find(qn("w:numFmt")).get(qn("w:val"))
        except Exception:
            pass
        return int(ilvl), formato

    def parrafo(self, parrafo: Paragraph):
        try:
            estilo = parrafo.style.name if parrafo.style is not None else ""
        except Exception:
            estilo = ""
        texto = self._texto_parrafo(parrafo)
        if estilo.startswith("Heading"):
            nivel = int(estilo.split()[-1])
            self.en_lista_numerada = False
            self.lineas.append("")
            self.lineas.append("#" * nivel + " " + texto)
            self.lineas.append("")
            return
        if not texto:
            return
        lista = self._nivel_lista(parrafo)
        if lista is not None or estilo.startswith("List"):
            nivel, formato = lista if lista is not None else (0, "bullet")
            numerada = formato != "bullet"
            marca = "1." if numerada else "-"
            # Una viñeta que sigue a un ítem numerado sin salto es una sublista.
            if not numerada and self.en_lista_numerada and nivel == 0:
                nivel = 1
            ultima = self.lineas[-1] if self.lineas else ""
            if ultima and not re.match(r"^\s*(-|\d+\.) ", ultima):
                self.lineas.append("")
            self.lineas.append("   " * nivel + f"{marca} {texto}")
            self.en_lista_numerada = numerada or (self.en_lista_numerada and nivel > 0)
            return
        self.en_lista_numerada = False
        if self.lineas and self.lineas[-1] != "":
            self.lineas.append("")
        self.lineas.append(texto)

    # ---------------------------------------------------------------- tablas
    def _bloque_codigo(self, celda):
        lineas = [p.text.rstrip() for p in celda.paragraphs]
        while lineas and not lineas[-1]:
            lineas.pop()
        while lineas and not lineas[0]:
            lineas.pop(0)
        self.lineas.append("")
        self.lineas.append("```" + self._lenguaje(lineas))
        self.lineas.extend(lineas)
        self.lineas.append("```")
        self.lineas.append("")

    @staticmethod
    def _lenguaje(lineas: list[str]) -> str:
        if not lineas:
            return ""
        primera = lineas[0].lstrip()
        texto = "\n".join(lineas)
        if primera.startswith(INICIOS_SHELL):
            return "powershell"
        if re.search(r"^(import |from \w+ import|def |class |@app|@pytest|print\(|if __name__)", texto, re.M):
            return "python"
        if re.search(r"^\w[\w\-]*:\s*$", texto, re.M) and ":" in primera:
            return "yaml"
        if primera.startswith("{") or primera.startswith("["):
            return "json"
        if re.search(r"^\s*(library\(|function\(|<-)", texto, re.M):
            return "r"
        return "text"

    def _alerta(self, celda, tipo: str | None):
        parrafos = [self._texto_parrafo(p) for p in celda.paragraphs]
        parrafos = [p for p in parrafos if p]
        if not parrafos:
            return
        primero = parrafos[0]
        coincidencia = re.match(r"^\**\s*([💡⚠️✅📘🧪]+)\s*\**\s*([A-Za-zÁ-ú]+)\**\s*(.*)$", primero, re.S)
        if coincidencia:
            emoji, etiqueta, resto = coincidencia.groups()
            tipo = ETIQUETAS_ALERTA.get(etiqueta.lower(), tipo or "NOTE")
            encabezado = f"**{emoji.strip()} {NOMBRE_ALERTA[tipo]}**"
            cuerpo = ([resto.strip()] if resto.strip() else []) + parrafos[1:]
        else:
            tipo = tipo or "NOTE"
            encabezado = None
            cuerpo = parrafos
        self.lineas.append("")
        self.lineas.append(f"> [!{tipo}]")
        if encabezado:
            self.lineas.append(f"> {encabezado}")
            if cuerpo:
                self.lineas.append(">")
        for i, p in enumerate(cuerpo):
            if i:
                self.lineas.append(">")
            self.lineas.append(f"> {p}")
        self.lineas.append("")

    def _tabla_datos(self, tabla: Table):
        filas = []
        for fila in tabla.rows:
            celdas = []
            for celda in fila.cells:
                texto = " ".join(self._texto_parrafo(p) for p in celda.paragraphs).strip()
                celdas.append(texto.replace("|", "\\|"))
            filas.append(celdas)
        ancho = max(len(f) for f in filas)
        self.lineas.append("")
        encabezado = [c.strip("*") for c in filas[0]] + [""] * (ancho - len(filas[0]))
        self.lineas.append("| " + " | ".join(encabezado) + " |")
        self.lineas.append("|" + "|".join(["----"] * ancho) + "|")
        for fila in filas[1:]:
            fila = fila + [""] * (ancho - len(fila))
            self.lineas.append("| " + " | ".join(fila) + " |")
        self.lineas.append("")

    def tabla(self, tabla: Table):
        n_filas, n_cols = len(tabla.rows), len(tabla.columns)
        if n_cols == 1:
            for fila in tabla.rows:
                celda = fila.cells[0]
                color = color_de_celda(celda)
                fuentes = {r.font.name for p in celda.paragraphs for r in p.runs}
                if color in COLOR_CODIGO or (color is None and fuentes & FUENTES_CODIGO):
                    self._bloque_codigo(celda)
                else:
                    self._alerta(celda, COLOR_ALERTA.get(color or ""))
            return
        tiene_imagenes = any(c._tc.find(".//" + qn("w:drawing")) is not None for c in tabla.rows[0].cells)
        if n_filas == 1 and tiene_imagenes:
            imagenes = [self._texto_parrafo(p) for c in tabla.rows[0].cells for p in c.paragraphs]
            self.lineas.append("")
            self.lineas.append(" ".join(i for i in imagenes if i))
            self.lineas.append("")
            return
        self._tabla_datos(tabla)

    # ------------------------------------------------------------ documento
    def convertir(self) -> str:
        cuerpo = self.doc.element.body
        for hijo in cuerpo.iterchildren():
            if hijo.tag == qn("w:p"):
                self.parrafo(Paragraph(hijo, self.doc))
            elif hijo.tag == qn("w:tbl"):
                self.tabla(Table(hijo, self.doc))
        salida = "\n".join(self.lineas)
        salida = re.sub(r"\n{3,}", "\n\n", salida)
        return salida.strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entrada", type=Path)
    parser.add_argument("salida", type=Path)
    parser.add_argument("--img", type=Path, default=None, help="carpeta donde guardar las imágenes")
    parser.add_argument("--prefijo-img", default="figura")
    args = parser.parse_args()
    carpeta_img = args.img or args.salida.parent / "img"
    conversor = Conversor(docx.Document(str(args.entrada)), carpeta_img, args.prefijo_img)
    args.salida.parent.mkdir(parents=True, exist_ok=True)
    args.salida.write_text(conversor.convertir(), encoding="utf-8")
    print(f"{args.entrada.name} -> {args.salida} ({len(conversor.lineas)} lineas, {conversor.contador_img} imagenes)")


if __name__ == "__main__":
    main()
