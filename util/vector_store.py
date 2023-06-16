import faiss
import numpy as np

from util.generate_embedding import generate_embedding


class VectorStore:
    def __init__(self):
        self.documents = []
        self.embeddings = None

    def add_to_store(self, document):
        self.documents.append(document)
        response = generate_embedding(document.content)
        if self.embeddings is None:
            self.embeddings = np.array([response])
        else:
            self.embeddings = np.vstack((self.embeddings, response))

    def create_index(self):
        index = faiss.IndexFlatL2(self.embeddings.shape[1])
        index.add(self.embeddings)
        return index
