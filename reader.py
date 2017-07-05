import re
from docDefault import Handler

class FileReader:

    def __init__(self, sourceFile):
        self.fileName = sourceFile
        self.file = open(self.fileName, "r")
        self.fileContents = self.file.read().split("\n")
        self.linePos = 0
        for i in range(len(self.fileContents)):
            self.fileContents[i].strip()

    def peek(self):
        if self.linePos < len(self.fileContents):
            return self.fileContents[self.linePos]
        else:
            return None

    def get(self):
        if self.linePos < len(self.fileContents):
            print("Get: %d:%s" % (self.linePos, self.fileContents[self.linePos]))
            line = self.fileContents[self.linePos]
            self.linePos += 1
            return line
        else:
            return None

    def assign(self, line):
        if self.linePos < len(self.fileContents):
            self.fileContents[self.linePos] = line
        
    def reset(self):
        self.linePos = 0

class Parser:

    re_heading = re.compile(r"^(#{1,6})(\{(.+)\})? (.+)$")
    re_bold = re.compile(r"\*{2}(\w+)\*{2}")
    re_italics = re.compile(r"\*(\w+)\*")
    re_bullet_item = re.compile(r"^(.*)[-\.\*] (.+)$")
    re_num_item = re.compile(r"^(.*)\d+[\)\.] (.+)$")

    def __init__(self, sourceFile):
        print("Reading from file: %s" % sourceFile)
        self.lines = FileReader(sourceFile)
        self.docHandler = Handler("test.pdf")

        self.process_file()
        self.docHandler.save()

    def process_file(self):
        while self.lines.peek() != None:
            line = self.lines.peek()
            line = self.process_bold(line)
            line = self.process_italics(line)
            self.lines.assign(line)
            self.lines.get()
        self.lines.reset()

        while self.lines.peek() != None:
            line = self.lines.peek()
            if re.search(self.re_heading, line):
                self.process_header()
            elif re.search(self.re_bullet_item, line):
                self.process_bullet()
            elif re.search(self.re_num_item, line):
                self.process_list()
            else:
                self.process_plain_text()

    def process_bold(self, line):
        return re.sub(self.re_bold, self.docHandler.add_bold, line)

    def process_italics(self, line):
        return re.sub(self.re_italics, self.docHandler.add_italics, line)

    def process_header(self):
        result = re.search(self.re_heading, self.lines.get())
        headingDepth = len(result.group(1))
        headingOptions = result.group(3)
        headingTitle = result.group(4)
        self.docHandler.add_heading(headingTitle, headingDepth, headingOptions)
    
    def process_bullet(self):
        listCache = []
        while self.lines.peek() != None:
            result = re.search(self.re_bullet_item, self.lines.peek())
            if not result:
                break
            self.lines.get()
            bulletDepth = len(result.group(1)) / 4
            bulletText = result.group(2)
            listCache.append((bulletText, bulletDepth))
        self.docHandler.add_bullet(listCache)

    def process_list(self):
        listCache = []
        indices = [1,1,1,1,1,1,1,1,1,1,1]
        lastDepth = 0
        while self.lines.peek() != None:
            result = re.search(self.re_num_item, self.lines.peek())
            if not result:
                break
            self.lines.get()
            listDepth = len(result.group(1)) / 4
            if listDepth > lastDepth:
                indices[listDepth] = 1
            listText = result.group(2)
            listCache.append((listText, listDepth, indices[listDepth]))
            indices[listDepth] += 1
            lastDepth = listDepth
        self.docHandler.add_list(listCache)

    def process_plain_text(self):
        self.docHandler.add_plain_text(self.lines.get())