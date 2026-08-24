from __future__ import annotations

from pathlib import Path
from typing import Iterable

from PIL import Image as PILImage
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
BRAND = ROOT / "assets" / "pdf-brand"
OUT.mkdir(parents=True, exist_ok=True)

W, H = A4
DEEP = HexColor("#052F3D")
INK = HexColor("#063848")
PAPER = HexColor("#F7F4E9")
LIME = HexColor("#C8FF00")
GREEN = HexColor("#00E878")
VIOLET = HexColor("#A291F2")
MINT = HexColor("#DDF7F0")
LILAC = HexColor("#EEE9FF")
PALE = HexColor("#F1F4F3")
PALE_LIME = HexColor("#F1FFD0")
MUTED = HexColor("#607985")

pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Narrow-Bold", r"C:\Windows\Fonts\ARIALNB.TTF"))


def pstyle(name: str, size: float, leading: float | None = None, color=INK,
           font="Arial", alignment=TA_LEFT, space_after=0) -> ParagraphStyle:
    return ParagraphStyle(
        name, fontName=font, fontSize=size, leading=leading or size * 1.26,
        textColor=color, alignment=alignment, spaceAfter=space_after,
    )


S_BODY = pstyle("body", 10.2, 14.2)
S_BODY_WHITE = pstyle("body-white", 10.2, 14.2, white)
S_SMALL = pstyle("small", 8.4, 11.2, MUTED)
S_SMALL_WHITE = pstyle("small-white", 8.4, 11.2, Color(1, 1, 1, .82))
S_H2 = pstyle("h2", 24, 26, INK, "Arial-Bold")
S_H3 = pstyle("h3", 13.6, 16, INK, "Arial-Bold")
S_H3_WHITE = pstyle("h3-white", 13.6, 16, white, "Arial-Bold")
S_LABEL = pstyle("label", 8.2, 10, VIOLET, "Arial-Bold")
S_NUM = pstyle("num", 11, 13, INK, "Arial-Bold")


def masked_image(rgb_path: Path, mask_path: Path) -> ImageReader:
    rgb = PILImage.open(rgb_path).convert("RGB")
    mask = PILImage.open(mask_path).convert("L")
    rgba = rgb.convert("RGBA")
    rgba.putalpha(mask)
    return ImageReader(rgba)


CHANGE = masked_image(BRAND / "changesprint-rgb.png", BRAND / "changesprint-alpha.png")
PARTNERS = masked_image(BRAND / "partners-rgb.png", BRAND / "partners-alpha.png")
HADOX = masked_image(BRAND / "hadox-rgb.png", BRAND / "hadox-alpha.png")


def fit_image(c: canvas.Canvas, img: ImageReader, x: float, y: float,
              max_w: float, max_h: float, anchor="left") -> None:
    iw, ih = img.getSize()
    scale = min(max_w / iw, max_h / ih)
    dw, dh = iw * scale, ih * scale
    if anchor == "right":
        x -= dw
    elif anchor == "center":
        x -= dw / 2
    c.drawImage(img, x, y, dw, dh, mask="auto")


def para(c: canvas.Canvas, text: str, x: float, top: float, width: float,
         style: ParagraphStyle = S_BODY) -> float:
    p = Paragraph(text, style)
    _, ph = p.wrap(width, H)
    p.drawOn(c, x, top - ph)
    return ph


def rounded(c: canvas.Canvas, x: float, y: float, w: float, h: float,
            fill, radius=12, stroke=None) -> None:
    c.setFillColor(fill)
    c.setStrokeColor(stroke or fill)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=1 if stroke else 0)


def button(c: canvas.Canvas, label: str, url: str, x: float, y: float,
           w: float, fill=LIME, color=DEEP) -> None:
    rounded(c, x, y, w, 27, fill, 13)
    c.setFillColor(color)
    c.setFont("Arial-Bold", 8.1)
    c.drawCentredString(x + w / 2, y + 9.3, label.upper())
    c.linkURL(url, (x, y, x + w, y + 27), relative=0)


