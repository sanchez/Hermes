from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class Handler:
    def __init__(self, destName):
        self.c = SimpleDocTemplate(destName, bottomup=0)
        # self.c.setAuthor("Hermes (Daniel Fitz)")
        # self.c.setTitle(destName)
        # self.c.setFont('Helvetica', 12)
        self.destName = destName

        self.content = []
        self.styles = getSampleStyleSheet()

    def save(self):
        self.c.build(self.content, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)
        # self.c.save()

    def add_header_footer(self, canvas, doc):
        canvas.setAuthor("Hermes (Daniel Fitz")
        canvas.setTitle(self.destName)
        canvas.setFont('Helvetica', 12)

    def add_heading(self, title, depth, options):
        self.content.append(Paragraph("Heading: %s" % title, self.styles["Normal"]))

    def add_plain_text(self, text):
        self.content.append(Paragraph("Text: %s" % text, self.styles["Normal"]))