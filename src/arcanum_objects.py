from my_exception import Duplicate_id, No_id
from arcanum_entrys import *

class Arcanum_entry():
    def __init__(self, type, file, json):
        self.type = type
        self.file = file
        self.data={}
        try:
            self.id = json["id"]
        except TypeError:
            print("unexpected error in file", file, type)
        
        for entry in json:
            self.data[entry] = arcanum_json(json[entry])
class Arcanum_base():
    def __init__(self, type):
        self.type = type
        self.__entry = {}
        self.expectedHeaders = None

    def addEntry(self, json, file, type):
        entry = Arcanum_entry(file, type, json)
        if not entry.id:
            raise No_id(entry.file, entry.type, json)
        if not entry.id in self.__entry:
            self.__entry[entry.id] = entry
        else:
            existing = self.__entry[entry.id]
            raise Duplicate_id(entry.id, entry.file, entry.type, existing.file, existing.type)
        
    def process_entrys(self, root):
        if self.expectedHeaders:
            header = self.__getHeaderSet()
            expected = set(self.expectedHeaders)

            missing = expected - header
            if missing:
                for mis in missing:
                    errString = f"missing head \"{mis}\" in {self.type}]"
                    root.addError(errString)
            unexpected = header - expected
            if unexpected:
                for un in unexpected:
                    errString = f"unexpected head \"{un}\" in {self.type}]"
                    root.addError(errString)

    def __getHeaderSet(self):
        header = set()
        entris = self.__entry
        for entry in entris:
            header = header.union(entris[entry].data.keys())
        return header
        
    def getHeaderList(self):
        header = list(self.__getHeaderSet())
        header = sorted(header)
        return header
    
    def keys(self):
        return self.__entry.keys()

    def data(self, key, head):
        if key in self.__entry:
            element = self.__entry[key]
        else:
            return None
        if head in element.data:
            return element.data[head]
        
class Arcanum_skills(Arcanum_base):
    def __init__(self, type):
        super().__init__(type)
        self.expectedHeaders = ['result', 'effect', 'mod', 'run', 'alias', 'require', 'need', 'buy', 'id', 'verb', 'school', 'tags', 'name', 'level', 'flavor', 'locked', 'desc']

    def process_entrys(self, root):
        super().process_entrys(root)
        for key, entry in self._Arcanum_base__entry.items():
            if not "name" in entry.data:
                entry.data["name"] = entry.data["id"]

            name_column = arcanum_lines()
            name_column.addLine(arcanum_text(entry.data["name"].json, True))
            if "desc" in entry.data:
                name_column.addLine(arcanum_text(entry.data["desc"].json))
            if "flavor" in entry.data:
                name_column.addLine(arcanum_text(entry.data["flavor"].json))
            entry.data["name"] = name_column

            name_column = arcanum_lines()
            if "need" in entry.data:
                name_column.addLine(arcanum_json(entry.data["need"].json))
            if "require" in entry.data:
                name_column.addLine(arcanum_text(entry.data["require"].json))
            if "level" in entry.data:
                name_column.addLine(arcanum_text("level: "+str(entry.data["level"].json)))
            entry.data["require"] = name_column
            
            name_column = arcanum_lines()
            if "result" in entry.data:
                name_column.addLine(arcanum_json(entry.data["result"].json))
                pass
            if "effect" in entry.data:
                name_column.addLine(arcanum_json(entry.data["effect"].json))
                pass
            if "mod" in entry.data:
                name_column.addLine(arcanum_json(entry.data["mod"].json))
                pass
            entry.data["result"] = name_column

    def getHeaderList(self):
        # 'alias', 'verb', 'id', 'locked', 'school', 'tags'
        return ['name', 'require', 'result', 'run',  'buy']