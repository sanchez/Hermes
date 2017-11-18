#!/usr/bin/env node

var chalk = require("chalk");
console.log(chalk.blue("Running Hermes - Markdown to pdf"));
var Regex = require("regex");

function check_args(args) {
    if (args.length != 2) {
        console.log(chalk.bold.red("Invalid arguments length"));
        process.exit(1);
    }
    console.log(chalk.magenta(`Got ${args[0]} -> ${args[1]}`));
}

function get_file_in(args) {
    console.log(chalk.gray("Reading from file"));
    var contents = require("fs").readFileSync(args[0], 'utf-8');
    return contents;
}

var regHeader = new RegExp(/^```$/);
var regKeyValue = new RegExp(/^(.+): (.+)$/);
function read_header(lines) {
    var headerContent = {};
    if (regHeader.test(lines.get())) {
        console.log(chalk.gray("Got start header"));
    } else {
        console.log(chalk.red("Could not find header"));
        return headerContent;
    }
    while (1) {
        if (regHeader.test(lines.peek())) {
            lines.get();
            break;
        }
        if (lines.peek() == undefined) {
            console.log(chalk.red("Could not find ending header"));
            return headerContent;
        }
        var currentLine = regKeyValue.exec(lines.get());
        headerContent[currentLine[1]] = currentLine[2];
    }
    if (headerContent["template"] == undefined) {
        console.log(chalk.yellow("Could not find template"));
        headerContent["template"] = "default";
    }
    return headerContent;
}

function load_template(templateName) {
    var headerLocation = `./template/${templateName}.js`;
    var docTemplate = require(headerLocation);
    if (docTemplate == undefined) {
        console.log(chalk.red("Invalid template name"));
        docTemplate = include("./template/default.js");
    }
    return docTemplate;
}

check_args(process.argv.slice(2));
var lineObject = {
    lines: get_file_in(process.argv.slice(2)).split("\n"),
    pos: 0,
    peek: function() {
        return this.lines[this.pos];
    },
    get: function() {
        return this.lines[this.pos++];
    },
    set: function(newLine) {
        return this.lines[this.pos++];
    }
};

var header = read_header(lineObject);
var docTemplate = load_template(header["template"]);
docTemplate.load_parses();
var parser = require("./lib/parser.js");
var resultHtml = parser.parse(lineObject, docTemplate);
console.log(resultHtml);
var fs = require("fs");
fs.writeFile("./test.html", resultHtml, function(err) {
    if (err) {
        console.log(err);
    }
});

var newConfig = {
    "format": "A4",
    "renderDelay": "3000"
};
var pdf = require("html-pdf");
pdf.create(resultHtml, newConfig).toFile(process.argv.slice(2)[1], function(err, res) {
    if (err) {
        console.log(chalk.red(err));
    }
    console.log(res);
});
