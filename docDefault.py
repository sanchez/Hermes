from reportlab.pdfgen import canvas

class Handler:
    def __init__(self, destName):
        self.c = canvas.Canvas(destName, bottomup=0)
        self.c.setAuthor("Hermes (Daniel Fitz)")
        self.c.setTitle(destName)
        self.c.setFont('Helvetica', 12)

    def save(self):
        self.c.save()

    def add_heading(self, title, depth, options):
        self.c.drawString(20, 20, title)