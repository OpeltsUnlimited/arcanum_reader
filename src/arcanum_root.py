# Reads the raw json data from the data-directory, and transforms it into linked data

import json
from os import path
from arcanum_objects import *

class Arcanum_root:
    def __init__(self) -> None:
        self.__error = [] # when i encounter a pharese that seems to be a problem i put it here.
        self.__group = { # groups like classes, events, ... each one should be transformed to a page. (The game seems to call this modules)
            "tags": Arcanum_base("tags"),
            "resources": Arcanum_base("resources"),
            "upgrades": Arcanum_base("upgrades"),
            "tasks": Arcanum_base("tasks"),
            "homes": Arcanum_base("homes"),
            "furniture": Arcanum_base("furniture"),
            "skills": Arcanum_base("skills"),
            "states": Arcanum_base("states"),
            "player": Arcanum_base("player"),
            "spells": Arcanum_base("spells"),
            "monsters": Arcanum_base("monsters"),
            "dungeons": Arcanum_base("dungeons"),
            "events": Arcanum_base("events"),
            "classes": Arcanum_base("classes"),
            "armors": Arcanum_base("armors"),
            "weapons": Arcanum_base("weapons"),
            "materials": Arcanum_base("materials"),
            "enchants": Arcanum_base("enchants"),
            "sections": Arcanum_base("sections"),
            "potions": Arcanum_base("potions"),
            "encounters": Arcanum_base("encounters"),
            "locales": Arcanum_base("locales"),
            "stressors": Arcanum_base("stressors"),
            "rares": Arcanum_base("rares"),
            "reagents": Arcanum_base("reagents"),
            "properties": Arcanum_base("properties"),
            "potencies": Arcanum_base("potencies"),
            #"hall": Arcanum_base("hall"),
            "clashes": Arcanum_base("clashes"),
        }

    def groups(self):
        return self.__group.keys()
    
    def errors(self):
        return self.__error
    
    def getClassDict(self, type):
        if not type or not type in self.__group:
            return None
        return self.__group[type]

    def read(self, data_dir):
        with open(path.join(data_dir, "modules.json"), 'r') as file:
            last_run = json.load(file)
        for core in last_run["core"]:
            self.__read_core(path.join(data_dir, core+".json"), core);
        for modules in last_run["modules"]:
            self.__read_module(path.join(data_dir,"modules", modules+".json"));

    def __read_core(self, core_file, type):
        with open(core_file, 'r') as file:
            core_data = json.load(file)
            if not "module" in core_data:# hall data is different!!
                for element in core_data:
                    self.__process_json_element(core_file, type, element)
            else:
                modules_data = core_data["data"]
                for data in modules_data:
                    for element in modules_data[data]:
                        self.__process_json_element(core_file, type, element)
                        pass

    def __read_module(self, modules_file):
        with open(modules_file, 'r') as file:
            modules = json.load(file)
            modules_data = modules["data"]
            for data in modules_data:
                for element in modules_data[data]:
                    self.__process_json_element(modules_file, data, element)
                    pass

    def __process_json_element(self, file, type, json_object):
        group = self.getClassDict(type)
        #print(type, group)
        if group:
            group.addEntry(json_object, file, type)
        else:
            missingString = f"missing group \"{type}\" from {file}]"
            if not missingString in self.__error:
                self.__error.append(missingString)
        #print(element)


    