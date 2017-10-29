
var chalk = require("chalk");

module.exports = {
    text: function(lines, buffer) {
        // TODO: Add find and replace of characters
        buffer += lines.get();
        buffer += "<br />\n";
        return buffer;
    },

    header: function(depth, text, buffer) {
        buffer += `<h${depth}>${text}</h${depth}>\n`;
        return buffer;        
    },

    load_parses: function () {

    }
}