def checkbox(c: canvas.Canvas, x: float, y: float, checked=False) -> None:
    c.setStrokeColor(INK)
    c.setLineWidth(1)
    c.rect(x, y, 10, 10, fill=0, stroke=1)
    if checked:
        c.setFont("Arial-Bold", 8)
        c.drawString(x + 1.7, y + 1.3, "X")


def header(c: canvas.Canvas, label: str, page: int) -> None:
    c.setFillColor(DEEP)
    c.rect(0, H - 66, W, 66, fill=1, stroke=0)
    fit_image(c, CHANGE, 34, H - 53, 145, 42)
    c.setFillColor(VIOLET)
    c.setFont("Arial-Bold", 8.2)
    c.drawRightString(W - 34, H - 27, label.upper())
    c.setFillColor(white)
    c.setFont("Arial", 8.4)
    c.drawRightString(W - 34, H - 43, f"Guia de trabajo  |  {page:02d}")


def footer(c: canvas.Canvas, page: int, label="ChangeSprint Encuentro 2026") -> None:
    c.setFillColor(DEEP)
    c.rect(0, 0, W, 32, fill=1, stroke=0)
    fit_image(c, HADOX, 40, 5.5, 104, 22)
    c.setFillColor(white)
    c.setFont("Arial", 7.2)
    c.drawCentredString(W / 2, 12, f"{label} - Transformando lo público")
    c.setFillColor(LIME)
    c.setFont("Arial-Bold", 8)
    c.drawRightString(W - 39, 11.5, f"{page:02d}")


def content_page(c: canvas.Canvas, label: str, page: int, title: str,
                 subtitle: str | None = None) -> float:
    c.setFillColor(white)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, label, page)
    footer(c, page)
    y = H - 98
    y -= para(c, title, 39, y, W - 78, S_H2)
    if subtitle:
        y -= 8
        y -= para(c, subtitle, 39, y, W - 78, pstyle("sub", 10.2, 14, MUTED))
    return y - 18


def cover(c: canvas.Canvas, kicker: str, title: str, chips: Iterable[str],
          objective: str, includes: list[str], doc_no: str, sources=None) -> None:
    c.setFillColor(DEEP)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(LIME)
    c.rect(0, H - 13, W, 13, fill=1, stroke=0)
    fit_image(c, CHANGE, 42, H - 91, 185, 60)
    fit_image(c, HADOX, W - 42, H - 80, 125, 46, "right")
    c.setFillColor(VIOLET)
    c.setFont("Arial-Bold", 10)
    c.drawString(43, H - 127, kicker.upper())
    y = H - 158
    y -= para(c, title, 43, y, W - 86,
              pstyle("cover-title", 31.5, 33.5, white, "Arial-Bold"))
    chip_x = 43
    for i, chip in enumerate(chips):
        fill = [LIME, VIOLET, white][i % 3]
        text_color = DEEP
        cw = max(104, min(177, 16 + len(chip) * 5.3))
        rounded(c, chip_x, y - 40, cw, 27, fill, 14)
        c.setFillColor(text_color)
        c.setFont("Arial-Bold", 7.7)
        c.drawCentredString(chip_x + cw / 2, y - 30.5, chip.upper())
        chip_x += cw + 10

    panel_y = 74
    panel_h = max(285, y - 73 - panel_y)
    rounded(c, 34, panel_y, W - 68, panel_h, white, 16)
    top = panel_y + panel_h - 25
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 15)
    c.drawString(55, top, "Objetivo")
    top -= 15
    top -= para(c, objective, 55, top, W - 110, S_BODY)
    top -= 18
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 14)
    c.drawString(55, top, "Este documento incluye")
    top -= 17
    for idx, item in enumerate(includes, 1):
        rounded(c, 55, top - 32, W - 110, 28, [PALE_LIME, PALE, LILAC][(idx - 1) % 3], 8)
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 8.5)
        c.drawString(66, top - 21, f"{idx:02d}")
        para(c, item, 96, top - 10, W - 162, pstyle(f"incl-{doc_no}-{idx}", 8.7, 10.5, INK, "Arial-Bold"))
        top -= 35
    if sources:
        top -= 5
        c.setFillColor(MUTED)
        c.setFont("Arial", 6.9)
        c.drawString(55, top, "Fuentes oficiales: " + "  |  ".join(sources))
    fit_image(c, PARTNERS, W / 2, panel_y + 14, 330, 35, "center")
    c.setFillColor(MUTED)
    c.setFont("Arial", 6.8)
    c.drawCentredString(W / 2, panel_y + 6, "Instituciones participantes del bootcamp")


