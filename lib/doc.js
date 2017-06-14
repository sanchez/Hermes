
function Doc() {

    this.defaultSize = 18;
    this.headingOne = 26;
    this.headingTwo = 24;
    this.headingThree = 22;
    this.primaryColor = "blue";
    this.blackColor = "black";

    this.heading = function(doc, headingLevel, headingText, headingOptions) {
        doc.fillColor(this.primaryColor)
            .fontSize 26
    }
}

module.exports = new Doc();
