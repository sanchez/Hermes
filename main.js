#!/usr/bin/env node

var chalk = require('chalk');
console.log(chalk.blue("Running Hermes - Markdown to pdf"));
var PDFDocument = require('pdfkit');
var doc = new PDFDocument({bufferPages: true});
var handler = require("./lib/doc.js");

function check_arguments(args) {
    if (args.length != 2) {
        console.log(chalk.bold.red("Invalid arguments length"));
        process.exit(1);
    }
    
    var fs = require("fs");
    var contents = fs.readFileSync(args[0], 'utf8');
    doc.pipe(fs.createWriteStream(args[1]));
    return contents;
}

function process_header(line) {
    var regex = /^(#{1,3})(\{(.+)\})? (.+)$/;
    var result = line.match(regex);
    if (result == null) {
        return false;
    }
    var headingLevel = result[1];
    var headingText = result[4];
    var headingOptions = result[3];
    handler.heading(doc, headingLevel, headingText, headingOptions);
    return true;
}

function process_plain_text(line) {
    line = line.replace(/\\#/g, "#");
    console.log("Text: " + line);
    return true;
}

var contents = check_arguments(process.argv.slice(2));
contents.split("\n").forEach((line) => {
    if (process_header(line)) {
    } else {
        process_plain_text(line);
    }
});

doc.flushPages();
doc.end();
