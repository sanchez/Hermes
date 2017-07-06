from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, XPreformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from support import Bookmark, BlockQuote

class Handler:
    def __init__(self, destName):
        self.c = SimpleDocTemplate(destName, bottomup=0, pagesize=A4,
            topMargin=30, bottomMargin=30, leftMargin=40, rightMargin=40)
        self.destName = destName

        self.content = []
        self.styles = getSampleStyleSheet()
        self.primaryColor = "#0B75CB"
        self.tableCount = 1

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
        self.styles.add(ParagraphStyle(
            "Table Heading",
            parent=self.styles["Heading 2"],
            fontSize=12
        ))
        self.styles.add(ParagraphStyle(
            "Caption",
            parent=self.styles["Normal"],
            alignment=TA_CENTER,
            fontName="Helvetica-Oblique"
        ))
        self.styles.add(ParagraphStyle(
            "Block",
            parent=self.styles["Normal"],
            textColor=colors.grey,
            leftIndent=10
        ))
        self.styles.add(ParagraphStyle(
            "Code Block",
            parent=self.styles["Normal"],
            backColor=colors.lightgrey,
            leftIndent=10,
            borderPadding=4,
            fontName="Courier-Bold"
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

    def add_code_inline(self, matchobj):
        return "<font name='courier' bgcolor='lightgrey'><b>%s</b></font>" % matchobj.group(1)

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
        
    def add_table(self, headerRow, tableData, caption):
        data = []
        style = [
            # ('GRID', (0,0), (-1,-1), 1, colors.grey),
            ('VALIGN', (0,0), (-1,-1), 'TOP')
        ]
        if headerRow != None:
            data.append([])
            for header in headerRow:
                data[0].append(Paragraph(header, self.styles["Table Heading"]))
        rowCount = 0
        for row in tableData:
            newRow = []
            for column in row:
                newRow.append(Paragraph(column, self.styles["Normal"]))
            data.append(newRow)
            rowCount += 1
            if (rowCount % 2):
                style.append(
                    ('BACKGROUND', (0,rowCount), (-1,rowCount), colors.lightgrey)
                )
        t = Table(data, style=style)
        self.content.append(t)
        if caption:
            self.content.append(Spacer(0, 6))
            self.content.append(Paragraph(
                    "Figure %d: %s" % (self.tableCount, caption), 
                self.styles["Caption"]))
    
    def add_blockquote(self, text):
        self.content.append(BlockQuote(text, self.styles["Block"]))

    def add_checklist(self, checked, text, depth):
        uncheckChar = u"\u274F\u2001"
        checkedChar = u"\u2713\u2001"
        totalText = ""
        if checked:
            totalText = checkedChar + text
        else:
            totalText = uncheckChar + text
        indent = depth * 10 + 5
        self.content.append(Paragraph(totalText, ParagraphStyle(
            "Checklist",
            parent=self.styles["Bullet"],
            leftIndent=indent
        )))

    def add_code(self, codeCache):
        text = "\n".join(codeCache)
        self.content.append(XPreformatted(text, self.styles["Code Block"]))

    def add_plain_text(self, text):
        if text == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(text, self.styles["Normal"]))