import json
import uuid
from glob import glob

from langchain_text_splitters import CharacterTextSplitter
from qdrant_client import QdrantClient, models
from qdrant_client.http import models as rest
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer

from model.ConfluencePageData import ConfluencePageData


def load_pages() -> list[ConfluencePageData]:
    pages_files = glob("../data/confluence/*.json")
    return [
        ConfluencePageData(**json.load(open(page_file, 'r')))
        for page_file in pages_files
    ]


def chunk_text(text, chunk_size=300, overlap=50):
    """
    Chunks a long text into smaller overlapping segments using LangChain's CharacterTextSplitter.
    """
    return CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap).split_text(text)


def initialize_qdrant_client(client, collection_name, vector_size):
    if not client.collection_exists(collection_name):
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )


def create_point(chunk, page, embedder):
    return PointStruct(
        id=str(uuid.uuid4()),
        vector=embedder.encode(chunk).tolist(),
        payload={
            "page_id": page.id,
            "space": page.space,
            "title": page.title,
            "chunk_text": chunk,
            "url": page.url,
            "last_updated": page.last_updated,
        },
    )


def main():
    client = QdrantClient(path="../data/qdrant")
    embedder = SentenceTransformer("all-mpnet-base-v2")

    collection_name = "confluence_pages"
    vector_size = 768  # Adjust based on the model used (e.g., 768 for Sentence Transformers)

    initialize_qdrant_client(client, collection_name, vector_size)

    pages = load_pages()
    print(f'Loaded {len(pages)} pages')

    points = [
        create_point(chunk, page, embedder)
        for page in pages
        for chunk in chunk_text(page.contents)
    ]

    client.upsert(
        collection_name=collection_name,
        points=points,
        wait=True,
    )

    client.create_payload_index(
        collection_name=collection_name,
        field_name="chunk_text",
        field_schema=rest.PayloadSchemaType.TEXT,
    )


if __name__ == "__main__":
    main()
