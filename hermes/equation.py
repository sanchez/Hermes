from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Flowable, Paragraph, Image
from reportlab.lib.enums import TA_CENTER
from subprocess import call

def get_equation_count():
    get_equation_count.i += 1
    return get_equation_count.i
get_equation_count.i = 0

equationStyle = ParagraphStyle(
    "Equation",
    parent=getSampleStyleSheet()["Normal"],
    fontName="Courier",
    alignment=TA_CENTER
)

class EquationBlock(Flowable):
    def __init__(self, equationLines):
        Flowable.__init__(self)
        self.lines = "\\\\".join(equationLines)
        self.num = get_equation_count()
        call(["pnglatex/pnglatex", "-f", self.lines, "-o", ".hermes/%d.png" % self.num])
        self.image = Image(".hermes/%d.png" % self.num)

    def draw(self):
        lines = "<br />".join(self.lines)
        p = Paragraph(lines, equationStyle)
        p.wrap(450, 0)
        p.drawOn(self.canv, 0, 0)