import re

class FileReader:

    re_heading = re.compile(r"^(#{1,6})(\{(.+)\})? (.+)$")

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
            print("Processing line: " + line)
            if self.if_header(line):
                self.process_header(line)
            else:
                self.process_plain_text(line)

    def if_header(self, line):
        result = re.search(self.re_heading, line)
        if result == None:
            return False
        return True

    def process_header(self, line):
        result = re.search(self.re_heading, line)
        heading_depth = len(result.group(1))
        heading_options = result.group(3)
        heading_title = result.group(4)
        self.docHandler.add_heading(heading_title, heading_depth, heading_options)

    def process_plain_text(self, line):
        self.docHandler.add_plain_text(line)