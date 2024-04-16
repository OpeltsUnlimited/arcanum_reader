from my_exception import Duplicate_id, No_id

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
            self.data[entry] = json[entry]

class Arcanum_base():
    def __init__(self, type):
        self.type = type
        self.__entry = {}

    def entrys(self):
        return self.__entry

    def addEntry(self, json, file, type):
        entry = Arcanum_entry(file, type, json)
        if not entry.id:
            raise No_id(entry.file, entry.type, json)
        if not entry.id in self.__entry:
            self.__entry[entry.id] = entry
        else:
            existing = self.__entry[entry.id]
            raise Duplicate_id(entry.id, entry.file, entry.type, existing.file, existing.type)