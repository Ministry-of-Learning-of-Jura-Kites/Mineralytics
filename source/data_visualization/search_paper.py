import faiss
import numpy as np
from data_visualization.get_data import get_embeddings, get_model


def search(prompt: str):
    embeddings = get_embeddings()
    model = get_model()

    embeddings_np = embeddings.cpu().detach().numpy()

    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean) index
    index.add(embeddings_np)  # Add embeddings to the index

    query_embedding = (
        model.encode(prompt, convert_to_tensor=True).cpu().detach().numpy()
    )

    k = 5
    distances, indices = index.search(np.array([query_embedding]), k)

    return indices
