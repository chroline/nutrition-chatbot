class Document:
    def __init__(self, title="", url="", content=""):
        self.title = title
        self.url = url
        self.content = content

    def __str__(self):
        return self.content.strip()

    def __repr__(self):
        return self.__str__()
