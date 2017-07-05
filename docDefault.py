from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
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
        
    def add_bold(self, matchobj):
        return "<b>%s</b>" % matchobj.group(1)

    def add_italics(self, matchobj):
        return "<i>%s</i>" % matchobj.group(1)

    def add_heading(self, title, depth, options):
        if depth == 1:
            self.content.append(Paragraph(title, self.styles["Heading 1"]))
        elif depth == 2:
            self.content.append(Paragraph(title, self.styles["Heading 2"]))
        elif depth == 3:
            newTitle = "<font color=%s>%s</font><font color=black>%s</font>" % (self.primaryColor, title[:1], title[1:])
            self.content.append(Paragraph(newTitle, self.styles["Heading 3"]))
        self.content.append(Bookmark(title, depth))
        
    def add_bullet(self, bullets):
        bulletChar = u"\u2022"
        for text, depth in bullets:
            contentLine = "%s %s" % (bulletChar, text)
            bulletIndent = depth * 10 + 5
            self.content.append(Paragraph(contentLine, ParagraphStyle(
                "newBullet",
                parent=self.styles["Bullet"],
                leftIndent=bulletIndent
            )))

    def add_list(self, lists):
        for text, depth, num in lists:
            contentLine = "%s) %s" % (num, text)
            listIndent = depth * 10 + 5
            self.content.append(Paragraph(contentLine, ParagraphStyle(
                "newList",
                parent=self.styles["Bullet"],
                leftIndent=listIndent
            )))
        
    def add_table(self, headerRow, tableData):
        data = []
        if headerRow != None:
            data.append([])
            for header in headerRow:
                data[0].append(Paragraph(header, self.styles["Normal"]))
        for row in tableData:
            newRow = []
            for column in row:
                newRow.append(Paragraph(column, self.styles["Normal"]))
            data.append(newRow)
        t = Table(data, style=[
            ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ])
        self.content.append(t)

    def add_plain_text(self, text):
        if text == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(text, self.styles["Normal"]))