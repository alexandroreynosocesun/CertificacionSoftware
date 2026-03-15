from fpdf import FPDF
import re

class PDF(FPDF):
    def __init__(self, titulo_doc):
        super().__init__()
        self.titulo_doc = titulo_doc
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        self.set_fill_color(10, 10, 10)
        self.rect(0, 0, 210, 14, 'F')
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(255, 255, 255)
        self.set_xy(10, 3)
        self.cell(0, 8, self.titulo_doc, align="L")
        self.set_text_color(0, 0, 0)
        self.ln(10)

    def footer(self):
        self.set_y(-13)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Página {self.page_no()} | Desarrollador: Alexandro Reynoso | Marzo 2026", align="C")
        self.set_text_color(0, 0, 0)


def limpiar(texto):
    # Quitar caracteres problemáticos para latin-1
    reemplazos = {
        '\u2014': '-', '\u2013': '-', '\u2019': "'", '\u2018': "'",
        '\u201c': '"', '\u201d': '"', '\u2022': '-', '\u00e9': 'e',
        '\u00f3': 'o', '\u00fa': 'u', '\u00ed': 'i', '\u00e1': 'a',
        '\u00f1': 'n', '\u00e3': 'a', '\u00fc': 'u', '\u00f6': 'o',
        '\u00e4': 'a', '\u00e2': 'a', '\u00ea': 'e', '\u00ee': 'i',
        '\u00f4': 'o', '\u00fb': 'u', '\u00e0': 'a', '\u00e8': 'e',
        '\u00ec': 'i', '\u00f2': 'o', '\u00f9': 'u', '\u00c9': 'E',
        '\u00d3': 'O', '\u00da': 'U', '\u00cd': 'I', '\u00c1': 'A',
        '\u00d1': 'N', '\u2190': '<-', '\u2192': '->', '\u25ba': '>',
        '\u2588': '#', '\u2502': '|', '\u251c': '+', '\u2500': '-',
        '\u2518': '+', '\u250c': '+', '\u2510': '+', '\u2514': '+',
        '\u253c': '+', '\u2524': '+', '\u252c': '+', '\u2534': '+',
        '\u2550': '=', '\u2551': '|', '\u256c': '+', '\u2560': '+',
        '\u2563': '+', '\u2566': '+', '\u2569': '+', '\u2557': '+',
        '\u255d': '+', '\u2554': '+', '\u255a': '+',
        '\u00ab': '<<', '\u00bb': '>>',
        '\u25b2': '^', '\u25bc': 'v',
        '\u2640': '', '\u2642': '',
        '\u00b7': '.', '\u2026': '...',
        '\u00b0': ' grados', '\u00b1': '+/-',
        '\ufffd': '?',
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    resultado = ''
    for c in texto:
        try:
            c.encode('latin-1')
            resultado += c
        except UnicodeEncodeError:
            resultado += '?'
    return resultado


def generar_pdf(md_file, pdf_file, titulo):
    pdf = PDF(titulo)
    pdf.add_page()

    with open(md_file, encoding="utf-8") as f:
        lineas = f.readlines()

    in_code = False
    code_buffer = []

    for linea in lineas:
        linea_raw = linea.rstrip('\n')
        linea_txt = limpiar(linea_raw)

        # Bloque de código
        if linea_txt.strip().startswith('```'):
            if not in_code:
                in_code = True
                code_buffer = []
            else:
                in_code = False
                # Dibujar bloque de código
                pdf.set_fill_color(244, 244, 244)
                pdf.set_draw_color(41, 121, 255)
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_font("Courier", "", 7.5)
                linea_h = 4.2
                alto = len(code_buffer) * linea_h + 6
                pdf.rect(10, y, 190, alto, 'FD')
                pdf.set_xy(13, y + 3)
                for cl in code_buffer:
                    pdf.set_x(13)
                    pdf.cell(184, linea_h, cl[:120], ln=True)
                pdf.ln(2)
                pdf.set_draw_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 255)
            continue

        if in_code:
            code_buffer.append(linea_txt)
            continue

        # Separador ---
        if re.match(r'^-{3,}$', linea_txt.strip()):
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(3)
            continue

        # H1
        if linea_txt.startswith('# ') and not linea_txt.startswith('## '):
            texto = linea_txt[2:].strip()
            pdf.set_font("Helvetica", "B", 18)
            pdf.set_text_color(10, 10, 10)
            pdf.ln(4)
            pdf.multi_cell(0, 10, texto)
            pdf.set_draw_color(41, 121, 255)
            pdf.set_line_width(0.8)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_line_width(0.2)
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(4)
            continue

        # H2
        if linea_txt.startswith('## ') and not linea_txt.startswith('### '):
            texto = linea_txt[3:].strip()
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(20, 20, 20)
            pdf.multi_cell(0, 8, texto)
            pdf.set_draw_color(180, 180, 180)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.set_draw_color(0, 0, 0)
            pdf.ln(3)
            continue

        # H3
        if linea_txt.startswith('### ') and not linea_txt.startswith('#### '):
            texto = linea_txt[4:].strip()
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 7, texto)
            pdf.ln(1)
            continue

        # H4
        if linea_txt.startswith('#### '):
            texto = linea_txt[5:].strip()
            pdf.ln(2)
            pdf.set_font("Helvetica", "BI", 10)
            pdf.set_text_color(60, 60, 60)
            pdf.multi_cell(0, 6, texto)
            pdf.ln(1)
            continue

        # Tabla markdown
        if '|' in linea_txt and linea_txt.strip().startswith('|'):
            celdas = [c.strip() for c in linea_txt.strip().strip('|').split('|')]
            if all(re.match(r'^[-:]+$', c) for c in celdas if c):
                continue  # línea separadora de tabla
            es_header = False
            # Detectar si es encabezado mirando si la siguiente línea es separador
            pdf.set_font("Helvetica", "", 8.5)
            n = len(celdas)
            if n == 0:
                continue
            ancho = 185 / n
            # Checar si parece encabezado (bold)
            es_bold = any(c.isupper() or c in ['Requerimiento','Estado','Campo','Tipo',
                          'Restriccion','Descripcion','Componente','Minimo','Version',
                          'Prueba','Resultado'] for c in celdas)
            if es_bold:
                pdf.set_fill_color(41, 121, 255)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Helvetica", "B", 8.5)
                for celda in celdas:
                    pdf.cell(ancho, 7, celda[:40], border=0, fill=True)
                pdf.ln()
                pdf.set_text_color(0, 0, 0)
                pdf.set_fill_color(255, 255, 255)
            else:
                pdf.set_fill_color(249, 249, 249)
                pdf.set_text_color(30, 30, 30)
                pdf.set_font("Helvetica", "", 8.5)
                for celda in celdas:
                    pdf.cell(ancho, 6.5, celda[:50], border="B", fill=True)
                pdf.ln()
                pdf.set_fill_color(255, 255, 255)
            continue

        # Lista
        if re.match(r'^\s*[-*]\s+', linea_txt):
            texto = re.sub(r'^\s*[-*]\s+', '', linea_txt)
            texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
            texto = re.sub(r'`(.+?)`', r'\1', texto)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(14)
            pdf.cell(4, 6, chr(149))
            pdf.multi_cell(172, 6, texto)
            continue

        # Lista numerada
        if re.match(r'^\s*\d+\.\s+', linea_txt):
            texto = re.sub(r'^\s*\d+\.\s+', '', linea_txt)
            num = re.match(r'^\s*(\d+)\.', linea_txt).group(1)
            texto = re.sub(r'\*\*(.+?)\*\*', r'\1', texto)
            texto = re.sub(r'`(.+?)`', r'\1', texto)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(14)
            pdf.cell(5, 6, f"{num}.")
            pdf.multi_cell(171, 6, texto)
            continue

        # Línea vacía
        if linea_txt.strip() == '':
            pdf.ln(2)
            continue

        # Párrafo normal con bold e inline code
        partes = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', linea_txt)
        pdf.set_x(10)
        inicio_linea = True
        for parte in partes:
            if parte.startswith('**') and parte.endswith('**'):
                texto = parte[2:-2]
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(10, 10, 10)
            elif parte.startswith('`') and parte.endswith('`'):
                texto = parte[1:-1]
                pdf.set_font("Courier", "", 9)
                pdf.set_text_color(192, 57, 43)
            else:
                texto = parte
                pdf.set_font("Helvetica", "", 10)
                pdf.set_text_color(30, 30, 30)
            if texto:
                if inicio_linea:
                    pdf.multi_cell(0, 6, texto)
                    inicio_linea = False
                else:
                    pdf.set_x(10)
                    pdf.multi_cell(0, 6, texto)
        pdf.set_text_color(0, 0, 0)

    pdf.output(pdf_file)
    print(f"Generado: {pdf_file}")


generar_pdf(
    "MANUAL_DE_USUARIO_GALAPRO.md",
    "MANUAL_DE_USUARIO_GALAPRO.pdf",
    "GalaPro - Manual de Usuario"
)

generar_pdf(
    "MANUAL_TECNICO_GALAPRO.md",
    "MANUAL_TECNICO_GALAPRO.pdf",
    "GalaPro - Manual Tecnico"
)

print("Listo.")
