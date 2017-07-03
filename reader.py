class FileReader:
    def __init__(self, sourceFile):
        print("Reading from file: %s" % sourceFile)
        self.fileName = sourceFile

        self.file = open(self.fileName, "r")
        self.fileContents = self.file.read()

        self.process_file()

    def process_file(self):
        pass