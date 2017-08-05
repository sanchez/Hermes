import parser
import re
import support
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

class docDefault():
    def __init__(self, config):
        print("Loading Default Template")

        parser.set_lookup(self.reHeader, "header")

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
        self.content.append(support.Bookmark(content, depth, key))
        self.content.append(support.TOCEntry(content, depth, key))
    
    def text(self, lineArray):
        line = lineArray.get()
        line = parser.parse_content_line(self, line)
        if line == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(line, self.styles["Normal"]))