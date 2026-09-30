import chromadb
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_tavily import TavilySearch
from pydantic import BaseModel,Field

load_dotenv()

client = chromadb.PersistentClient(path="./chroma_db_veri")

koleksiyon = client.get_collection(name="langchain")

soru = input("Sorunuzu Giriniz: ")

#Veri sorumlusunun aydınlatma yükümlülüğü nedir?

embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

soru_vektoru = embedding.embed_query(soru)

sonuclar = koleksiyon.query(query_embeddings=[soru_vektoru], n_results=3)

metinler = "\n\n".join(sonuclar['documents'][0])

LLM = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

system_prompt = f"""
    Sen katı ve tarafsız bir denetleyecisisin.

    Görevin: Kullanıcının sorusunun, yalnızca
    sağlanan metin parçalarındaki bilgilerle 
    tam ve doğru şekilde cevaplanıp cevaplanamayacağını değerlendirmek.

    KURALLAR:
    1. Kendi genel kültürünü veya dış bilgini kesinlikle kullanma.
    2. Sadece verilen metinlere sadık kal.
    3. Cevap metinde açıkça yoksa, üstünkörü geçiyorsa veya eksik kalıyorsa bunu yetersiz olarak değerlendir.q
    """

prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("human", "Soru: {soru}\n\nMetinler: {metinler}\n\nVektör Skorları: {vektor_skorlari}"),
])


class denetleyici(BaseModel):
    yeterli_mi: bool = Field(
    description="Cevap metinlerde yeterli mi? Evet ise True, Hayır ise False"
    )
    gerekce: str = Field(
    description="Neden yeterli veya yetersiz olduğuna dair kısa, tek cümlelik açıklama."
    )

structured_llm = LLM.with_structured_output(denetleyici)

chain = prompt | structured_llm

karar = chain.invoke({
    "system_prompt": system_prompt,
    "soru": soru,
    "metinler": metinler,
    "vektor_skorlari": str(sonuclar['distances'][0])
})

print(f"Sonuç: {karar.yeterli_mi}")
print(f"Gerekçe: {karar.gerekce}")

if karar.yeterli_mi == False:
    print("*" * 50)
    print("Yeterli bilgi bulunamadı. Aşağıdaki arama sonuçlarını inceleyerek sorunuza yanıt bulmaya çalışın.")
    tavily_search = TavilySearch(max_results=3, search_engine="google", language="tr", description="Kullanıcının sorusuna yanıt verecek yeterli bilgi bulunamadı. Lütfen aşağıdaki arama sonuçlarını inceleyin ve sorunuza yanıt bulmaya çalışın.")
    arama_sonuclari = tavily_search.invoke({"query": soru})

    parcalar = []
    site_linkleri = []
    
    for sonuc in arama_sonuclari["results"]:
        url = sonuc.get("url")
        icerik = sonuc.get("content")
        
        parcalar.append(f"Kaynak ({url}):\n{icerik}")
        site_linkleri.append(url)
        
    final_baglam = "\n\n---\n\n".join(parcalar)
    print(f"Arama Sonuçları:\n{final_baglam}")
    #"Veri ihlali durumunda Kurul'a kaç saat içinde bildirim yapılmalıdır ve bildirim formu nereden indirilir?"