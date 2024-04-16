class My_Base_exception(Exception):
    def __init__(self):
        raise NotImplementedError()

class Duplicate_id(My_Base_exception):
    def __init__(self, id, file1, type1, file2, type2):
        self.id=id
        self.file1=file1
        self.type1=type1
        self.file2=file2
        self.type2=type2

    def __str__(self) -> str:
        return f"{self.id} is defined in {self.file1}/{self.type1} and {self.file2}/{self.type2}"
    
    
class No_id(My_Base_exception):
    def __init__(self, file, type, json):
        self.file=file
        self.type=type
        self.json=json