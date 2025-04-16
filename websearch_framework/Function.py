import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

def store_data(chunks):
    # Get the directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))

    folder_path = os.path.join(current_dir, 'battery_ppt')

    # Load pre-trained sentence vector model (MiniLM example)
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    # Calculate vector representation for each text chunk
    embeddings = model.encode(chunks)  # shape: (num_chunks, 384)
    embeddings = np.array(embeddings, dtype="float32")

    # Create index object, build FAISS index (using cosine similarity, normalize vectors first and then use inner product for retrieval)
    vec_dim = embeddings.shape[1]  # Vector dimension, e.g., all-MiniLM-L6-v2 is 384
    index = faiss.IndexFlatIP(vec_dim)
    # For cosine similarity, vectors need to be L2 normalized first
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    # Store the index to disk
    faiss.write_index(index, "my_faiss.index")
    
    return index

def load_lists_from_files(urls_file_path, descriptions_file_path):
  """Load URL and description lists from files
  
  Args:
      urls_file_path: URL file path
      descriptions_file_path: Description file path
      
  Returns:
      urls: List of URLs
      descriptions: List of descriptions
  """
  # Load URL list
  with open(urls_file_path, 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]
  
  # Load description list
  with open(descriptions_file_path, 'r', encoding='utf-8') as f:
    content = f.read()
    descriptions = content.split("---ITEM_SEPARATOR---\n")
    # Remove the last empty element (if exists)
    if descriptions and not descriptions[-1].strip():
      descriptions.pop()
    # Remove newline characters at the end of each description
    descriptions = [desc.strip() for desc in descriptions]
  
  return urls, descriptions

def load_index(index_path="my_faiss.index"):
    """Load FAISS index from disk
    
    Args:
        index_path: FAISS index file path
        
    Returns:
        index: Loaded FAISS index object
    """
    try:
        # Check if index file exists
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"Index file {index_path} does not exist")
            
        # Read index from disk
        index = faiss.read_index(index_path)
        print(f"Successfully loaded index with {index.ntotal} vectors")
        return index
    except Exception as e:
        print(f"Failed to load index: {e}")
        return None
    
def search_with_loaded_index(query, loaded_index, urls, top_k=10):
    """Search using loaded index
    
    Args:
        query: Query text
        loaded_index: Pre-loaded FAISS index
        urls: URL list, corresponding one-to-one with vectors in the index
        top_k: Number of most relevant results to return
        
    Returns:
        search_results: Search results list containing URLs and similarity scores
    """
    # Load model (must be the same model used when creating the index)
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    # Encode query text
    query_vector = model.encode([query])
    query_vector = np.array(query_vector, dtype="float32")
    
    # Normalize query vector
    faiss.normalize_L2(query_vector)
    
    # Execute search
    scores, indices = loaded_index.search(query_vector, top_k)
    
    # Organize search results
    search_results = []
    for i in range(len(indices[0])):
        if indices[0][i] != -1:  # Valid index
            search_results.append({
                'url': urls[indices[0][i]],
                'score': float(scores[0][i])
            })
    
    # return corresponding urls and scores
    return search_results

def retrieve_relevant_texts(query, loaded_index, urls, threshold=0.7, top_k=20, texts_folder="website_texts"):
    """
    Search for relevant URLs, filter results above threshold, and read corresponding text files
    
    Args:
        query: Query text
        loaded_index: Pre-loaded FAISS index
        urls: URL list, corresponding one-to-one with vectors in the index
        threshold: Similarity threshold, only return results with scores above this value
        top_k: Number of initial search results to return
        texts_folder: Folder path storing text files
        
    Returns:
        combined_text: String containing all concatenated relevant texts
    """
    # Get search results
    search_results = search_with_loaded_index(query, loaded_index, urls, top_k)
    
    # Filter results above threshold
    filtered_results = [result for result in search_results if result['score'] > threshold]
    
    # Read and concatenate texts, iterate from the first result
    combined_text = ""
    for result in filtered_results:
        url = result['url']
        file_path = os.path.join(texts_folder, f"{url}.txt")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
                combined_text += text_content + "\n\n"
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    return combined_text