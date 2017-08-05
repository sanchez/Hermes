import re
import support

lookup = {}
lineLookup = {}

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
    for key in lookup:
        if re.search(key, line):
            methodToCall = getattr(handler, lineLookup[key])
            if methodToCall:
                line = methodToCall(line)
    return line