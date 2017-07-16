#!/usr/bin/python3

import sys
from reader import Parser
from docDefault import Handler

def main():
    print("Running Hermes")
    sourceFile = sys.argv[1];
    outputFile = Handler(sys.argv[2]);
    originalFile = Parser(sourceFile, outputFile)

if __name__ == '__main__':
    main()