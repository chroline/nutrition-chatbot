import os

import numpy as np
from sentence_transformers import SentenceTransformer

path_name = "util/model/multi-qa-MiniLM-L6-cos-v1"
absolute_path = os.path.abspath(path_name)
normalized_path = os.path.normpath(absolute_path)

model = SentenceTransformer('util/model/multi-qa-MiniLM-L6-cos-v1', device="cpu")

os.environ['TOKENIZERS_PARALLELISM'] = 'true'


def generate_embedding(text):
    response = model.encode([text])
    return np.array(response[0])
