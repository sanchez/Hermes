
var chalk = require("chalk");
var parser = require("../lib/parser.js");

module.exports = {
    text: function(lines, buffer) {
        // TODO: Add find and replace of characters
        var line = lines.get();
        for (var key in global.textReplace) {
            if (global.textReplace[key].test(line)) {
                line = global.textLookup[key](this, line);
            }
        }
        buffer += line + "<br />\n";
        return buffer;
    },

    header: function(depth, text, buffer) {
        buffer += `<h${depth}>${text}</h${depth}>\n`;
        return buffer;
    },

    load_parses: function () {
    }
}
