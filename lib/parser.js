var chalk = require("chalk");

function parse_text(lines, template, buffer) {
    return template.text(lines, buffer);
}

function parse_comment(lines, template, buffer) {
    var command = global.lookupPair["Comment"].exec(lines.get())[1];
    for (var c in global.commandLookup) {
        if (c == command) {
            return global.commandLookup[c](template, buffer);
        }
    }
    return buffer;
}

function parse_header(lines, template, buffer) {
    var res = global.lookupPair["Header"].exec(lines.get());
    return template.header(res[1].length, res[2], buffer);
}

function parse_tp(template, buffer) {
    console.log(chalk.gray("Title Page not supported yet"));
    return buffer;
}

function parse_toc(template, buffer) {
    console.log(chalk.gray("Table of contents not supported yet"));
    return buffer;
}

function parse_bold(template, line) {
    var broken = line.split(global.textReplace["Bold"]);
    var newLine = "";
    var opened = 0;
    for (var chunk in broken) {
        newLine += broken[chunk];
        if (chunk < (broken.length - 1)) {
            if (opened) {
                newLine += "</b>";
                opened = 0;
            } else {
                newLine += "<b>";
                opened = 1;
            }
        }
    }
    return newLine;
}

function parse_italics(template, line) {
    var broken = line.split(global.textReplace["Italics"]);
    var newLine = "";
    var opened = 0;
    for (var chunk in broken) {
        newLine += broken[chunk];
        if (chunk < (broken.length - 1)) {
            if (opened) {
                newLine += "</em>";
                opened = 0;
            } else {
                newLine += "<em>";
                opened = 1;
            }
        }
    }
    return newLine;
}

global.lookupPair = {
    "Comment": new RegExp(/^\\(.*)$/),
    "Header": new RegExp(/^(#{1,6}) (.+)$/)
}
global.parsePair = {
    "Comment": parse_comment,
    "Header": parse_header
};
global.commandLookup = {
    "tp": parse_tp,
    "toc": parse_toc
};
global.textReplace = {
    "Bold": new RegExp(/\*{2}/),
    "Italics": new RegExp(/\*/)
};
global.textLookup = {
    "Bold": parse_bold,
    "Italics": parse_italics
};

function load_css(template, buffer) {
    buffer += "<style>";
    var fs = require("fs");
    for (var file in template.styles) {
        var fileContent = fs.readFileSync(`./template/${template.styles[file]}`, "utf8");
        buffer += fileContent;
    }
    buffer += "</style>";
    return buffer;
}

module.exports = {
    parse: function(lines, template) {
        var buffer = "<html>";
        buffer += "<head>";
        buffer = load_css(template, buffer);
        buffer += "</head>";
        buffer += "<body>\n";
        while (1) {
            if (lines.peek() == undefined) {
                break;
            }

            var foundKey = 0;
            for (var name in global.lookupPair) {
                var reg = global.lookupPair[name];
                if (reg.test(lines.peek())) {
                    buffer = global.parsePair[name](lines, template, buffer);
                    foundKey = 1;
                    break;
                }
            }
            if (!foundKey) {
                buffer = parse_text(lines, template, buffer);
            }

        }
        buffer += "</body></html>";
        return buffer;
    },

    add: function(name, re, func) {
        global.lookupPair[name] = re;
        global.parsePair[name] = func;
    }
}
