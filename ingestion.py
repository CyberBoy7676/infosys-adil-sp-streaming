from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_pinecone import PineconeVectorStore
from langchain_huggingface import HuggingFaceEmbeddings
import os
# import pinecone
# Load environment variables
load_dotenv()

# Initialize Pinecone with the API key and environment
# pinecone.init(api_key=os.getenv("PINECONE_API_KEY"))

if __name__ == "__main__":

    # 1. Loading Documents
    loader = TextLoader("delhi_data.txt", encoding="utf-8") # add path to the file you want to ingest
    document = loader.load() # loads the documents with metadata
    print(f"Loaded {len(document)} documents")

    # 2. Splitting Documents
    splitter = CharacterTextSplitter(chunk_size=30, chunk_overlap=0) 
    # Each model has limitations on the amount of context it can handle so we provide chunk size.
    # Chunk overlap is the amount of overlap between chunks
    documents = splitter.split_documents(document)
    print(f"Split {len(document)} documents into {len(documents)} chunks")

    # 3. Embedding Documents
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 4. Inserting Documents into VectorDB
    vector_db = PineconeVectorStore.from_documents(documents, embeddings, index_name = "rag-project-1",
                                                   pinecone_api_key = os.getenv("PINECONE_API_KEY")
                                                   ) # index name is the name of the index in pinecone
    print(f"Inserted {len(documents)} documents into VectorDB")


    # pip install python-dotenv
    # pip install langchain-huggingface
    # pip install langchain-pinecone
    # pip install langchain-community
    # pip install langchain
    # for run c:\users\adilr\anaconda3\python.exe .\ingestion.py