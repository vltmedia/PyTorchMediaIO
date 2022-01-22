import os
import json


class Extensions():
    def __init__(self):
        self.extensions = self.LoadExtensions()

    def GetMediaType(self, inputFile):
        found = False
        ext = os.path.splitext(inputFile)[1].upper()
        mediaType = ("Raster image", ext)
        for key in self.extensions.keys():
            if not found:
                if ext in self.extensions[key]:
                    found = True
                    mediaType = (key,ext)
        return mediaType


    def LoadExtensions(self):
        file = open(os.path.join(os.path.dirname(__file__), "extensions.json"), 'r')
        data = file.read()
        file.close()
        extensions = json.loads(data)
        return extensions

    def Close(self):
        del self
