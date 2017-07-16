#!/usr/bin/python3

import sys
from reader import Parser
from docDefault import Handler

def main():
    print("Running Hermes")
    sourceFile = sys.argv[1];
    originalFile = Parser(sourceFile)

if __name__ == '__main__':
    main()