from Database_sqlite import Database
import Database_chroma
import re
db = Database(path="./job.db")
k = []
s = []

datas = db.read(
  table_name="competency",
)
for i in range(len(datas)):
  k += (datas[i][5].split(", "))
  s += (datas[1][6].split(", "))

k = list(dict.fromkeys(k))
s = list(dict.fromkeys(s))


k_prompts = ""
s_prompts = ""
for k_prompt in k:
  k_prompts += f"- {k_prompt}\n"
for s_prompt in k:
  s_prompts += f"- {s_prompt}\n"


prompt = f'''
你是一位職業顧問，專注於幫助使用者發現他們的職業內涵，包括職業內涵k(知識)和職業內涵s(技能)。請根據使用者的回答來判斷他們擁有的職能。以下是職能的敘述與列表：

職能內涵k(知識)：指執行某項任務所需瞭解可應用於該領域的原則與事實。
職能內涵s(技能)：指執行某項任務所需具備可幫助任務進行的認知層面能力或技術性操作層面的能力(通稱hard skills)，以及跟個人有關之社交、溝通、自我管理行為等能力(通稱soft skills)。

**職業內涵k(知識)**：
{k_prompts}

**職業內涵s(技能)**：
{s_prompts}

請開始與使用者進行對話，通過提出一系列開放式問題來了解他們的背景、興趣和技能。請注意，每次只提出一個問題，並在等待使用者回答後再提出下一個問題。請確保在提出3個問題之後，根據使用者的回答，自行判斷出他們可能擁有的職業內涵k和s，並確保這些職能僅限於上述列表中。

在你確定了使用者的職能後，請按照以下格式輸出結果，且確保每個類別最多不超過10個項目：

### 職業內涵k(知識):
- 知識1
- 知識2
- ...

### 職業內涵s(技能):
- 技能1
- 技能2
- ...

並在最後附上「判斷已完成，對話結束。」以表示對話的結束。

在開始對話時，可以用友好且引導性的語言，讓使用者感到舒適並鼓勵他們分享更多。請注意全程使用中文進行應答。請開始對話：
'''
# print(prompt)


conversation_history = [{"role":"system","content":prompt}]

from openai import OpenAI
client = OpenAI()


while True:

  stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation_history,
    stream=True
  )

  ai_response = ""
  print("ai: ", end="")
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          ai_response += chunk.choices[0].delta.content
          print(chunk.choices[0].delta.content, end="")
  print("")
  conversation_history.append({"role":"assistant","content":ai_response})

  if "判斷已完成，對話結束。" in ai_response:
     break
  
  user_input = input("user: ")
  # print(f"user: {user_input}")

  conversation_history.append({"role":"user","content":user_input})


# 使用正則表達式提取 k 和 s
k_match = re.search(r'### 職業內涵k\(知識\):\n((?:- .*\n?)+)', ai_response)
s_match = re.search(r'### 職業內涵s\(技能\):\n((?:- .*\n?)+)', ai_response)

# 提取並格式化
k_values = [item.strip('- ').strip() for item in k_match.group(1).strip().split("\n")] if k_match else []
s_values = [item.strip('- ').strip() for item in s_match.group(1).strip().split("\n")] if s_match else []

# 打印結果
print("職業內涵k(知識)列表:", k_values)
print("職業內涵s(技能)列表:", s_values)

query = "職業內涵k: "
for i in range(len(k_values)):
    query += f"{k_values[i]}"
    if k_values[i] != k_values[-1]:
      query += ", "
    else:
       query += "。"
query += "職業內涵s: "
for i in range(len(s_values)):
    query += f"{s_values[i]}"
    if s_values[i] != s_values[-1]:
      query += ", "
    else:
       query += "。"

db_chroma = Database_chroma.Database(path="./Database")

matched_jobs = db_chroma.query(
   table_name="competency",
   key_words=[query],
   n_results=5
)["ids"][0]

job_summary = db_chroma.query(
   table_name="job_104",
   key_words=[query],
   n_results=5,
   where={"職業":{"$in":matched_jobs}}
)["ids"][0]

jobs = db.query(
   magic_words=f"select * from job_104 where 職缺名稱 in {tuple(job_summary)}"
)
title = db.read_title(table_name="job_104")

vacancies = []
for job in jobs:
  vacancy = ""
  for i in range(len(title)):
    if i not in [8,10,11,12]:
      vacancy += f"{title[i]}: {job[i]}。"
  vacancies.append(vacancy)

prompt = f'''
你是一位職業分析師，根據使用者的回答、職能分析結果以及從向量資料庫中查找到的職業和職缺資料，請生成一份職能分析報告。報告應該包括以下內容：

1. **使用者擁有的職能**：
   - 使用者擁有的知識 (k)：{', '.join(k_values)}
   - 使用者擁有的技能 (s)：{', '.join(s_values)}

2. **對應的職業**：
   根據使用者的職能分析，以下是最相關的職業：
   - 職業1：{matched_jobs[0]}
   - 職業2：{matched_jobs[1]}
   - 職業3：{matched_jobs[2]}
   - 職業4：{matched_jobs[3]}
   - 職業5：{matched_jobs[4]}

3. **推薦的職缺概述**：
   以下是針對上述職業的推薦職缺的概述（更詳細的內容如公司名稱、上班地點、職缺連結等可以在使用者詢問時提供）：
   - 職缺1：{vacancies[0]}
   - 職缺2：{vacancies[1]}
   - 職缺3：{vacancies[2]}
   - 職缺4：{vacancies[3]}
   - 職缺5：{vacancies[4]}

請根據以上信息，生成一份詳細的職能分析報告，提供給使用者參考，需要包括推薦的職缺。如果使用者對某個職缺有進一步的興趣，請保留更詳細的資料，如公司名稱、上班地點、職缺連結等，以便在後續對話中提供。
'''
conversation_history.append({"role":"system","content":prompt})
conversation_history.append({"role":"user","content":"請產出分析報告"})

# from langchain_ollama import ChatOllama
# from langchain.chains import ConversationChain
# from langchain_core.prompts import ChatPromptTemplate
import ollama
# from ollama import chat
while True:
  # stream = ollama.chat(
  #    model="llama3.1",
  #    messages=conversation_history,
  #    stream=True
  # )
  stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=conversation_history,
    stream=True
  )

  ai_response = ""
  print("ai: ", end="")
  # for chunk in stream:
  #   print(chunk['message']['content'], end='', flush=True)
  for chunk in stream:
      if chunk.choices[0].delta.content is not None:
          ai_response += chunk.choices[0].delta.content
          print(chunk.choices[0].delta.content, end="")
  print("")
  conversation_history.append({"role":"assistant","content":ai_response})
  
  user_input = input("user: ")

  conversation_history.append({"role":"user","content":user_input})