class arcanum_json():
    def __init__(self, json):
        self.json = json

    def __str__(self) -> str:
        return str(self.json)
    
class arcanum_lines():
    def __init__(self):
        self.lines = []

    def addLine(self, line):
        self.lines.append(line)

class arcanum_text():
    def __init__(self, text, bold = False):
        self.text = text
        self.bold = bold

class arcanum_TEST():
    def __init__(self, json):
        self.json = json
        print(json)

class arcanum_compound():
    def __init__(self, json):
        self.json = json
        print(type(json), json)