import numpy as np

from bot.data import dump, faiss_index
from store_generator.generate_embedding import generate_embedding


def retrieve_related_docs(query, k=3):
    query_embedding = generate_embedding(query)
    distances, indexes = faiss_index.search(np.expand_dims(query_embedding, axis=0), k)

    filtered_indexes = []
    for distance, index in zip(distances[0], indexes[0]):
        if distance < 1:
            filtered_indexes.append(index)

    return [(idx, dump[idx]) for idx in filtered_indexes]
