import os
from langchain.tools import tool
from data_models.models import RagToolSchema
from utils.model_loader import ModelLoader
from utils.config_loader import load_config
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

load_dotenv()
model_loader=ModelLoader()
config = load_config()

@tool(args_schema=RagToolSchema)
def retriever_node(question):
    """This is tool acts as a person who is an expert knowledge on climate/weather pattern
    Use this tool answer questions about weather history, climate patterns, environmental 
    and geographical changes, monsoon pattern or climate history of particular place or country 
    """
    index_name = config["vector_db"]["index_name"]
    embedding_model = model_loader.load_embeddings()
    qdrant_client = QdrantClient(
        url="https://c025c1b0-d18c-455d-b338-2158a6ce5708.us-east4-0.gcp.cloud.qdrant.io:6333", 
        api_key=os.getenv("QDRANT_API_KEY")
        )
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=index_name,
        embedding=embedding_model,
    )
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": config["retriever"]["top_k"] , "score_threshold": config["retriever"]["score_threshold"]},
    )
    retriever_result=retriever.invoke(question)
    
    return retriever_result