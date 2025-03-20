# File: backend/rag/processor.py
import logging
import sys
from typing import Dict, Any, List
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from app.config import settings
import os

# Fix for Python 3.8 compatibility with type annotations
if sys.version_info < (3, 9):
    import typing
    typing.Dict = Dict
    typing.Any = Any
    typing.List = List

logger = logging.getLogger(__name__)

class RAGProcessor:
    def __init__(self):
        logger.info("Initializing RAG Processor...")
        try:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=settings.OPENAI_API_KEY
            )
            
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len,
            )
            
            # Make sure the vector store directory exists
            os.makedirs(settings.VECTOR_STORE_PATH, exist_ok=True)
            
            # Initialize vector store
            self.vector_store = Chroma(
                persist_directory=settings.VECTOR_STORE_PATH,
                embedding_function=self.embeddings
            )
            
            logger.info("RAG Processor initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG Processor: {str(e)}")
            raise

    def process_lecture(self, lecture_id: int, content: str) -> None:
        """Process lecture content and store in vector store"""
        try:
            # Split text into chunks
            chunks = self.text_splitter.split_text(content)
            
            # Prepare documents
            metadatas = [{
                "lecture_id": lecture_id,
                "chunk_id": i,
                "source": f"lecture_{lecture_id}"
            } for i in range(len(chunks))]
            
            # Add to vector store
            self.vector_store.add_texts(
                texts=chunks,
                metadatas=metadatas
            )
            
            # Persist changes
            self.vector_store.persist()
            
            logger.info(f"Successfully processed lecture {lecture_id} with {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Error processing lecture: {str(e)}")
            raise

    async def find_relevant_context(self, question: str, num_chunks: int = 3):
        """Find relevant context for a question"""
        try:
            # Check if there's any data in the vector store
            collection = self.vector_store._collection
            if collection.count() == 0:
                logger.warning("Vector store is empty - no lectures loaded")
                return []
                
            # Perform similarity search
            results = self.vector_store.similarity_search(
                question,
                k=num_chunks
            )
            
            # Format results
            context_docs = [{
                "content": doc.page_content,
                "metadata": doc.metadata
            } for doc in results]
            
            logger.info(f"Found {len(context_docs)} relevant chunks for question")
            return context_docs
            
        except Exception as e:
            logger.error(f"Error finding relevant context: {str(e)}")
            raise