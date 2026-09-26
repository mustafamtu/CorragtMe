import chromadb
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db_veri")

koleksiyon = client.get_collection(name="langchain")

soru = input("Sorunuzu Giriniz: ")

#Veri sorumlusunun aydınlatma yükümlülüğü nedir?

embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

soru_vektoru = embedding.embed_query(soru)

sonuclar = koleksiyon.query(query_embeddings=[soru_vektoru], n_results=3)
print(sonuclar)