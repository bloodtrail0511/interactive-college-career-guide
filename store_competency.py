import Database_chroma
import Database_sqlite

sqlite_db = Database_sqlite.Database(path="job.db")
chroma_db = Database_chroma.Database(path="./Database")

title = sqlite_db.read_title(table_name="competency")
datas = sqlite_db.read(table_name="competency")
# datas = datas[-3:]

ids = []
metadatas=[]
documents=[]
for data in datas:
  ids.append(data[0])
  metadata = {}
  document = ""
  for i in range(len(title)):
    metadata[title[i]] = data[i]
    document += f"{title[i]}: {data[i]}。"
  metadatas.append(metadata)
  documents.append(document)



chroma_db.add(
  table_name="competency",
  ids=ids,
  metadatas=metadatas,
  documents=documents
)

# if __name__ == "__main__":
#   import chromadb
#   client = chromadb.PersistentClient("./Database")
#   table = client.get_collection("competency")
#   table.get()["metadatas"][0]