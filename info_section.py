""" info_section.py: for an InfoSection class """

class InfoSection():
    def __init__(self, title: str, info: list, sources: list):
        self.title = title 
        self.info = info
        self.sources = sources

def load_info_sections(filename: str):
    info_sections = []
    with open(filename) as file:
        lines = file.readlines()
        for line in lines:
            data = line.split(";")
            title = data[0]
            info = data[1].split(",")
            sources = data[2].split(",")
            info_sections.append(InfoSection(title, info, sources))
    return info_sections
