import parser
import re
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

    reHeader = re.compile(r"^(#{1,6})(\{(.+)\})? (.+)$")
    def header(self, lineArray):
        result = re.search(self.reHeader, lineArray.get())
        depth = len(result.group(1))
        content = result.group(4)
        if depth == 1:
            self.content.append(Paragraph(content, self.styles["Heading 1"]))
    
    def text(self, lineArray):
        line = lineArray.get()
        line = parser.parse_content_line(self, line)
        if line == "":
            self.content.append(Spacer(0, 12))
        else:
            self.content.append(Paragraph(line, self.styles["Normal"]))