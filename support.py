from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer, XPreformatted)
from reportlab.lib import colors

def get_key():
    get_key.i += 1
    return get_key.i
get_key.i = 0

class Bookmark(Flowable):
    def __init__(self, text, depth):
        Flowable.__init__(self)
        self.text = text
        self.depth = depth - 1
        self.key = "B%d%s" % (depth, text)

    def __repr__(self):
        return "Bookmark: (%d: %s)" % (self.depth, self.text)

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.text, self.key, self.depth)

    def get_key(self):
        return self.key

class BlockQuote(Flowable):
    def __init__(self, text, style):
        Flowable.__init__(self)
        self.text = text
        self.p = Paragraph(self.text, style=style)
        width, height = self.p.wrapOn(None, 450, 0)
        self.height = height

    def draw(self):
        self.p.drawOn(self.canv, 0, 0)

        self.canv.setStrokeColor(colors.grey)
        self.canv.line(0, -1, 0, self.height - 1)

class CodeBlock(Flowable):
    def __init__(self, text, style):
        Flowable.__init__(self)
        self.p = XPreformatted(text, style)
        width, height = self.p.wrap(450, 0)
        self.height = height
        self.lines = height / (style.fontSize + 2)

    def draw(self):
        self.p.drawOn(self.canv, 0, 0)

        self.canv.setStrokeColor(colors.black)
        self.canv.line(24, -1, 24, self.height - 1)
        for i in range(1, int(self.lines + 1)):
            xPos = 12
            if i > 99:
                xPos = 0
            elif i > 9:
                xPos = 6
            self.canv.drawString(xPos, (self.lines - i) * 12, str(i))

class ResetPageNum(Flowable):
    def draw(self):
        pass