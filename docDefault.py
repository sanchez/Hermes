from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from support import Bookmark

class Handler:
    def __init__(self, destName):
        self.c = SimpleDocTemplate(destName, bottomup=0)
        # self.c.setAuthor("Hermes (Daniel Fitz)")
        # self.c.setTitle(destName)
        # self.c.setFont('Helvetica', 12)
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

    def save(self):
        self.c.build(self.content, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        # self.c.save()

    def add_header_footer(self, canvas, doc):
        canvas.setAuthor("Hermes (Daniel Fitz")
        canvas.setTitle(self.destName)
        canvas.setFont('Helvetica', 12)

    def add_heading(self, title, depth, options):
        self.content.append(Bookmark(title, depth))
        if depth == 1:
            self.content.append(Paragraph(title, self.styles["Heading 1"]))

    def add_plain_text(self, text):
        self.content.append(Paragraph("Text: %s" % text, self.styles["Normal"]))