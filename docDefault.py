from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, XPreformatted, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from support import Bookmark, BlockQuote, CodeBlock

class Handler:
    def __init__(self, destName):
        self.c = SimpleDocTemplate(destName, bottomup=0, pagesize=A4,
            topMargin=40, bottomMargin=40, leftMargin=40, rightMargin=40)
        self.destName = destName

        self.content = []
        self.styles = getSampleStyleSheet()
        self.primaryColor = "#0B75CB"
        self.tableCount = 1
        self.figureCount = 1
        self.config = {}

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
            leftIndent=30,
            fontName="Courier-Bold"
        ))

    def set_config(self, config):
        self.config = config

    def save(self):
        self.c.build(self.content, onFirstPage=self.add_header_footer, onLaterPages=self.add_header_footer)

    def add_header_footer(self, canv, doc):
        if self.config["author"]:
            canv.setAuthor(self.config["author"])
        else:
            canv.setAuthor("Hermes")
        if self.config["title"]:
            canv.setTitle(self.config["title"])
        canv.setFont('Helvetica', 12)

        canv.setStrokeColor(colors.grey)
        canv.setFillColor(colors.grey)
        pageNum = canv.getPageNumber()
        canv.drawString(A4[0] - 100, 27, "Page %d" % pageNum)
        canv.drawString(50, 27, self.config["title"])
        canv.drawCentredString(A4[0]/2, 27, self.config["author"])

        canv.line(40, 40, A4[0] - 40, 40)
        canv.line(40, A4[1] - 40, A4[0] - 40, A4[1] - 40)
        
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
                p = Paragraph(column, self.styles["Normal"])
                newRow.append(p)
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
        self.content.append(CodeBlock(text, self.styles["Code Block"]))

    def add_newline(self):
        self.content.append(PageBreak())

    def add_image(self, location, caption):
        self.content.append(Image(location))
        if caption:
            self.content.append(Paragraph(
                "Figure %d: %s" % (self.figureCount, caption), self.styles["Caption"]))

    def add_plain_text(self, text):
        if text == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(text, self.styles["Normal"]))