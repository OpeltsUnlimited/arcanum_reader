from arcanum_root import Arcanum_root
from arcanum_objects import Arcanum_base
from my_html_file import My_html_file
from os import path, makedirs
import xml.etree.ElementTree as ElementTree
import html

class ToHtml:
    def __init__(self, output_folder, root_folder) -> None:
        self.root_folder = root_folder
        self.output_folder = output_folder

    def toHtml(self, arcanmum_data: Arcanum_root):
        if not path.exists(self.output_folder):
            makedirs(self.output_folder)
        self.createIndex(arcanmum_data)
        self.createErrorPage(arcanmum_data)
        for elemenmt in arcanmum_data.groups():
            self.subPages(arcanmum_data.getClassDict(elemenmt))

    def createIndex(self, arcanmum_data: Arcanum_root):
        index_file = My_html_file("index", self.output_folder)

        list = index_file.content.add("ul")
        list_element = list.add("li")

        link = list_element.add("a")
        link.attrib["href"]=f"{self.root_folder}/Error.html"
        link.text = "ERROR"

        for entry in arcanmum_data.groups():
            list_element = list.add("li")
            link = list_element.add("a")
            link.attrib["href"]=f"{self.root_folder}/{entry}.html"
            link.text = f"{entry}"

        index_file.write()

    def createErrorPage(self, arcanmum_data):
        index_file = My_html_file("Error", self.output_folder)

        list = index_file.content.add("ul")

        for entry in arcanmum_data.errors():
            list_element = list.add("li")
            list_element.text = entry

        index_file.write()


    def subPages(self, data: Arcanum_base):
        index_file = My_html_file(data.type, self.output_folder)

        table = index_file.content.add("table")
        table_head = table.add("tr")

        header = set()
        entris = data.entrys()
        for entry in entris:
            header = header.union(entris[entry].data.keys())
        header = list(header)
            
        for head in header:
            head_entry = table_head.add("th")
            head_entry.text = head

        for entry in entris:
            table_line = table.add("tr")

            for head in header:
                cell = table_line.add("td")
                if head in entris[entry].data:
                    dat = entris[entry].data[head]
                    cell.text = html.escape(str(dat), quote=False)

        index_file.write()
        