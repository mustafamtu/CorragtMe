# ⚡ CorragtMe: Corrective RAG (CRAG) Pipeline

CorragtMe, geleneksel RAG (Retrieval-Augmented Generation) sistemlerinde yaşanan **bilgi yetersizliği ve halüsinasyon** problemlerini ortadan kaldırmak amacıyla geliştirilmiş hafif ve optimize edilmiş bir **Corrective RAG (CRAG)** uygulamasıdır.

Vektör veritabanından çekilen doküman parçaları katı bir hakem (Router) tarafından denetlenir; yerel veri yetersizse sistem otomatik olarak **Tavily Web Search** motoruna dallanarak eksik bilgiyi internetten tamamlar.

---

## 🎯 Temel Özellikler & Mühendislik Kararları

- **Katı Doğrulama (Router):** Gemini 2.5 Flash ve Pydantic kullanılarak yapılandırılmış denetçi sınıfı (`True`/`False`), yerel veritabanından çekilen parçaların soruyu tam yanıtlamaya yetip yetmediğini dış bilgi kullanmadan tarafsızca değerlendirir.
- **Dinamik Web Fallback:** Bilgi eksik veya yetersizse (`False`), sistem akışı kesmeden Tavily API aracılığıyla güncel web kaynaklarını tarar.

---

## Sistem Mimarisi

```text
[Kullanıcı Sorgusu]
        │
        ▼
[ChromaDB Vektör Arama] ──► (Doküman Parçaları)
        │
        ▼
[Pydantic Router / Gemini] ──► Karar: Yeterli mi?
        │
        ├──► (True)  ──► Yerel Bilgi Bankasından Yanıt
        │
        └──► (False) ──► [Tavily Web Search Fallback]
                                │
                                └──► Doğrulanmış Özetler & URL Listesi
