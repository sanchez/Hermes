
function Doc() {

    this.defaultSize = 18;
    this.headingOne = 26;
    this.headingTwo = 24;
    this.headingThree = 22;
    this.primaryColor = "blue";
    this.blackColor = "black";

    this.heading = function(doc, headingLevel, headingText, headingOptions) {
        console.log("Heading Found");
        doc.push("\\section{"+ headingText +"}");
    }

    this.pre_document = function(doc, options) {
        doc.push("\\documentclass{article}");
        doc.push("\\begin{document}");
    }

    this.post_document = function(doc, options) {
        doc.push("\\end{document}");
    }

    this.text = function(doc, text) {
        doc.push("\\noindent");
        if (text == "") {
            doc.push("\\null\\par");
        } else {
            doc.push(text);
            doc.push("\\par");

        }
    }
}

module.exports = new Doc();
