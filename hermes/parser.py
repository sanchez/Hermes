import re
import support

lookup = {}
lineLookup = {
    re.compile(r"\*{2}([^*]+)\*{2}"): "bold",
    re.compile(r"\*([^*]+)\*"): "italics"
}
symbolLibrary = {
    "--": "&ndash;",
    "<->": "&harr;",
    "<-": "&larr;",
    "->": "&rarr;",
    "(/)": "&empty;",
    "\_": "&#95;",
    "\|": "&#124;"
}

def set_lookup(key, value):
    global lookup
    lookup[key] = value

def set_line_lookup(key, value):
    global lineLookup
    lineLookup[key] = value

def parse_lines(handler, lines):
    while lines.peek() != None:
        line = lines.peek()
        for key in lookup:
            if re.search(key, line):
                methodToCall = getattr(handler, lookup[key])
                if methodToCall:
                    methodToCall(lines)
                    break
        else:
            handler.text(lines)

def parse_content_line(handler, line):
    line = parse_symbol_line(line)
    for key in lineLookup:
        methodToCall = getattr(handler, lineLookup[key])
        line = re.sub(key, methodToCall, line)
    return line

def parse_symbol_line(line):
    for key in symbolLibrary:
        line = line.replace(key, symbolLibrary[key])
    return line