import os

import numpy as np
from sentence_transformers import SentenceTransformer

current_dir = os.path.dirname(os.path.abspath(__file__))
path_name = "../../util/model/multi-qa-MiniLM-L6-cos-v1"
absolute_path = os.path.join(current_dir, path_name)

model = SentenceTransformer(absolute_path, device="cpu")

os.environ['TOKENIZERS_PARALLELISM'] = 'true'


def generate_embedding(text):
    response = model.encode([text])
    return np.array(response[0])
