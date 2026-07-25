from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from .parser import ElementNode, TextNode
import html

class PDFMLCompiler:
    def __init__(self, output_path):
        self.output_path = output_path
        self.doc = SimpleDocTemplate(output_path, pagesize=A4,
                                     rightMargin=50, leftMargin=50,
                                     topMargin=50, bottomMargin=50)
        self.styles = getSampleStyleSheet()
        self.flowables = []

    def get_alignment(self, align_str):
        mapping = {"center": TA_CENTER, "right": TA_RIGHT, "justify": TA_JUSTIFY}
        return mapping.get(align_str.lower(), TA_LEFT)

    def parse_color(self, hex_or_name):
        try:
            if hex_or_name.startswith('#'):
                return colors.HexColor(hex_or_name)
            return getattr(colors, hex_or_name.lower())
        except:
            return colors.black

    def compile_inline(self, nodes):
        """Merangkai node menjadi string XML inline yang di-support Paragraph ReportLab."""
        result = ""
        for node in nodes:
            if isinstance(node, TextNode):
                # Escape HTML safety < > &
                result += html.escape(node.text.replace('\n', ' '))
            elif isinstance(node, ElementNode):
                inner = self.compile_inline(node.children)
                if node.tag == "b": result += f"<b>{inner}</b>"
                elif node.tag == "i": result += f"<i>{inner}</i>"
                elif node.tag == "u": result += f"<u>{inner}</u>"
                elif node.tag == "color":
                    c = node.attrs.get("val", "#000000")
                    result += f'<font color="{c}">{inner}</font>'
                else:
                    result += inner # Tag tak dikenal di dalam paragraf jadi teks biasa
        return result

    def build_flowable(self, node):
        """Mengonversi AST Node (Block-level) ke objek ReportLab Flowable."""
        if isinstance(node, TextNode):
            # Teks telanjang di-wrap sebagai Paragraph biasa
            return Paragraph(self.compile_inline([node]), self.styles["Normal"])

        tag = node.tag
        attrs = node.attrs

        # 1. PARAGRAF (head, sub, body)
        if tag in ["head", "sub", "body"]:
            inline_html = self.compile_inline(node.children)
            base_style = "Heading1" if tag == "head" else "Heading3" if tag == "sub" else "Normal"
            
            style = ParagraphStyle(
                name=f"Custom_{id(node)}",
                parent=self.styles[base_style],
                alignment=self.get_alignment(attrs.get("align", "left")),
                textColor=self.parse_color(attrs.get("color", "black"))
            )
            return Paragraph(inline_html, style)

        # 2. IMAGE
        elif tag == "image":
            src = attrs.get("src")
            w = float(attrs.get("width", 200))
            h = float(attrs.get("height", 150))
            if Path(src).exists():
                return Image(src, width=w, height=h)
            else:
                print(f"[Warning] Gambar tidak ditemukan: {src}")
                return Spacer(w, h)

        # 3. SPACING & PAGEBREAK
        elif tag == "space":
            h = float(attrs.get("height", 20))
            return Spacer(1, h)
        elif tag == "page":
            return PageBreak()

        # 4. TABLE
        elif tag == "table":
            table_data = []
            for child in node.children:
                if isinstance(child, ElementNode) and child.tag == "row":
                    row_data = []
                    for cell in child.children:
                        if isinstance(cell, ElementNode) and cell.tag == "cell":
                            # Sel mendukung inline styling melalui Paragraph
                            cell_content = self.compile_inline(cell.children)
                            row_data.append(Paragraph(cell_content, self.styles["Normal"]))
                    if row_data:
                        table_data.append(row_data)

            if table_data:
                t = Table(table_data)
                border = int(attrs.get("border", 0))
                t_style = [('VALIGN', (0,0), (-1,-1), 'TOP')]
                
                if border > 0:
                    t_style.extend([
                        ('GRID', (0,0), (-1,-1), border, colors.black),
                        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey) # Header style otomatis
                    ])
                t.setStyle(TableStyle(t_style))
                return t
            return None
            
        else:
            # Fallback
            return Paragraph(self.compile_inline([node]), self.styles["Normal"])

    def compile(self, ast_nodes):
        for node in ast_nodes:
            flowable = self.build_flowable(node)
            if flowable:
                self.flowables.append(flowable)
        
        self.doc.build(self.flowables)
        print(f"\n[✓] SUKSES! PDF berhasil dirender di: {self.output_path}")
