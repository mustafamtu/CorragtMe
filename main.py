import chromadb
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

chroma_client = chromadb.PersistentClient(path="./chroma_db_veri")

collection = chroma_client.get_collection(name="langchain")

soru = input("Sorunuzu Giriniz: ")

#Veri sorumlusunun aydınlatma yükümlülüğü nedir?

embedding = GoogleGenerativeAIEmbeddings(model="text-embedding-001")

soru_vektoru = embedding.embed_query(soru)

print(soru_vektoru)
