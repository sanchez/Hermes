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
            fontName="Helvetica-Bold",
            spaceBefore=18
        ))
        self.styles.add(ParagraphStyle(
            "Heading 2",
            parent=self.styles["Heading 1"],
            endDots=None,
            fontSize=16,
            spaceAfter=8,
            spaceBefore=0
        ))
        self.styles.add(ParagraphStyle(
            "Heading 3",
            parent=self.styles["Heading 2"],
            endDots=None,
            fontSize=12,
            textColor="#000",
            spaceAfter=4
        ))

    def save(self):
        self.c.build(self.content, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)

    def add_header_footer(self, canv, doc):
        canv.setAuthor("Hermes (Daniel Fitz")
        canv.setTitle(self.destName)
        canv.setFont('Helvetica', 12)

    def add_heading(self, title, depth, options):
        if depth == 1:
            self.content.append(Paragraph(title, self.styles["Heading 1"]))
        elif depth == 2:
            self.content.append(Paragraph(title, self.styles["Heading 2"]))
        elif depth == 3:
            newTitle = "<font color=%s>%s</font><font color=black>%s</font>" % (self.primaryColor, title[:1], title[1:])
            print(newTitle)
            self.content.append(Paragraph(newTitle, self.styles["Heading 3"]))
        self.content.append(Bookmark(title, depth))
        

    def add_plain_text(self, text):
        self.content.append(Paragraph(text, self.styles["Normal"]))