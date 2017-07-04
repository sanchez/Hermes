#!/usr/bin/python3

import sys
from reader import FileReader
from docDefault import Handler

def main():
    print("Running Hermes")
    sourceFile = sys.argv[1];
    destFile = "test.pdf"
    outputHandler = Handler(destFile)
    originalFile = FileReader(sourceFile, outputHandler)

if __name__ == '__main__':
    main()