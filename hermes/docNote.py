import docDefault

class docNote(docDefault.docDefault):
    def __init__(self, config):
        super().__init__(config)
        print("Loading the note template")