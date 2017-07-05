import re

class FileReader:

    re_heading = re.compile(r"^(#{1,6})(\{(.+)\})? (.+)$")
    re_bold = re.compile(r"\*{2}(\w+)\*{2}")
    re_italics = re.compile(r"\*(\w+)\*")
    re_bullet_item = re.compile(r"^(.*)[-\.\*] (.+)$")
    re_num_item = re.compile(r"^(.*)\d+[\)\.] (.+)$")

    def __init__(self, sourceFile, docHandler):
        print("Reading from file: %s" % sourceFile)
        self.fileName = sourceFile
        self.docHandler = docHandler

        self.file = open(self.fileName, "r")
        self.fileContents = self.file.read().split("\n");

        self.process_file()
        docHandler.save()

    def process_file(self):
        for line in self.fileContents:
            line.strip()
            line = self.process_bold(line)
            line = self.process_italics(line)
            if self.if_header(line):
                self.process_header(line)
            elif self.if_bullet(line):
                self.process_bullet(line)
            else:
                self.process_plain_text(line)

    def if_header(self, line):
        result = re.search(self.re_heading, line)
        if result == None:
            return False
        return True

    def process_bold(self, line):
        return re.sub(self.re_bold, self.docHandler.add_bold, line)

    def process_italics(self, line):
        return re.sub(self.re_italics, self.docHandler.add_italics, line)

    def process_header(self, line):
        result = re.search(self.re_heading, line)
        headingDepth = len(result.group(1))
        headingOptions = result.group(3)
        headingTitle = result.group(4)
        self.docHandler.add_heading(headingTitle, headingDepth, headingOptions)

    def if_bullet(self, line):
        return re.search(self.re_bullet_item, line) != None
    
    def process_bullet(self, line):
        result = re.search(self.re_bullet_item, line)
        bulletDepth = len(result.group(1)) / 4
        bulletText = result.group(2)
        self.docHandler.add_bullet(bulletText, bulletDepth)

    def if_list(self, line):
        return re.search(self.re_num_item, line) != None

    def process_list(self, line):
        result = re.search(self.re_num_item, line)
        listDepth = len(result.group(1)) / 4
        listText = result.group(2)
        self.docHandler.add_list(listText, listDepth)

    def process_plain_text(self, line):
        self.docHandler.add_plain_text(line)