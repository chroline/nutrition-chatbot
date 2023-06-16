from pickle import Unpickler

import faiss

faiss_index = faiss.read_index("index.faiss")


class CustomUnpickler(Unpickler):
    def find_class(self, module, name):
        if name == 'Document':
            from util.document import Document
            return Document
        return super().find_class(module, name)


with open("dump.pkl", 'rb') as file:
    dump = CustomUnpickler(file).load()
    file.close()
