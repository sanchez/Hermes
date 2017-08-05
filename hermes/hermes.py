#!/usr/bin/python3

import sys
import docDefault
from support import LineFeed
import re
import parser
from pydoc import locate
from reportlab.lib.pagesizes import A4

class Hermes:
    re_config_block = re.compile(r"^---$")
    re_config_line = re.compile(r"^(.+):\s?(.+)$")

    def __init__(self, inputFileName, root=False):
        print("Input: %s" % inputFileName)
        self.inputFileName = inputFileName
        self.inFile = open(self.inputFileName, "r")
        self.fileContents = self.inFile.read().split("\n")
        self.lines = LineFeed(self.fileContents)
        self.content = []
        self.config = {}
        self.load_config()
        parser.parse_lines(self.doc, self.lines)

    def load_config(self):
        if re.search(self.re_config_block, self.lines.peek()):
            self.lines.get()
            while self.lines.peek() != None:
                if re.search(self.re_config_block, self.lines.peek()):
                    self.lines.get()
                    break
                result = re.search(self.re_config_line, self.lines.peek())
                if result:
                    self.config[result.group(1)] = result.group(2)
                self.lines.get()
        docHandler = docDefault.docDefault
        if "doc" in self.config:
            print("Found doc type: %s" % self.config["doc"])
            docHandler = locate("%s.%s" % (self.config["doc"], self.config["doc"]))
        self.doc = docHandler(self.config)
    
    def save(self, destName):
        print("Output: %s" % destName)
        template = docDefault.MyDocTemplate(destName, bottomup=0, pagesize=A4, topMargin=40, bottomMargin=40, leftMargin=40, rightMargin=40)
        if "titlePage" in self.config:
            template.multiBuild(self.doc.get_content(), onFirstPage=self.doc.title, onLaterPages=self.doc.header_footer)
        else:
            template.multiBuild(self.doc.get_content(), onFirstPage=self.header_footer, onLaterPages=self.header_footer)

def main():
    print("Running Hermes")
    hermes = Hermes(sys.argv[1])
    hermes.save(sys.argv[2])

if __name__ == '__main__':
    main()