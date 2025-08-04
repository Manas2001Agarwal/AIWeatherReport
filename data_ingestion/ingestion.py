import os
import sys
import tempfile
from uuid import uuid4
from typing import List
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from exception.exceptions import WeatherReportException

class DataIngestion:
    """
    Class to handle document loading, transformation and ingestion into QDrant vector store.
    """

    def __init__(self):
        try:
            print("Initializing DataIngestion pipeline...")
            self.model_loader = ModelLoader()
            self._load_env_variables()
            self.config = load_config()
        except Exception as e:
            raise WeatherReportException(e, sys)

    def _load_env_variables(self):
        try:
            load_dotenv()

            required_vars = [
                "GOOGLE_API_KEY",
                "QDRANT_API_KEY"
            ]

            missing_vars = [var for var in required_vars if os.getenv(var) is None]
            if missing_vars:
                raise EnvironmentError(f"Missing environment variables: {missing_vars}")

            self.google_api_key = os.getenv("GOOGLE_API_KEY")
            self.qdrant_api_key = os.getenv("QDRANT_API_KEY")
        except Exception as e:
            raise WeatherReportException(e, sys)

    def load_documents(self, uploaded_files) -> List[Document]:
        try:
            documents = []
            for uploaded_file in uploaded_files:
                file_ext = os.path.splitext(uploaded_file.filename)[1].lower()
                suffix = file_ext if file_ext in [".pdf", ".docx"] else ".tmp"

                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                    temp_file.write(uploaded_file.file.read())
                    temp_path = temp_file.name

                if file_ext == ".pdf":
                    loader = PyPDFLoader(temp_path)
                    documents.extend(loader.load())
                elif file_ext == ".docx":
                    loader = Docx2txtLoader(temp_path)
                    documents.extend(loader.load())
                else:
                    print(f"Unsupported file type: {uploaded_file.filename}")
            return documents
        except Exception as e:
            raise WeatherReportException(e, sys)

    def store_in_vector_db(self, documents: List[Document]):
        try:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                length_function=len
            )
            documents = text_splitter.split_documents(documents)

            qdrant_client = QdrantClient(
                url="https://c025c1b0-d18c-455d-b338-2158a6ce5708.us-east4-0.gcp.cloud.qdrant.io:6333", 
                api_key=self.qdrant_api_key
                )
            index_name = self.config["vector_db"]["index_name"]

            if not qdrant_client.collection_exists(collection_name=index_name):
                
                qdrant_client.create_collection(
                    collection_name=index_name,
                    vectors_config=VectorParams(size=100, distance=Distance.COSINE)
                    )

            vector_store = QdrantVectorStore(
                client=qdrant_client,
                collection_name=index_name,
                embedding=self.model_loader.load_embeddings()
                )
            uuids = [str(uuid4()) for _ in range(len(documents))]
            vector_store.add_documents(documents=documents, ids=uuids)
        except Exception as e:
            raise WeatherReportException(e, sys)

    def run_pipeline(self, uploaded_files):
        try:
            documents = self.load_documents(uploaded_files)
            if not documents:
                print("No valid documents found.")
                return
            self.store_in_vector_db(documents)
        except Exception as e:
            raise WeatherReportException(e, sys)

if __name__ == '__main__':
    pass