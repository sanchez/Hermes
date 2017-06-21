
function Doc() {

    this.lastLineText = false;

    this.boldText = "\\textbf{$1}";
    this.italicsText = "\\textit{$1}";

    this.heading = function(doc, headingLevel, headingText, headingOptions) {
        this.lastLineText = false;
        if (headingLevel == 1) {
            doc.push("\\section{"+ headingText +"}");
        } else if (headingLevel == 2) {
            doc.push("\\subsection{"+ headingText +"}");
        } else if (headingLevel == 3) {
            doc.push("\\subsubsection{"+ headingText +"}");
        }
    }

    this.pre_document = function(doc, options) {
        doc.push("\\documentclass{article}");
        doc.push("\\begin{document}");
    }

    this.post_document = function(doc, options) {
        doc.push("\\end{document}");
    }

    this.text = function(doc, text) {
        if (this.lastLineText == true) {
            doc.push("\\null\\par\\noindent");
        }
        doc.push(text);
        this.lastLineText = true;
    }
}

module.exports = new Doc();
