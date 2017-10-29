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

module.exports = {
    parse: function(lines, template) {
        var buffer = "<html>";
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
        buffer += "</html>";
        return buffer;
    },

    add: function(name, re, func) {
        global.lookupPair[name] = re;
        global.parsePair[name] = func;
    }
}
