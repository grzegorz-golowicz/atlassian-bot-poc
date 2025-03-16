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

This script processes Confluence page data stored as JSON files, chunks the text content, and feeds it into a Qdrant vector database.
It utilizes `sentence-transformers` to generate embeddings for text chunks and stores them in the Qdrant database along with metadata.
The script initializes a Qdrant client, loads Confluence pages, chunks the content of each page, and upserts the data into the specified collection.

### `03_query_vector_db.py`

This script queries the Qdrant vector database to retrieve relevant information based on a query text.
It uses `sentence-transformers` to encode the query text into a vector and performs a search in the Qdrant database.
The script prints the search results, including the ID, score, page ID, title, chunk text, and URL of the retrieved entries.

## Assumptions
* This project is purely a proof of concept and is not intended to be used in production.
* I'm not Python developer, and using this technology only for early prototyping. Don't expect production grade code quality, extensive testing, or sticking to best practices.
* This project is not intended to be a full-featured chatbot. It's a simple prototype that demonstrates how to integrate with Atlassian APIs.
* Expect some parameters to be hardcoded.