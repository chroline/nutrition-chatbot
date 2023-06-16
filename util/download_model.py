import os

from sentence_transformers import SentenceTransformer

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, "model/multi-qa-MiniLM-L6-cos-v1")

if __name__ == "__main__":
    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
    model.save(model_path)
