# Atlassian Bot Proofs of Concept

## Overview
This repository contains a proof of concept of chatbot that is using data from Atlassian Confluence and JIRa.
Idea of the bot is to provide information about the project, team, sprint, etc.

## Scripts

### `01_dump_data.py`

This script is used to dump data from Atlassian Confluence and JIRA to the local file system.
It retrieves data from Confluence pages based on a specified label and saves it as JSON files.
It uses the `atlassian-python-api` library to interact with the Confluence API.
The script requires environment variables for Confluence access, including base URL, username, and access token.

### `02_feed_vector_db.py`

This script reads Confluence page data stored as JSON files, splits the text content into smaller chunks, and stores the resulting data in a Qdrant vector database.
It leverages `sentence-transformers` to create embeddings for these text chunks and associates them with relevant metadata in the database.
The script initializes a Qdrant client, processes the content of each Confluence page, and inserts or updates the data in the specified collection within the Qdrant database.

### `03_query_vector_db.py`

This script queries the Qdrant vector database to retrieve relevant information based on a query text.
It uses `sentence-transformers` to encode the query text into a vector and performs a search in the Qdrant database.
The script prints the search results, including the ID, score, page ID, title, chunk text, and URL of the retrieved entries.

### `04_rag_llm_gemini.py`

This script integrates a Retrieval-Augmented Generation (RAG) approach with a Large Language Model (LLM), specifically leveraging the data stored in the Qdrant vector database. The Gemini model is used for natural
language understanding and generation.

The script performs the following steps:

1. Encodes user queries using `sentence-transformers` to create query embeddings.
2. Searches the Qdrant vector database to retrieve the most relevant documents based on the query embedding.
3. Combines the retrieved document data as context and inputs it into the Gemini LLM to generate a response.
4. Presents the final response to the user, augmented with the retrieved information.

Key features:

- Demonstrates how to perform RAG with vector database-backed retrieval.
- Uses real project-related data to generate insightful responses.
- Showcases integrating multiple technologies (Qdrant and Gemini LLM) to create a basic retrieval-driven chatbot.

## Assumptions
* This project is purely a proof of concept and is not intended to be used in production.
* I'm not Python developer, and using this technology only for early prototyping. Don't expect production grade code quality, extensive testing, or sticking to best practices.
* This project is not intended to be a full-featured chatbot. It's a simple prototype that demonstrates how to integrate with Atlassian APIs.
* Expect some parameters to be hardcoded.