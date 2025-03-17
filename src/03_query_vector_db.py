from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer


def perform_search(client, embedder, collection_name, query_text, limit=3) -> list:
    vector = embedder.encode(query_text).tolist()
    return client.query_points(
        collection_name=collection_name,
        query=vector,
        with_payload=True,
        limit=limit,
    )


def print_search_results(search_results):
    print("Search Results:")
    for result in search_results.points:
        print(f"  - ID: {result.id}, Score: {result.score}")
        print(f"    - Page ID: {result.payload['page_id']}")
        print(f"    - Title: {result.payload['title']}")
        print(f"    - URL: {result.payload['url']}")



if __name__ == '__main__':
    client = QdrantClient(path="../data/qdrant")
    embedder = SentenceTransformer("all-mpnet-base-v2")
    collection_name = "confluence_pages"
    query_text = "How llm works?"

    search_results = perform_search(client, embedder, collection_name, query_text)
    print_search_results(search_results)
