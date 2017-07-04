from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from support import Bookmark

class Handler:
    def __init__(self, destName):
        self.c = SimpleDocTemplate(destName, bottomup=0)
        self.destName = destName

        self.content = []
        self.styles = getSampleStyleSheet()
        self.primaryColor = "#0B75CB"
        self.styles.add(ParagraphStyle(
            "Heading 1",
            parent=self.styles["Normal"],
            textColor=self.primaryColor,
            endDots="_",
            fontSize=20,
            spaceAfter=12,
            fontName="Helvetica-Bold"
        ))
        self.styles.add(ParagraphStyle(
            "Heading 2",
            parent=self.styles["Heading 1"],
            endDots=None,
            fontSize=16
        ))

    def save(self):
        self.c.build(self.content, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)

    def add_header_footer(self, canvas, doc):
        canvas.setAuthor("Hermes (Daniel Fitz")
        canvas.setTitle(self.destName)
        canvas.setFont('Helvetica', 12)

    def add_heading(self, title, depth, options):
        if depth == 1:
            self.content.append(Paragraph(title, self.styles["Heading 1"]))
        elif depth == 2:
            self.content.append(Paragraph(title, self.styles["Heading 2"]))
        self.content.append(Bookmark(title, depth))
        

    def add_plain_text(self, text):
        self.content.append(Paragraph(text, self.styles["Normal"]))