
function Doc() {

    this.lastCommand = "";

    this.boldText = "\\textbf{$1}";
    this.italicsText = "\\textit{$1}";

    this.end_bullet = function(doc) {
        if (this.lastCommand == "bullet") {
            for (var i = 0; i < this.currentBulletLevel; i++) {
                doc.push("\\end{itemize}");
            }
        }
    }

    this.heading = function(doc, headingLevel, headingText, headingOptions) {
        this.end_bullet(doc);
        this.lastCommand = "heading";
        if (headingLevel == 1) {
            doc.push("\\section{"+ headingText +"}");
        } else if (headingLevel == 2) {
            doc.push("\\subsection{"+ headingText +"}");
        } else if (headingLevel == 3) {
            doc.push("\\subsubsection{"+ headingText +"}");
        }
    }

    this.currentBulletLevel = 1;
    this.bullet = function(doc, bulletLevel, bulletText) {
        if (this.lastCommand != "bullet") {
            doc.push("\\begin{itemize}");
            this.currentBulletLevel = bulletLevel;
        }
        this.lastCommand = "bullet";
        if (bulletLevel > this.currentBulletLevel) {
            doc.push("\\begin{itemize}");
            this.currentBulletLevel = bulletLevel;
        } else if (bulletLevel < this.currentBulletLevel) {
            doc.push("\\end{itemize}");
            this.currentBulletLevel = bulletLevel;
        }
        doc.push("\\item " + bulletText);
    }

    this.pre_document = function(doc, options) {
        this.lastCommand = "pre";
        doc.push("\\documentclass{article}");
        doc.push("\\begin{document}");
    }

    this.post_document = function(doc, options) {
        this.end_bullet(doc);
        this.lastCommand = "post";
        doc.push("\\end{document}");
    }

    this.text = function(doc, text) {
        this.end_bullet(doc);
        if (this.lastCommand == "text") {
            doc.push("\\null\\par\\noindent");
        }
        doc.push(text);
        this.lastCommand = "text";
    }
}

module.exports = new Doc();
