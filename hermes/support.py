from reportlab.platypus import Flowable

tableContentCache = {}

class LineFeed:
    def __init__(self, lines):
        self.linePos = 0
        self.lines = lines

    def peek(self):
        if self.linePos < len(self.lines):
            return self.lines[self.linePos]
        else:
            return None

    def get(self):
        if self.linePos < len(self.lines):
            line = self.lines[self.linePos]
            self.linePos += 1
            return line
        else:
            return None

    def assign(self, line):
        if self.linePos < len(self.lines):
            self.lines[self.linePos] = line
        
    def reset(self):
        self.linePos = 0

class Bookmark(Flowable):
    def __init__(self, text, depth, key):
        Flowable.__init__(self)
        self.text = text
        self.depth = depth - 1
        self.key = key

    def __repr__(self):
        return "Bookmark: (%d: %s)" % (self.depth, self.text)

    def draw(self):
        self.canv.bookmarkPage(self.key)
        self.canv.addOutlineEntry(self.text, self.key, self.depth)

    def get_key(self):
        return self.key

class TOCEntry(Flowable):
    def __init__(self, text, depth, key):
        Flowable.__init__(self)
        self.text = text
        self.depth = depth
        self.key = key
    
    def draw(self):
        global tableContentCache
        tableContentCache[self.key] = [self.text, self.depth, self.canv.getPageNumber()]