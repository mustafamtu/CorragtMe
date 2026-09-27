import chromadb
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db_veri")

koleksiyon = client.get_collection(name="langchain")

soru = input("Sorunuzu Giriniz: ")

#Veri sorumlusunun aydınlatma yükümlülüğü nedir?

embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

soru_vektoru = embedding.embed_query(soru)

sonuclar = koleksiyon.query(query_embeddings=[soru_vektoru], n_results=3)

skorlar = sonuclar['distances'][0]
en_yakin_sonuc = skorlar[0]
print(en_yakin_sonuc)

if en_yakin_sonuc > 0.50:
    pass
