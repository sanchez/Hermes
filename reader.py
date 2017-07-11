import re
from docDefault import Handler

class FileReader:

    def __init__(self, sourceFile):
        self.fileName = sourceFile
        self.file = open(self.fileName, "r")
        self.fileContents = self.file.read().split("\n")
        self.linePos = 0
        for i in range(len(self.fileContents)):
            # self.fileContents[i].strip()
            pass

    def peek(self):
        if self.linePos < len(self.fileContents):
            return self.fileContents[self.linePos]
        else:
            return None

    def get(self):
        if self.linePos < len(self.fileContents):
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
    re_bold = re.compile(r"\*{2}([^\*]+)\*{2}")
    re_italics = re.compile(r"(?:\*|_)([^\*]+)(?:\*|_)")
    re_code_inline = re.compile(r"\`(.+)\`")
    re_double_dash = re.compile(r"([^-])(-{2})([^-])")
    re_code_block = re.compile(r"^```$")
    re_bullet_item = re.compile(r"^(\s*)[-\.\*] (.+)$")
    re_num_item = re.compile(r"^(\s*)\d+[\)\.] (.+)$")
    re_table_row = re.compile(r"\|\s([^\|]*)")
    re_table_line = re.compile(r"^(?:\|\s-*\s){1,}\|$")
    re_table_caption = re.compile(r"^:\s(.+)$")
    re_blockquote = re.compile(r"^> (.+)$")
    re_checklist = re.compile(r"^(\s*)\[(-?)\] (.+)$")
    re_config_block = re.compile(r"^---$")
    re_config_line = re.compile(r"^(.+):\s?(.+)$")
    re_newline = re.compile(r"^\\\\$")
    re_image = re.compile(r"^!\[(.+)\]\((.+)\)$")
    re_toc = re.compile(r"^\\toc$")
    re_comment = re.compile(r"^\\(.+)$")

    def __init__(self, sourceFile):
        print("Reading from file: %s" % sourceFile)
        self.lines = FileReader(sourceFile)
        self.docHandler = Handler("test.pdf")
        self.config = {}

        self.process_file()
        self.docHandler.save()

    def process_file(self):
        while self.lines.peek() != None:
            line = self.lines.peek()
            line = self.process_code_inline(line)
            line = self.process_bold(line)
            line = self.process_italics(line)
            line = self.process_double_dash(line)
            #print(line)
            self.lines.assign(line)
            self.lines.get()
        self.lines.reset()

        if re.search(self.re_config_block, self.lines.peek()):
            self.process_config()

        while self.lines.peek() != None:
            line = self.lines.peek()
            if re.search(self.re_heading, line):
                self.process_header()
            elif re.search(self.re_num_item, line):
                self.process_list()
            elif re.search(self.re_bullet_item, line):
                self.process_bullet()
            elif re.search(self.re_table_row, line):
                self.process_table()
            elif re.search(self.re_blockquote, line):
                self.process_blockquote()
            elif re.search(self.re_checklist, line):
                self.process_checklist()
            elif re.search(self.re_code_block, line):
                self.process_code()
            elif re.search(self.re_newline, line):
                self.lines.get()
                self.docHandler.add_newline()
            elif re.search(self.re_image, line):
                self.process_image()
            elif re.search(self.re_toc, line):
                self.lines.get()
                self.docHandler.add_toc()
            elif re.search(self.re_comment, line):
                self.lines.get()
            else:
                self.process_plain_text()

    def process_double_dash(self, line):
        return re.sub(self.re_double_dash, self.docHandler.add_double_dash, line)

    def process_bold(self, line):
        return re.sub(self.re_bold, self.docHandler.add_bold, line)

    def process_italics(self, line):
        return re.sub(self.re_italics, self.docHandler.add_italics, line)

    def process_code_inline(self, line):
        if re.search(self.re_code_block, line):
            return line
        return re.sub(self.re_code_inline, self.docHandler.add_code_inline, line)

    def process_config(self):
        self.lines.get()
        configCache = {}
        while self.lines.peek() != None:
            # print(self.lines.peek())
            result = re.search(self.re_config_line, self.lines.get())
            if not result:
                break
            configKey = result.group(1)
            configValue = result.group(2)
            configCache[configKey] = configValue
        self.config = configCache
        self.docHandler.set_config(self.config)

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
            listDepth = int(len(result.group(1)) / 4)
            if listDepth > lastDepth:
                indices[listDepth] = 1
            listText = result.group(2)
            listCache.append((listText, listDepth, indices[listDepth]))
            indices[listDepth] += 1
            lastDepth = listDepth
        self.docHandler.add_list(listCache)

    def process_table(self):
        headerRow = re.findall(self.re_table_row, self.lines.get())
        tableData = []
        captionData = None
        if not re.search(self.re_table_line, self.lines.peek()):
            tableData.append(headerRow)
            headerRow = None
            result = re.findall(self.re_table_row, self.lines.peek())
            if result != None:
                tableData.append(result)
        self.lines.get()
        while self.lines.peek() != None:
            caption = re.search(self.re_table_caption, self.lines.peek())
            if caption:
                captionData = caption.group(1)
                self.lines.get()
                break
            result = re.findall(self.re_table_row, self.lines.peek())
            if not result:
                break
            self.lines.get()
            tableData.append(result)
        self.docHandler.add_table(headerRow, tableData, captionData)

    def process_code(self):
        codeCache = []
        firstLine = re.search(self.re_code_block, self.lines.get())
        while self.lines.peek() != None:
            result = re.search(self.re_code_block, self.lines.peek())
            if result:
                self.lines.get()
                break
            codeCache.append(self.lines.get())
        self.docHandler.add_code(codeCache)

    def process_blockquote(self):
        text = re.search(self.re_blockquote, self.lines.get())
        self.docHandler.add_blockquote(text.group(1))

    def process_checklist(self):
        checklist = re.search(self.re_checklist, self.lines.get())
        depth = len(checklist.group(1)) / 4
        checked = len(checklist.group(2)) == 1
        text = checklist.group(3)
        self.docHandler.add_checklist(checked, text, depth)

    def process_image(self):
        result = re.search(self.re_image, self.lines.get())
        location = result.group(2)
        captionData = result.group(1)
        self.docHandler.add_image(location, captionData)


    def process_plain_text(self):
        self.docHandler.add_plain_text(self.lines.get())