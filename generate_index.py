import os
import pickle

import faiss

from util.scraper_utils import get_all_links, scrape_webpage
from util.vector_store import VectorStore

current_dir = os.path.dirname(os.path.abspath(__file__))

store = VectorStore()
processed_links = []


def generate_index():
    for index in range(1, 2):
        print(f"Processing page {index}...")
        links = get_all_links(index)
        for link in links:
            if link in processed_links:
                continue
            else:
                processed_links.append(link)
                print(f"- Processing {link}...")
                docs = scrape_webpage(link)
                if len(docs) > 0:
                    for doc in docs:
                        store.add_to_store(doc)
                else:
                    print("  ERROR")

    print(f"# links processed: {len(processed_links)}")
    print(f"# docs: {len(store.documents)}")

    print("Storing FAISS index...")
    faiss.write_index(store.create_index(), 'index.faiss')
    print("Creating pkl dump...")
    with open('dump.pkl', "wb") as file:
        pickle.dump(store.documents, file)
        file.close()


if __name__ == "__main__":
    generate_index()
