#!/usr/bin/python3

import sys
from reader import FileReader

def main():
    print("Running Hermes")
    sourceFile = sys.argv[1];
    destFile = "test.pdf"
    originalFile = FileReader(sourceFile)

if __name__ == '__main__':
    main()