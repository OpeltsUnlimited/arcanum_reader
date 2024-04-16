import xml.etree.ElementTree as ElementTree
from os import path

class My_html_element(ElementTree.Element):
    def __init__(self, type):
        super().__init__(type)

    def add(self, type):
        newElement = My_html_element(type)
        self.append(newElement)
        return newElement

class My_html_file():
    def __init__(self, title, output_path, filename = None) -> None:
        self.title = title
        self.content = My_html_element("div")

        self.output_path = output_path
        self.filename = filename
        if not self.filename:
            self.filename = f"{title}.html"

        self.meta = [] 

    def addMeta(self):
        newElement = My_html_element("meta")
        self.meta.append(newElement)
        return newElement

    def write(self):
        with open("template.html") as template_file:
            template = template_file.read()

        meta_data = ""
        for meta in self.meta:
            meta_data +=  ElementTree.tostring(meta, encoding='unicode')
            
        output = template.replace("{{ Meta }}", meta_data)
        output = output.replace("{{ Title }}", self.title)
        output = output.replace("{{ Content }}", ElementTree.tostring(self.content, encoding='unicode'))

        with open(path.join(self.output_path, self.filename),'w') as file:
            file.write(output)