def numbered_card(c: canvas.Canvas, n: str, title: str, body: str, x: float,
                  top: float, w: float, h: float, fill=PALE, note: str | None = None) -> None:
    rounded(c, x, top - h, w, h, fill, 10)
    c.setFillColor(LIME if fill != PALE_LIME else VIOLET)
    c.circle(x + 24, top - 24, 13, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("Arial-Bold", 8.5)
    c.drawCentredString(x + 24, top - 27, n)
    title_h = para(c, title, x + 45, top - 13, w - 58, S_H3)
    para(c, body, x + 45, top - 18 - title_h, w - 60, S_SMALL)
    if note:
        para(c, note, x + 45, top - h + 19, w - 60, pstyle("note", 7.4, 9.4, INK, "Arial-Bold"))


def draw_manual() -> Path:
    path = OUT / "Manual_Instalacion_ChatGPT_Codex_Windows_macOS_ChangeSprint_2026.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Manual de instalación - ChatGPT y Codex para Windows y macOS")
    c.setAuthor("Hadox Research Labs - ChangeSprint Encuentro 2026")
    cover(
        c, "Preparación técnica - Sesión 02",
        "Instala ChatGPT y abre Codex en Windows o macOS",
        ["Antes del taller", "Windows + macOS", "15-25 minutos"],
        "Dejar tu equipo listo para trabajar con Codex desde la aplicación oficial de ChatGPT, abrir una carpeta local de práctica y conservar permisos seguros durante el taller.",
        ["La descarga oficial para cada sistema operativo.", "El primer inicio de sesión y la ubicación de Codex.", "Una lista de verificación y soluciones a problemas frecuentes."],
        "manual", ["learn.chatgpt.com/docs/app", "learn.chatgpt.com/docs/windows/windows-app"],
    )
    c.showPage()

    y = content_page(c, "Instalación en Windows", 2, "Windows: instala una sola aplicación.",
                     "Codex no se instala por separado: está dentro de la aplicación oficial de ChatGPT.")
    steps = [
        ("01", "Abre la página oficial", "Visita learn.chatgpt.com/docs/windows/windows-app y selecciona la descarga desde Microsoft Store."),
        ("02", "Instala desde Microsoft Store", "Pulsa Obtener o Instalar. Si tu organización bloquea la tienda, solicita apoyo antes del taller."),
        ("03", "Alternativa con Windows Terminal", "Si ya utilizas winget, ejecuta: <font name='Arial-Bold'>winget install --id 9PLM9XGG6VKS -s msstore</font>"),
        ("04", "Abre ChatGPT e inicia sesión", "Usa tu cuenta de ChatGPT. No compartas contraseñas ni abras cuentas del equipo en una sola computadora."),
        ("05", "Selecciona Codex", "En la esquina superior izquierda cambia de ChatGPT a Codex y elige New chat."),
        ("06", "Abre la carpeta del taller", "Descarga y extrae el kit. En Codex abre solamente esa carpeta, no Documentos completos ni una unidad compartida."),
    ]
    for i, (n, t, b) in enumerate(steps):
        col = i % 2
        row = i // 2
        numbered_card(c, n, t, b, 39 + col * 260, y - row * 122, 245, 105,
                      [PALE_LIME, PALE, LILAC][row])
    y2 = y - 3 * 122 - 3
    rounded(c, 39, y2 - 120, W - 78, 120, DEEP, 11)
    para(c, "Permisos recomendados para la práctica", 57, y2 - 18, W - 114, S_H3_WHITE)
    para(c, "Mantén <b>Ask for approval</b>. No actives Full access. Codex debe pedir autorización antes de salir de la carpeta, usar herramientas sensibles o ejecutar acciones que cambien el sistema.", 57, y2 - 44, W - 114, S_SMALL_WHITE)
    button(c, "Abrir guia oficial de Windows", "https://learn.chatgpt.com/docs/windows/windows-app", 57, y2 - 109, 183, GREEN)
    c.showPage()

    y = content_page(c, "Instalación en macOS", 3, "macOS: descarga desde OpenAI.",
                     "La página oficial identifica actualmente la descarga para Apple Silicon.")
    mac_steps = [
        ("01", "Confirma tu procesador", "En menú Apple > Acerca de esta Mac, comprueba si aparece Apple M1, M2, M3, M4 o posterior."),
        ("02", "Abre la descarga oficial", "Visita learn.chatgpt.com/docs/app y pulsa Download for macOS (Apple Silicon)."),
        ("03", "Instala la aplicación", "Abre el archivo descargado y mueve ChatGPT a Aplicaciones cuando macOS lo indique."),
        ("04", "Inicia sesión", "Abre ChatGPT desde Aplicaciones y entra con tu cuenta. Autoriza solamente los accesos necesarios."),
        ("05", "Entra a Codex", "Selecciona Codex en la esquina superior izquierda y crea un chat nuevo."),
        ("06", "Limita el espacio de trabajo", "Extrae el kit y abre solamente esa carpeta local. Conserva el modo que solicita aprobación."),
    ]
    for i, (n, t, b) in enumerate(mac_steps):
        col = i % 2
        row = i // 2
        numbered_card(c, n, t, b, 39 + col * 260, y - row * 122, 245, 105,
                      [PALE_LIME, PALE, LILAC][row])
    y2 = y - 3 * 122 - 3
    rounded(c, 39, y2 - 125, W - 78, 125, LILAC, 11)
    para(c, "¿Tu Mac tiene procesador Intel?", 57, y2 - 18, W - 114, S_H3)
    para(c, "No asumas compatibilidad: la descarga oficial consultada está marcada para Apple Silicon. Avísale al facilitador antes del taller y revisen juntos los requisitos vigentes. Para las actividades generales puedes usar ChatGPT web, pero el laboratorio de Codex requiere la aplicación compatible.", 57, y2 - 43, W - 114, S_SMALL)
    button(c, "Abrir descarga oficial", "https://learn.chatgpt.com/docs/app", 57, y2 - 114, 150, VIOLET)
    c.showPage()

    y = content_page(c, "Verificación antes del taller", 4, "Prueba de preparación: cinco minutos.",
                     "Hazla antes de la sesión. Si falla un punto, conserva una captura y avísale al facilitador.")
    checks = [
        "Puedo abrir la aplicación oficial de ChatGPT e iniciar sesión.",
        "Veo la opción Codex en la esquina superior izquierda.",
        "Descargué y extraje el kit de mi equipo; no estoy trabajando dentro del ZIP.",
        "Codex puede abrir la carpeta y leer LEEME.md y AGENTS.md.",
        "El modo de permisos pide aprobación y la carpeta no contiene datos reales.",
    ]
    rounded(c, 39, y - 170, W - 78, 170, PALE_LIME, 12)
    para(c, "Lista de verificación", 57, y - 17, W - 114, S_H3)
    cy = y - 47
    for item in checks:
        checkbox(c, 58, cy - 3)
        para(c, item, 77, cy + 8, W - 145, pstyle("check", 9.2, 11.5, INK))
        cy -= 24
    y -= 194
    rounded(c, 39, y - 137, W - 78, 137, DEEP, 12)
    para(c, "Reglas de seguridad para el bootcamp", 57, y - 18, W - 114, S_H3_WHITE)
    safety = [
        "Descarga solo desde OpenAI o Microsoft Store; evita sitios que ofrecen un Codex separado.",
        "Usa exclusivamente los casos ficticios entregados para el taller.",
        "No pegues expedientes, nombres, identificaciones, calificaciones ni información sensible.",
        "Lee la acción solicitada antes de aprobarla. Ante una duda, detén el agente y llama al facilitador.",
    ]
    sy = y - 49
    for item in safety:
        c.setFillColor(GREEN)
        c.circle(61, sy + 3, 3.2, fill=1, stroke=0)
        para(c, item, 73, sy + 10, W - 143, S_SMALL_WHITE)
        sy -= 22
    y -= 158
    rounded(c, 39, y - 132, W - 78, 132, PALE, 11)
    para(c, "Si algo no funciona", 57, y - 17, W - 114, S_H3)
    para(c, "1. Verifica conexión e inicio de sesión.  2. Cierra y abre la aplicación.  3. Confirma que el kit fue extraído.  4. Si no aparece Codex o la instalación está bloqueada, no instales alternativas: registra el mensaje y pide apoyo.", 57, y - 44, W - 114, S_BODY)
    button(c, "Volver a la página del curso", "https://hadox-research-labs.github.io/changesprint-encuentro-2026/", 57, y - 121, 178, LIME)
    c.save()
    return path


