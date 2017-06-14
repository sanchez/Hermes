
function String() {
    this.count = function(string) {
        for (var i = 0; i < string.length; i++) {
            console.log("Read: " + string.charAt(i));
        }
    }
}
