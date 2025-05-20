from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

#Load embedding model
model =SentenceTransformer('all-MiniLM-L6-v2')

#Initialize ChromoDB client 
client = chromadb.Client(Settings(  
    chroma_db_impl="duckdb+parquet",    #use DuckDB with Parquet for storage
    persist_directory="./chroma_store" #path to store the database
))

collection = client.get_or_create_collection(name="enterprise_docs") #create or get a collection for storing documents


def index_chunks(chunks):
    #embed and store documents chunks in chromaDB
    embeddings= model.encode(chunks).tolists()
    ids =[f"doc_{i}" for i in range(len(chunks))] #create unique ids for each chunk
    collection.add(documents= chunks, embeddings=embeddings,  ids=ids) #store chunks in the collection

#search for top k similar chunks from stored documents
def query_chunks(query, top_k=3):
    #embed the query
    query_embedding = model.encode(query).tolist()
    #search for similar chunks in the collection
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results['documents'][0]  #return the top k similar chunks


#Uses SentenceTransformer to convert text chunks and queries into vectors
#Uses ChromaDB to store vectors and perform fast similarity search