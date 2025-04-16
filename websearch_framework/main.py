from Function import *

urls, descriptions = load_lists_from_files("all_urls.txt", "all_descriptions.txt")

loaded_index = load_index(index_path="my_faiss.index")

query = "What is the best way to charge a battery?"

retrieved_texts = retrieve_relevant_texts(query, loaded_index, urls, threshold=0.7, top_k=10, texts_folder="website_texts")
