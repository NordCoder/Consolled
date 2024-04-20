class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.heirs = None

    def __str__(self):
        return f'{self.name}, {self.parent}, {self.heirs}'