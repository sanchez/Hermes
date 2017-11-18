
var chalk = require("chalk");
var parser = require("../lib/parser.js");

module.exports = {
    text: function(lines, buffer, addP=true) {
        // TODO: Add find and replace of characters
        var line = lines.get();
        if (addP) {
            buffer += "<p>";
        }
        for (var key in global.textReplace) {
            if (global.textReplace[key].test(line)) {
                line = global.textLookup[key](this, line);
            }
        }
        if (addP) {
            buffer += line + "</p>\n";
        } else {
            buffer += line + "\n";
        }
        return buffer;
    },

    header: function(depth, text, buffer) {
        buffer += `<h${depth}>${text}</h${depth}>\n`;
        return buffer;
    },

    load_parses: function () {
    },

    styles: ["default.css"],
    defaultColor: "orange"
}
