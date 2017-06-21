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

function process_bold(line) {
    var text = line.check_line();
    var result = text.replace(/\*{2}(\w+)\*{2}/g, handler.boldText);
    line.set_line(result);
}

function process_italics(line) {
    var text = line.check_line();
    var result = text.replace(/\*(\w+)\*/g, handler.italicsText);
    line.set_line(result);
}

function process_header(line) {
    var regex = /^(#{1,6})(\{(.+)\})? (.+)$/;
    var heading = line.check_line();
    var result = heading.match(regex);
    if (result == null) {
        return false;
    }
    var headingLevel = result[1].length;
    var headingText = result[4];
    var headingOptions = result[3];
    handler.heading(docCache, headingLevel, headingText, headingOptions);
    line.get_line();
    return true;
}

function process_bullet_point(line) {
    var regex = /^( +)*- (.+)$/;
    var bullet = line.check_line();
    var result = bullet.match(regex);
    if (result == null) {
        return false;
    }
    console.log(result);
    var bulletLevel = (result[1] == undefined) ? 1 : result[1].length/4;
    var bulletText = result[2];
    handler.bullet(docCache, bulletLevel, bulletText);
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
    },
    set_line: function(newLine) {
        this.lines[this.pos] = newLine;
    }
};

handler.pre_document(docCache, undefined);
while (lineObject.check_line() != undefined) {
    process_bold(lineObject);
    process_italics(lineObject);
    if (process_header(lineObject)) {
    } else if (process_bullet_point(lineObject)) {
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
