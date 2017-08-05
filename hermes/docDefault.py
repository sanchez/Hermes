import parser
import re
import support
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.tableofcontents import TableOfContents

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
        print("Making title")

    def header_footer(self, canv, doc):
        print("Page")

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