""" info_section.py: for an InfoSection class """

class InfoSection():
    """ InfoScection class for tidy storage of each page's text """
    
    def __init__(self, title: str, info: list, sources: list):
        self.title = title 
        self.info = info
        self.sources = sources

def load_info_sections(filename: str):
    """ Loads data from a file into InfoSections """
    
    info_sections = []
    
    with open(filename) as file:
        lines = file.readlines()
        
        for line in lines:
            # different sections of data are separated by |
            data = line.split("|")
            
            title = data[0]
            # paragraphs are separated by ;;
            info = data[1].split(";;")
            sources = data[2].split(";;")
            
            info_sections.append(InfoSection(title, info, sources))
            
    return info_sections
