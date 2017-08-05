import parser
import re
import support
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

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

class docDefault():
    def __init__(self, config):
        print("Loading Default Template")

        parser.set_lookup(self.reHeader, "header")
        parser.set_lookup(self.reCommand, "command")

        self.content = []
        self.styles = getSampleStyleSheet()
        self.primaryColor = "#0B75CB"
        self.config = config

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
    
    def get_content(self):
        return self.content

    def title(self, canv, doc):
        if "author" in self.config:
            canv.setAuthor(self.config["author"])
        else:
            canv.setAuthor("Hermes")
        if "title" in self.config:
            canv.setTitle(self.config["title"])
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

    def header_footer(self, canv, doc):
        canv.setStrokeColor(colors.grey)
        canv.setFillColor(colors.grey)
        pageNum = canv.getPageNumber() - 1
        canv.drawString(A4[0] - 100, 27, "Page %d" % pageNum)
        canv.drawString(50, 27, self.config["title"])
        canv.drawCentredString(A4[0]/2, 27, self.config["author"])
        canv.line(40, 40, A4[0] - 40, 40)
        canv.line(40, A4[1] - 40, A4[0] - 40, A4[1] - 40)

    def bold(self, matchobj):
        return "<b>%s</b>" % matchobj.group(1)

    def italics(self, matchobj):
        return "<i>%s</i>" % matchobj.group(1)

    reHeader = re.compile(r"^(#{1,6})(?:\{(.+)\})? (.+)$")
    def header(self, lineArray):
        result = re.search(self.reHeader, lineArray.get())
        depth = len(result.group(1))
        content = result.group(3)
        key = result.group(2)
        if key == None:
            key = content
        if depth == 1:
            self.content.append(Paragraph(content, self.styles["Heading 1"]))
        elif depth == 2:
            self.content.append(Paragraph(content, self.styles["Heading 2"]))
        elif depth == 3:
            newTitle = "<font color=%s>%s</font><font color='black'>%s</font>" % (self.primaryColor, title[:1], title[1:])
            self.content.append(Paragraph(newTitle, self.styles["Heading 3"]))
        self.content.append(support.Bookmark(content, depth))

    reCommand = re.compile(r"^\\(.+)$")
    def command(self, lineArray):
        command = re.search(self.reCommand, lineArray.get()).group(1)
        if command == "toc":
            self.content.append(Paragraph("Table of Contents", self.styles["Heading"]))
            self.content.append(TableOfContents())
            self.content[-1].dotsMinLevel = 5
            self.content[-1].levelStyles = [
                ParagraphStyle(name="TOCH1", textColor=self.primaryColor, fontName="Helvetica-Bold"),
                ParagraphStyle(name="TOCH2", fontName="Helvetica-Bold", leftIndent=12, endDots=""),
                ParagraphStyle(name="TOCH3", fontName="Helvetica-Bold", leftIndent=24)
            ]
        elif command == "\\":
            self.content.append(PageBreak())
    
    def text(self, lineArray):
        line = lineArray.get()
        line = parser.parse_content_line(self, line)
        if line == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(line, self.styles["Normal"]))