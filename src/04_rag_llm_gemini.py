import json
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

from model.ConfluencePageData import ConfluencePageData

load_dotenv()


def perform_search(client: QdrantClient, embedder: SentenceTransformer, collection_name: str, query_text: str, limit: int = 3) -> list:
    query_vector = embedder.encode(query_text).tolist()
    return client.query_points(
        collection_name=collection_name,
        query=query_vector,
        with_payload=True,
        limit=limit,
    )


def load_pages(page_ids: list, pages_dir: str = "../data/confluence") -> list:
    pages = []
    for page_id in page_ids:
        file_path = os.path.join(pages_dir, f"{page_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                page_data = json.load(file)
                pages.append(ConfluencePageData(**page_data))
    return pages


def pages_to_llm_context(pages: list) -> str:
    return "\n".join(
        f"---Confluence page---\n"
        f"Title: {page.title}\n"
        f"URL: {page.url}\n"
        f"Last Updated: {page.last_updated}\n"
        f"Contents: {page.contents}\n"
        for page in pages
    )


def llm_query(client: genai.Client, query_text: str) -> str:
    model_name = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=query_text)]
        )
    ]
    config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
    )
    response = client.models.generate_content(model=model_name, contents=contents, config=config)
    return response.text


def generate_llm_query(pages: list, question: str) -> str:
    context = pages_to_llm_context(pages)
    return f"Question: {question}\n\nContext: {context}"


if __name__ == "__main__":
    qdrant_client = QdrantClient(path="../data/qdrant")
    llm_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    embedder = SentenceTransformer("all-mpnet-base-v2")
    collection_name = "confluence_pages"

    question = input("Question: ")

    search_results = perform_search(qdrant_client, embedder, collection_name, question)
    page_ids = [result.payload['page_id'] for result in search_results.points]
    pages = load_pages(page_ids)
    query = generate_llm_query(pages, question)

    llm_answer = llm_query(llm_client, query)

    print("LLM Answer:")
    print(llm_answer)
    print("\nPages used for context:")
    for page in pages:
        print(f"  - {page.title} ({page.url})")
