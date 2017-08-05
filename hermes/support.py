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