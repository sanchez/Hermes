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

function parse_code_block(lines, template, buffer) {
    lines.get();
    var innerLines = [];
    while (1) {
        if (global.lookupPair["Code"].test(lines.peek())) {
            lines.get();
            break;
        }
        innerLines.push(lines.get());
    }
    var newInputLines = {
        lines: innerLines,
        pos: 0,
        peek: function() {
            return this.lines[this.pos];
        },
        get: function() {
            return this.lines[this.pos++];
        }
    };
    buffer += "<code class='block'>";
    buffer = require("./parser.js").parse_block(newInputLines, template, buffer);
    buffer += "</code>";
    return buffer;
}

function parse_eq_block(lines, template, buffer) {
    lines.get();
    buffer += "<p>\\[";
    while (1) {
        if (global.lookupPair["Equation"].test(lines.peek())) {
            lines.get();
            break;
        }
        buffer += lines.get();
    }
    buffer += "\\]</p>";
    return buffer;
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

function parse_code(template, line) {
    var broken = line.split(global.textReplace["Code"]);
    var newLine = "";
    var opened = 0;
    for (var chunk in broken) {
        newLine += broken[chunk];
        if (chunk < (broken.length - 1)) {
            if (opened) {
                newLine += "</code>";
                opened = 0;
            } else {
                newLine += "<code>";
                opened = 1;
            }
        }
    }
    return newLine;
}

function parse_super_start(template, line) {
    return line.replace(global.textReplace["SuperStart"], "<sup>");
}

function parse_super_end(template, line) {
    return line.replace(global.textReplace["SuperEnd"], "</sup>");
}

function parse_sub_start(template, line) {
    return line.replace(global.textReplace["SubStart"], "<sub>");
}

function parse_sub_end(template, line) {
    return line.replace(global.textReplace["SubEnd"], "</sub>");
}

function parse_color(template, line) {
    while (global.textReplace["Color"].test(line)) {
        var res = global.textReplace["Color"].exec(line);
        if (res[1] == '') {
            res[1] = template.defaultColor;
        }
        line = line.replace(global.textReplace["Color"], `<span style="color: ${res[1]}">${res[2]}</span>`);
    }
    return line;
}

global.lookupPair = {
    "Comment": new RegExp(/^\\(.*)$/),
    "Header": new RegExp(/^(#{1,6}) (.+)$/),
    "Code": new RegExp(/^`{3}$/),
    "Equation": new RegExp(/^\$\$\$$/)
}
global.parsePair = {
    "Comment": parse_comment,
    "Header": parse_header,
    "Code": parse_code_block,
    "Equation": parse_eq_block
};
global.commandLookup = {
    "tp": parse_tp,
    "toc": parse_toc
};
global.textReplace = {
    "Bold": new RegExp(/\*{2}/),
    "Italics": new RegExp(/\*/),
    "SuperStart": new RegExp(/\{{2}/),
    "SuperEnd": new RegExp(/\}{2}/),
    "SubStart": new RegExp(/\{/),
    "SubEnd": new RegExp(/\}/),
    "Code": new RegExp(/`/),
    "Color": new RegExp(/~\((\w*)\)([^~]+)~/)
};
global.textLookup = {
    "Bold": parse_bold,
    "Italics": parse_italics,
    "SuperStart": parse_super_start,
    "SuperEnd": parse_super_end,
    "SubStart": parse_sub_start,
    "SubEnd": parse_sub_end,
    "Code": parse_code,
    "Color": parse_color
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

        buffer = this.parse_block(lines, template, buffer);

        buffer += "<script type='text/x-mathjax-config'>MathJax.Hub.Config({tex2jax: {inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]}});</script>";
        buffer += "<script src='file:///home/sanchez/Documents/git/Hermes/node_modules/mathjax/MathJax.js?config=TeX-AMS_CHTML'></script>";

        buffer += "</body></html>";
        return buffer;
    },

    parse_block: function(lines, template, buffer) {
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
        return buffer;
    },

    add: function(name, re, func) {
        global.lookupPair[name] = re;
        global.parsePair[name] = func;
    }
}
