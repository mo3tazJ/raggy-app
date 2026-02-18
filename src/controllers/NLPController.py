from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import List
import json
import logging


class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, embedding_client):
        super().__init__()
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client
        self.logger = logging.getLogger(__name__)

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vectordb_collection(self, project: Project):
        collection_name = self.create_collection_name(
            project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vectordb_collection_info(self, project: Project):
        collection_name = self.create_collection_name(
            project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(
            collection_name=collection_name)
        collection_info_serialized = json.loads(json.dumps(
            collection_info, default=lambda x: x.__dict__))
        return collection_info_serialized

    def index_into_vectordb(self, project: Project, chunks: List[DataChunk], chunks_ids: List[int], do_reset: bool = False):

        # Get collection name
        collection_name = self.create_collection_name(
            project_id=project.project_id)

        # Manage chunks items
        texts = [
            c.chunk_text
            for c in chunks
        ]
        metadata = [
            c.chunk_metadata
            for c in chunks
        ]
        vectors = [
            self.embedding_client.embed_text(
                text=text, document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]

        # Check if any embedding failed
        # if any(v is None for v in vectors):
        #     self.logger.error("Failed to generate embeddings for some chunks")
        #     return False

        # Create collection
        self.vectordb_client.create_collection(
            collection_name=collection_name, embedding_size=self.embedding_client.embedding_size, do_reset=do_reset)

        # Insert into vector db
        _ = self.vectordb_client.insert_many(
            collection_name=collection_name, texts=texts, vectors=vectors, metadata=metadata, record_ids=chunks_ids)

        return True

    def search_vectordb_collection(self, project: Project, text: str, limit: int = 5):
        # Get collection name
        collection_name = self.create_collection_name(
            project_id=project.project_id)
        # embed the text
        vector = self.embedding_client.embed_text(
            text=text, document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            self.logger.error("failed to embed the query text for search")
            return False

        # Search in vectordb (semantic search)
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name, vector=vector, limit=limit)

        if not results:
            self.logger.error("No results found in victordb search")
            return False

        return results
