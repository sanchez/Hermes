#!/usr/bin/env node

function check_arguments(args) {
    if (args.length == 1) {
        console.log(chalk.bold.red("Invalid arguments length"));
        process.exit(1);
    }
    return args
}

var chalk = require('chalk');
console.log(chalk.blue("Running Hermes - Markdown to pdf"));
global.args = check_arguments(process.argv.slice(2));


console.log(global.args);
