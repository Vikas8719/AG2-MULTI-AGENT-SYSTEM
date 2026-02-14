
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import json

class VectorDB:
    """
    Vector Database Manager using ChromaDB for Agent Memory context.
    Stores and retrieves semantic information to help agents maintain context.
    """
    

    def __init__(self, persist_directory: str = "chroma_db", collection_name: str = "agent_memory"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.logger = logging.getLogger("vector_db")
        
        # Ensure directory exists
        Path(persist_directory).mkdir(parents=True, exist_ok=True)
        
        self.client = None
        self.collection = None
        self.embedding_fn = None

    def _init_db(self):
        """Lazy initialization of ChromaDB client to avoid threading issues"""
        if self.client is None:
             # Initialize Client
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            # Initialize Embedding Function (using default all-MiniLM-L6-v2)
            self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            
            # Get or Create Collection
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_fn
            )
            self.logger.info(f"VectorDB initialized at {self.persist_directory} with collection '{self.collection_name}'")

    def add_memory(self, text: str, metadata: Dict[str, Any], memory_id: str):

        """
        Add a text chunk to the vector database.
        
        Args:
            text: The text content to store (e.g. agent thought, code snippet, requirement)
            metadata: Additional info (e.g. agent_name, step, timestamp)
            memory_id: Unique ID for this memory item
        """
        try:
            self._init_db()
            self.collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[memory_id]
            )
            self.logger.info(f"Added memory ID: {memory_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add memory: {str(e)}")
            return False

    def query_memory(self, query_text: str, n_results: int = 5, filter_metadata: Optional[Dict] = None) -> List[Dict]:
        """
        Search for semantically similar memories.
        
        Args:
            query_text: The query string
            n_results: Number of results to return
            filter_metadata: Optional filter for metadata (e.g. {'agent': 'coder'})
            

        Returns:
            List of dictionaries containing document and metadata
        """
        try:
            self._init_db()
            results = self.collection.query(
                query_texts=[query_text],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'text': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'id': results['ids'][0][i],
                        'distance': results['distances'][0][i] if results['distances'] else None
                    })
            
            return formatted_results
            
        except Exception as e:
            self.logger.error(f"Failed to query memory: {str(e)}")
            return []


    def get_all_memories(self) -> List[Dict]:
        """Retrieve all stored memories (limit to first 100 for UI display)."""
        try:
            self._init_db()
            # Providing a dummy embedding or just getting based on basic get
            result = self.collection.get(limit=100)
            
            memories = []
            if result['documents']:
                for i in range(len(result['documents'])):
                    memories.append({
                        'id': result['ids'][i],
                        'text': result['documents'][i],
                        'metadata': result['metadatas'][i]
                    })
            return memories
        except Exception as e:
            self.logger.error(f"Failed to retrieve all memories: {str(e)}")
            return []


    def clear_memory(self):
        """Clear all memories from the collection."""
        try:
            self._init_db()
            self.client.delete_collection(self.collection_name)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_fn
            )
            self.logger.info("Memory cleared successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to clear memory: {str(e)}")
            return False