def draw_exercise1() -> Path:
    path = OUT / "Ejercicio_1_Guiado_Agentes_Verificables_ChangeSprint_2026.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Ejercicio 1 guiado - Agentes verificables")
    c.setAuthor("Hadox Research Labs - ChangeSprint Encuentro 2026")
    cover(
        c, "Ejercicio 01 - Práctica guiada",
        "Configura, prueba y corrige un agente verificable",
        ["Por equipo", "Con rueditas", "75 minutos"],
        "Aprender a operar Codex con una carpeta ya preparada: leer reglas persistentes, crear una skill, ejecutar cinco casos ficticios, registrar fallas y corregir la configuración.",
        ["Un kit distinto para cada uno de los tres equipos.", "Un recorrido paso a paso por AGENTS.md, skills, pruebas y resultados.", "Una demostración final de tres minutos centrada en evidencia y límites."],
        "ex1",
    )
    c.showPage()

    y = content_page(c, "Ejercicio 01 - Preparación", 2, "Antes de escribir: prepara el espacio de trabajo.",
                     "No comiencen con un prompt. Comiencen entendiendo la carpeta, las reglas y la tarea.")
    prep = [
        ("01", "Descarguen su kit", "Equipo 1: revisor de ensayos. Equipo 2: acompanante de expediente. Equipo 3: auditor de gobernanza."),
        ("02", "Extraigan el ZIP", "Trabajen dentro de la carpeta extraída. Confirmen que aparecen LEEME.md, AGENTS.md, casos, skills y resultados."),
        ("03", "Abran la carpeta en Codex", "No abran archivos sueltos. La carpeta completa es el contexto y el límite operativo del agente."),
        ("04", "Lean antes de cambiar", "Pidan a Codex que explique la misión, las prohibiciones, el formato de salida y los cinco casos."),
    ]
    for i, (n, t, b) in enumerate(prep):
        col = i % 2
        row = i // 2
        numbered_card(c, n, t, b, 39 + col * 260, y - row * 125, 245, 108,
                      PALE_LIME if row == 0 else LILAC)
    y -= 272
    para(c, "Roles sugeridos", 39, y, W - 78, S_H2)
    y -= 40
    roles = [
        ("Operador", "maneja Codex y narra cada acción"),
        ("Reglas", "vigila AGENTS.md y los límites"),
        ("Evidencia", "comprueba fuentes y citas"),
        ("Pruebas", "registra resultados y fallas"),
        ("Relatoría", "prepara la demostración final"),
    ]
    for i, (role, duty) in enumerate(roles):
        yy = y - i * 42
        c.setFillColor(DEEP)
        c.rect(39, yy - 27, 112, 27, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Arial-Bold", 8.8)
        c.drawString(49, yy - 17, role.upper())
        para(c, duty, 166, yy - 4, W - 205, pstyle(f"role-{i}", 9.1, 11, INK))
    c.showPage()

    y = content_page(c, "Ejercicio 01 - Recorrido", 3, "Seis movimientos, en este orden.",
                     "Guarden cada cambio dentro de la carpeta para que otra persona pueda reconstruir el trabajo.")
    moves = [
        ("01", "Reconocer el contrato", "Resume la misión, los datos permitidos, la decisión humana, las prohibiciones y el formato de salida."),
        ("02", "Localizar reglas persistentes", "Distingue lo que ya vive en AGENTS.md de lo que debe pedirse solamente en esta conversación."),
        ("03", "Crear la skill", "Usa $skill-creator. Define cuándo se activa, las entradas, el procedimiento, la verificación y cuándo debe detenerse."),
        ("04", "Ejecutar los cinco casos", "Procesa uno por uno. Guarda cada salida en resultados con un nombre que identifique caso y versión."),
        ("05", "Registrar y corregir", "Completa la bitácora: expectativa, resultado, riesgo y cambio. Corrige al menos una falla real."),
        ("06", "Volver a probar", "Repite el caso corregido y compara versiones. No borres la evidencia del primer intento."),
    ]
    for i, (n, t, b) in enumerate(moves):
        fill = [PALE_LIME, PALE, LILAC][i % 3]
        numbered_card(c, n, t, b, 39, y - i * 91, W - 78, 77, fill)
    c.showPage()

    y = content_page(c, "Ejercicio 01 - Pruebas y entrega", 4, "No demuestren que funciona. Descubran cómo falla.",
                     "Los cinco casos representan riesgos que un agente institucional debe hacer visibles.")
    tests = [
        ("01", "Normal", "El flujo basico produce la ficha esperada."),
        ("02", "Incompleto", "Reconoce lo que falta sin inventar datos."),
        ("03", "Inyección", "Ignora instrucciones maliciosas dentro del contenido."),
        ("04", "Variante lingüística", "No confunde forma de expresión con mérito o cumplimiento."),
        ("05", "Limítrofe", "Declara incertidumbre y escala a revisión humana."),
    ]
    for i, (n, t, b) in enumerate(tests):
        yy = y - i * 61
        rounded(c, 39, yy - 49, W - 78, 49, [PALE_LIME, PALE, LILAC][i % 3], 9)
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 10)
        c.drawString(54, yy - 28, n)
        c.drawString(88, yy - 20, t)
        para(c, b, 188, yy - 11, W - 236, S_SMALL)
    y -= 325
    rounded(c, 39, y - 158, W - 78, 158, DEEP, 12)
    para(c, "Entregables y demostración de tres minutos", 57, y - 18, W - 114, S_H3_WHITE)
    para(c, "Entreguen: 1) AGENTS.md, 2) una skill, 3) cinco salidas, 4) ficha final y 5) bitácora. En la demostración expliquen el objetivo, una regla crítica, una falla encontrada, la corrección aplicada y un límite que sigue requiriendo supervisión humana.", 57, y - 46, W - 114, S_BODY_WHITE)
    para(c, "Criterio de exito: el proceso puede explicarse, repetirse, auditarse y detenerse.", 57, y - 104, W - 114, pstyle("success", 9.2, 12, LIME, "Arial-Bold"))
    button(c, "Abrir materiales del ejercicio 1", "https://hadox-research-labs.github.io/changesprint-encuentro-2026/#ejercicio-1", 57, y - 148, 190, GREEN)
    c.save()
    return path


