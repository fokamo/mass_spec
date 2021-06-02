"""info_section.py: for an InfoSection class

InfoSection class -- for storing repetitive informational pages
load_info_sections -- to load informational sections from a file
"""

class InfoSection():
    """A class to represent an informational page

    Attributes:
    title -- title of the page
    info -- list of informational paragraphs on the page
    source -- source of the page
    """
    
    def __init__(self, title: str, info: list, source: str) -> None:
        """Initialize an InfoSection.

        title -- title of the page
        info -- list of informational paragraphs on the page
        source -- source of the page
        """
        
        self.title = title 
        self.info = info
        self.source = "Source: " + source

def load_info_sections(filename: str) -> list:
    """Load data from a file into InfoSections.

    filename -- string with file path

    Returns a list of InfoSections
    """

    # return variable
    info_sections = []
    
    with open(filename, encoding='utf8') as file:
        
        for line in file.readlines():
            # remove excess whitespace
            line.strip()
            
            # different sections of data are separated by |
            data = line.split("|")
            
            title = data[0]
            # paragraphs are separated by ;;
            info = data[1].split(";;")
            sources = data[2]

            # create InfoSection based off data
            info_sections.append(InfoSection(title, info, sources))
            
    return info_sections
