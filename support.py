from reportlab.platypus import (Flowable, Paragraph, SimpleDocTemplate, Spacer)

def get_key():
    get_key.i += 1
    return get_key.i
get_key.i = 0

class Bookmark(Flowable):
    def __init__(self, text, depth):
        Flowable.__init__(self)
        self.text = text
        self.depth = depth - 1
        self.key = "B%d" % get_key()

    def __repr__(self):
        return "Bookmark: (%d: %s)" % (self.depth, self.text)

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.text, self.key, self.depth)

    def get_key(self):
        return self.key