def draw_exercise2() -> Path:
    path = OUT / "Ejercicio_2_Del_Lienzo_Al_Agente_ChangeSprint_2026.pdf"
    c = canvas.Canvas(str(path), pagesize=A4)
    c.setTitle("Ejercicio 2 - Del lienzo al agente")
    c.setAuthor("Hadox Research Labs - ChangeSprint Encuentro 2026")
    cover(
        c, "Ejercicio 02 - Aplicación al proyecto",
        "Del lienzo propio a un agente pequeno y defendible",
        ["Por equipo", "Sin rueditas", "120 minutos"],
        "Utilizar el trabajo real de cada equipo para cuestionar el diagnostico, reconstruir el proceso, elegir una sola tarea y configurar un agente delimitado, verificable y corregible.",
        ["Una auditoría de hechos, hipótesis, decisiones y preguntas pendientes.", "Un contrato de agente antes de crear AGENTS.md o una skill.", "Pruebas propias, corrección de una falla y reflexión de madurez."],
        "ex2",
    )
    c.showPage()

    y = content_page(c, "Ejercicio 02 - Entender", 2, "Primero demuestren que entienden el proceso.",
                     "El agente es consecuencia del análisis. No utilicen la IA para ocultar preguntas que el equipo aún no ha resuelto.")
    blocks = [
        ("01", "Auditoría del lienzo", "Marquen cada afirmación como: hecho comprobado, hipótesis, decisión del equipo o pregunta pendiente. Para cada hecho anoten la fuente. Para cada hipótesis definan cómo la validarían."),
        ("02", "Mapa del proceso actual", "Reconstruyan entrada, persona que interviene, transformación, salida, decisión humana, registro y mecanismo de corrección. Señalen dónde ocurre hoy el problema."),
        ("03", "Tarea delimitada", "Elijan una persona usuaria, una sola tarea y un artefacto de salida. Escriban también lo que el agente no resolverá y la decisión que conservará una persona."),
    ]
    for i, (n, t, b) in enumerate(blocks):
        numbered_card(c, n, t, b, 39, y - i * 148, W - 78, 128,
                      [PALE_LIME, PALE, LILAC][i])
    y -= 455
    rounded(c, 39, y - 93, W - 78, 93, DEEP, 12)
    para(c, "Regla de avance", 57, y - 18, W - 114, S_H3_WHITE)
    para(c, "No creen la skill hasta poder explicar en una frase: quién necesita qué, con qué información, bajo qué reglas, qué salida recibirá y quién conserva la decisión.", 57, y - 45, W - 114, S_BODY_WHITE)
    c.showPage()

    y = content_page(c, "Ejercicio 02 - Construir y probar", 3, "Ahora conviertan el criterio en configuración.",
                     "Cada evidencia debe quedar guardada en la carpeta, fuera de la conversacion con la IA.")
    moves = [
        ("04", "Contrato del agente", "Define objetivo, entradas autorizadas, fuentes, formato de salida, acciones permitidas, prohibiciones, criterios de alto, persona revisora y registros."),
        ("05", "Prototipo en Codex", "Organiza fuentes, AGENTS.md, una skill, casos ficticios, resultados y bitácora. Pide a Codex que revise contradicciones antes de ejecutar."),
        ("06", "Pruebas propias", "Crea casos normal, incompleto, adversarial, lingüísticamente diverso y limítrofe. Registra una falla y modifica la configuración."),
        ("07", "Reflexión de madurez", "Explica qué cambiaste respecto del lienzo, qué falta validar con personas o documentos y por qué una decisión permanece humana."),
    ]
    for i, (n, t, b) in enumerate(moves):
        numbered_card(c, n, t, b, 39, y - i * 123, W - 78, 106,
                      [PALE_LIME, PALE, LILAC, MINT][i])
    y -= 505
    rounded(c, 39, y - 72, W - 78, 72, PALE, 11)
    para(c, "Entregable minimo", 57, y - 17, W - 114, S_H3)
    para(c, "Cinco plantillas completas + carpeta del prototipo + cinco pruebas + comparación antes/después de una corrección.", 57, y - 43, W - 114, S_BODY)
    c.showPage()

    y = content_page(c, "Ejercicio 02 - Equipos y tiempos", 4, "Tres puntos de partida, no tres respuestas.",
                     "Cada equipo debe validar lo que hoy solo aparece como supuesto en su lienzo.")
    teams = [
        ("EQUIPO 01", "Discrecionalidad y ensayos", "Verifiquen qué hace Gemini, qué hace el prompt, quién valora y quién autoriza. Un revisor de ensayos es posibilidad, no conclusión."),
        ("EQUIPO 02", "Brecha en la segunda fase", "Seleccionen un solo cuello de botella y un solo artefacto util. No intenten resolver comunicacion, documentos, seguimiento y acceso al mismo tiempo."),
        ("EQUIPO 03", "Gobernanza y trazabilidad", "Definan primero qué sistema, proceso, decisión, registro y responsable humano se audita. Sin caso concreto no existe auditor verificable."),
    ]
    for i, (lab, title, body) in enumerate(teams):
        yy = y - i * 103
        rounded(c, 39, yy - 88, W - 78, 88, DEEP, 10)
        c.setFillColor([LIME, VIOLET, GREEN][i])
        c.setFont("Arial-Bold", 8)
        c.drawString(55, yy - 22, lab)
        para(c, title, 55, yy - 33, W - 110, S_H3_WHITE)
        para(c, body, 55, yy - 57, W - 110, S_SMALL_WHITE)
    y -= 330
    para(c, "Ruta de 120 minutos", 39, y, W - 78, S_H2)
    y -= 35
    timeline = [
        ("00-20", "Auditar lienzo"), ("20-40", "Mapear proceso"),
        ("40-60", "Contratar agente"), ("60-90", "Configurar prototipo"),
        ("90-110", "Probar y corregir"), ("110-120", "Defender evidencia"),
    ]
    for i, (time, task) in enumerate(timeline):
        col = i % 2
        row = i // 2
        x = 39 + col * 260
        yy = y - row * 44
        c.setFillColor([PALE_LIME, LILAC][col])
        c.rect(x, yy - 30, 245, 30, fill=1, stroke=0)
        c.setFillColor(INK)
        c.setFont("Arial-Bold", 8.3)
        c.drawString(x + 10, yy - 19, time)
        c.setFont("Arial", 8.3)
        c.drawString(x + 58, yy - 19, task)
    y -= 145
    rounded(c, 39, y - 75, W - 78, 75, PALE_LIME, 11)
    para(c, "Criterio de aprobacion", 57, y - 15, W - 114, S_H3)
    para(c, "Pueden demostrar qué sabe el agente, qué todavía supone, qué delegaron, qué prohibieron, cómo lo probaron y quién conserva la decisión.", 57, y - 40, 285, pstyle("approval", 8.6, 10.5, INK, "Arial-Bold"))
    button(c, "Abrir ejercicio y materiales", "https://hadox-research-labs.github.io/changesprint-encuentro-2026/ejercicio-2-proyecto-propio/", W - 57 - 172, y - 57, 172, LIME)
    c.save()
    return path


if __name__ == "__main__":
    for generated in (draw_manual(), draw_exercise1(), draw_exercise2()):
        print(generated)
