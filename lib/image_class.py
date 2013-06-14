class Image :
    def __init__(self) :
        self.name = ""
        self.file = ""
        self.description = ""

    def setName(self, name) :
        self.name = name

    def setFile(self, fileName) :
        self.file = fileName

    def setDescription(self, desc) :
        self.description = desc

    def setImage(self, name = "", fileName = "", desc = "") :
        self.name = name
        self.file = fileName
        self.description = desc

    def getName(self) :
        return self.name

    def getFile(self) :
        return self.file

    def getDescription(self) :
        return self.description
