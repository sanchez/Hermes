from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, XPreformatted, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib.pagesizes import A4
from support import Bookmark, BlockQuote, CodeBlock, ResetPageNum, Note

class ListOfFigures(TableOfContents):
    def notify(self, kind, stuff):
        if kind == 'TOCFigure':
            self.addEntry(*stuff)

class ListOfTables(TableOfContents):
    def notify(self, kind, stuff):
        if kind == 'TOCTable':
            self.addEntry(*stuff)

class MyDocTemplate(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if flowable.__class__.__name__ == "Paragraph":
            text = flowable.getPlainText()
            style = flowable.style.name
            if style == "Heading 1":
                self.notify("TOCEntry", (0, text, self.page, "B1%s" % text))
            elif style == "Heading 2":
                self.notify("TOCEntry", (1, text, self.page, "B2%s" % text))
            elif style == "Heading 3":
                self.notify("TOCEntry", (2, text, self.page, "B3%s" % text))
            elif style == "TCaption":
                self.notify("TOCTable", (0, text, self.page))
            elif style == "FCaption":
                self.notify("TOCFigure", (0, text, self.page))
        elif flowable.__class__.__name__ == "ResetPageNum":
            self.canv._pageNumber = 0

class Handler:
    def __init__(self, destName):
        self.c = MyDocTemplate(destName, bottomup=0, pagesize=A4,
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
            spaceBefore=0
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
            "Heading",
            parent=self.styles["Heading 1"]
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
            "TCaption",
            parent=self.styles["Caption"]
        ))
        self.styles.add(ParagraphStyle(
            "FCaption",
            parent=self.styles["Caption"]
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
        self.c.multiBuild(self.content, onFirstPage=self.add_title, onLaterPages=self.add_header_footer)

    def add_header_footer(self, canv, doc):
        canv.setStrokeColor(colors.grey)
        canv.setFillColor(colors.grey)
        pageNum = canv.getPageNumber() - 1
        canv.drawString(A4[0] - 100, 27, "Page %d" % pageNum)
        canv.drawString(50, 27, self.config["title"])
        canv.drawCentredString(A4[0]/2, 27, self.config["author"])

        canv.line(40, 40, A4[0] - 40, 40)
        canv.line(40, A4[1] - 40, A4[0] - 40, A4[1] - 40)

    def add_title(self, canv, doc):
        if "author" in self.config:
            canv.setAuthor(self.config["author"])
        else:
            canv.setAuthor("Hermes")
        if "title" in self.config:
            canv.setTitle(self.config["title"])

        #print(self.config)
        name = self.config["author"].split(" ", 1)
        titleStyle = self.styles["Normal"]
        titleStyle.alignment = TA_CENTER
        titleStyle.fontSize = 24
        name = Paragraph(
            "%s<font color='%s'> <b>%s</b></font>" % (name[0], self.primaryColor, name[1]), 
            titleStyle)
        nameWidth, nameHeight = name.wrap(A4[0], 0)
        name.drawOn(canv, 0, A4[1] - 100)

        if "alt-name" in self.config:
            titleStyle.fontSize = 20
            titleStyle.alignment = TA_RIGHT
            altName = Paragraph("(<font color='%s'>%s</font>)" % 
                (self.primaryColor, self.config["alt-name"]), titleStyle)
            altName.wrapOn(canv, 450, 0)
            altName.drawOn(canv, 0, A4[1] - 124)

        if "logo" in self.config:
            canv.drawImage(self.config["logo"], (3*A4[0] / 8), A4[1] / 2 - 200, width=(A4[0]/4), preserveAspectRatio=True, mask="auto", anchor="c")

        if "school" in self.config:
            titleStyle.fontSize = 20
            titleStyle.alignment = TA_CENTER
            school = Paragraph(self.config["school"], titleStyle)
            school.wrapOn(canv, A4[0], 0)
            school.drawOn(canv, 0, 380)
        
        if "title" in self.config:
            titleStyle.fontSize = 18
            titleStyle.alignment = TA_CENTER
            title = Paragraph(self.config["title"], titleStyle)
            title.wrapOn(canv, A4[0], 0)
            title.drawOn(canv, 0, 200)

        if "subject" in self.config:
            titleStyle.fontSize = 14
            titleStyle.alignment = TA_CENTER
            subject = Paragraph(self.config["subject"], titleStyle)
            subject.wrapOn(canv, A4[0], 0)
            subject.drawOn(canv, 0, 350)
        
        titleStyle.alignment = TA_LEFT

        canv.setStrokeColor(self.primaryColor)
        canv.setLineWidth(5)
        canv.circle(A4[0], 500, 50)
        canv.circle(A4[0] - 20, 600, 60)
        canv.circle(A4[0] + 60, 600, 100)
        canv.circle(A4[0] - 40, 700, 30)
        canv.circle(A4[0], 710, 30)
        canv.circle(A4[0], 500, 100)
        canv.circle(A4[0] - 80, 800, 10)
        canv.circle(A4[0] - 60, 778, 20)
        canv.circle(A4[0] - 6, 750, 40)
        canv.circle(A4[0] - 50, 740, 20)
        canv.circle(A4[0] + 10, 420, 80)
        canv.circle(A4[0], 300, 60)

        canv.setFont("Helvetica", 12)
        canv.showPage()

    def add_color_inline(self, matchobj):
        color = matchobj.group(1)
        text = matchobj.group(2)
        if color == "primary" or color == "":
            color = self.primaryColor
        return "<font color='%s'>%s</font>" % (color, text)
        
    def add_double_dash(self, matchobj):
        return u"%s\u2013%s" % (matchobj.group(1), matchobj.group(3))

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
        if self.tableOfContents:
            self.tableOfContents.addEntry(depth, title, 1)
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
                    "Table %d: %s" % (self.tableCount, caption), 
                self.styles["TCaption"]))
    
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
                "Figure %d: %s" % (self.figureCount, caption), self.styles["FCaption"]))

    def add_toc(self):
        self.tableOfContents = TableOfContents()
        self.content.append(Paragraph("Table of Contents", self.styles["Heading"]))
        self.content.append(self.tableOfContents)
        self.tableOfContents.dotsMinLevel = 5
        style = [
            ParagraphStyle(name="TOCH1", textColor=self.primaryColor, fontName="Helvetica-Bold"),
            ParagraphStyle(name="TOCH2", fontName="Helvetica-Bold", leftIndent=12, endDots=""),
            ParagraphStyle(name="TOCH3", fontName="Helvetica-Bold", leftIndent=24)
        ]
        self.tableOfContents.levelStyles = style
        tocTable = ListOfTables()
        tocTable.levelStyles = style
        self.content.append(Paragraph("List of Tables", self.styles["Heading"]))
        self.content.append(tocTable)
        tocFig = ListOfFigures()
        tocFig.levelStyles = style
        self.content.append(Paragraph("List of Figures", self.styles["Heading"]))
        self.content.append(tocFig)

    def add_note(self, header, body):
        headerP = Paragraph(header, self.styles["Heading"])
        bodyP = Paragraph("<br />".join(body), self.styles["Normal"])
        self.content.append(Note(headerP, bodyP, self.primaryColor))

    def add_plain_text(self, text):
        if text == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(text, self.styles["Normal"]))