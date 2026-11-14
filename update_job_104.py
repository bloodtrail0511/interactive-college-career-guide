import Database_chroma
import Database_sqlite
from rich.progress import track

sqlite_db = Database_sqlite.Database(path="job.db")
chroma_db = Database_chroma.Database(path="./Database")

title = sqlite_db.read_title(table_name="job_104")
datas = sqlite_db.read(table_name="job_104")

# datas = sqlite_db.read(table_name="job_104", condition=["職業","醫療設備工程管理人員"])


# for i in range(len(datas)):
#   # 將職缺組合成長文本
#   query = ""
#   for j in range(len(title)):
#     if j not in [8, 10, 11, 12, 13]:
#     # if j not in [1, 2, 3, 5, 7, 8,10,11,12,13]:
#       # print(f"{j}:{title[j]}")
#       query += f"{title[j]}: {datas[i][j]}。"

#   # 職缺長文本匹配職業
#   result = chroma_db.query(
#   table_name="competency",
#   key_words=[query],
#   n_results=10,
#   include=[]
#   )["ids"][0]

#   print(f"{datas[i][0]}:")
#   for k in range(10):
#     print(f"{k}:{result[k]}")

#   # 職業寫入職缺table
#   sqlite_db.update(
#     table_name="job_104",
#     vacancy=datas[i][0],
#     profession=result[int(input())]
#   )


# for i in track(range(len(datas)), description="[pink]匹配職業中..."):
#   # 將職缺組合成長文本
#   query = ""
#   for j in range(len(title)):
#     if j not in [8, 10, 11, 12, 13]:
#     # if j not in [1, 2, 3, 5, 7, 8,10,11,12,13]:
#       # print(f"{j}:{title[j]}")
#       query += f"{title[j]}: {datas[i][j]}。"

#   # 職缺長文本匹配職業
#   result = chroma_db.query(
#   table_name="competency",
#   key_words=[query],
#   n_results=1,
#   include=[]
#   )["ids"][0][0]

#   # 職業寫入職缺table
#   sqlite_db.update(
#     table_name="job_104",
#     vacancy=datas[i][0],
#     profession=result
#   )



for i in track(range(len(datas)), description="[pink]存進chroma..."):
  ids = [datas[i][0]]
  metadatas = {}
  documents = ""
  for j in range(len(title)):
    metadatas[title[j]] = datas[i][j]
    if j not in [8,10,11,12]:
      documents += f"{title[j]}: {datas[i][j]}。"
  chroma_db.add(
    table_name="job_104",
    ids=ids,
    metadatas=[metadatas],
    documents=[documents]
  )



print("complete")
# import chromadb
# chromadb.PersistentClient("./Database").delete_collection("job_104")
# chromadb.PersistentClient("./Database").create_collection("job_104")
# chromadb.PersistentClient("./Database").get_collection("job_104").get(include=[])["ids"]
