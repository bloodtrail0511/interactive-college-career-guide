import chromadb
from FlagEmbedding import BGEM3FlagModel
# import Database_chroma

client = chromadb.PersistentClient("./Database_ppt")
table = client.get_or_create_collection("table1")


model = BGEM3FlagModel("BAAI/bge-m3")

model.encode(sentences=["流行音樂行銷企劃","半導體產業韌體工程師","遊戲技術美術人員"])["dense_vecs"]

table.delete(ids=["1","2","3"])

sentences=model.encode(sentences=["流行音樂行銷企劃","半導體產業韌體工程師","遊戲技術美術人員"])["dense_vecs"]

table.add(
  ids=["1","2","3"],
  embeddings=sentences,
  documents=["流行音樂行銷企劃","半導體產業韌體工程師","遊戲技術美術人員"]
)


table.query(
  query_embeddings=model.encode(
    sentences=["半導體產業類比IC設計工程師"])["dense_vecs"],
  n_results=3,
  include=["distances","documents"]
)

