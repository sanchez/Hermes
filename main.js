#!/usr/bin/env node

var chalk = require('chalk');
var fs = require("fs");
console.log(chalk.blue("Running Hermes - Markdown to pdf"));
var handler = require("./lib/doc.js");
var docCache = [];
var outputFileName;

function check_arguments(args) {
    if (args.length != 2) {
        console.log(chalk.bold.red("Invalid arguments length"));
        process.exit(1);
    }
    
    var contents = fs.readFileSync(args[0], 'utf8');
    outputFileName = args[1];
    return contents;
}

function process_header(line) {
    var regex = /^(#{1,3})(\{(.+)\})? (.+)$/;
    var heading = line.check_line();
    var result = heading.match(regex);
    if (result == null) {
        return false;
    }
    var headingLevel = result[1];
    var headingText = result[4];
    var headingOptions = result[3];
    handler.heading(docCache, headingLevel, headingText, headingOptions);
    line.get_line();
    return true;
}

function process_plain_text(line) {
    var text = line.get_line();
    handler.text(docCache, text);
    return true;
}

var contents = check_arguments(process.argv.slice(2));
var lineObject = {
    lines: contents.split("\n"),
    pos: 0,
    check_line: function() {
        return this.lines[this.pos];
    },
    get_line: function() {
        return this.lines[this.pos++];
    }
};
console.log(lineObject);

handler.pre_document(docCache, undefined);
while (lineObject.check_line() != undefined) {
    if (process_header(lineObject)) {
    } else {
        process_plain_text(lineObject);
    }
}
handler.post_document(docCache, undefined);

if (!fs.existsSync(".hermes")) {
    fs.mkdirSync(".hermes");
}
process.chdir(".hermes");
var file = fs.createWriteStream("main.tex");
docCache.forEach(function (line) {
    file.write(line + '\n');
});
console.log("File Written");
var spawn = require("child_process").spawn;
var child = spawn('pdflatex', ['main.tex']);
child.stdout.on('data', function (chunk) {
    process.stdout.write(chalk.yellow(chunk));
});
child.on('exit', function() {
    var source = fs.createReadStream('main.pdf');
    var dest = fs.createWriteStream('../main.pdf');

    source.pipe(dest);
    source.on('end', function() { console.log(chalk.green("Copied successfully")); });
    source.on('error', function(err) { console.log(chalk.red("Error: " + err)); });
});

console.log(docCache);
