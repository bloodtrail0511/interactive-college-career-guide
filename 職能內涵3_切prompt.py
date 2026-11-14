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

conversation_history = []

prompt = f'''
你是一位職業顧問，專注於幫助使用者發現他們的職業內涵，包括職業內涵k(知識)和職業內涵s(技能)。請根據使用者的回答來判斷他們擁有的職能。以下是職能的敘述與列表：

職能內涵k(知識)：指執行某項任務所需瞭解可應用於該領域的原則與事實。
職能內涵s(技能)：指執行某項任務所需具備可幫助任務進行的認知層面能力或技術性操作層面的能力(通稱hard skills)，以及跟個人有關之社交、溝通、自我管理行為等能力(通稱soft skills)。
'''
conversation_history.append({"role":"system","content":prompt})

prompt = f'''
**職業內涵k(知識)**：
{k_prompts}

**職業內涵s(技能)**：
{s_prompts}
'''
conversation_history.append({"role":"system","content":prompt})

prompt = f'''
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
conversation_history.append({"role":"system","content":prompt})

from openai import OpenAI
client = OpenAI()# 我的
import ollama

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

  # print(stream)
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
'''
0   職缺名稱
1   工作地點
2   學歷要求
3   工作經歷
4   科系要求
5   公司名稱
6   公司產業類別
7   工作待遇
8   更新日期
9   工作內容
10  應徵分析
11  職缺連結
12  公司連結
13  職業
'''
vacancies = []
for job in jobs:
  vacancy = ""
  for i in range(len(title)):
    if i in [0,1,2,3,4,5,6,7,9,13]:
      vacancy += f"{title[i]}: {job[i]}。"
  vacancies.append(vacancy)

prompt = f'''
你是一位職業分析師，根據使用者的回答、職能分析結果以及從向量資料庫中查找到的職業和職缺資料，請生成一份職能分析報告。報告應該包括以下內容：
1. **使用者擁有的職能**：
   - 使用者擁有的知識 (k)
   - 使用者擁有的技能 (s)
2. **對應的職業**：
   根據使用者的職能分析，以下是最相關的職業：
   - 職業1：{matched_jobs[0]}
   - 職業2：{matched_jobs[1]}
   - 職業3：{matched_jobs[2]}
   - 職業4：{matched_jobs[3]}
   - 職業5：{matched_jobs[4]}
3. **推薦的職缺概述**：
   最後，這裡是針對上述職業的推薦職缺的簡短概述。這些職缺的詳細資料如公司名稱、上班地點、職缺連結等，將在使用者進一步詢問時提供：
   - 職缺1：{vacancies[0]}
   - 職缺2：{vacancies[1]}
   - 職缺3：{vacancies[2]}
   - 職缺4：{vacancies[3]}
   - 職缺5：{vacancies[4]}
請根據以上信息，生成一份詳細的職能分析報告，請注意包含推薦的職缺概述，並且明確告知使用者可以要求更多詳細資料。詳細資料包括但不限於公司名稱、上班地點、職缺連結等。
'''
conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
# 1. **使用者擁有的職能**：
#    - 使用者擁有的知識 (k)：{', '.join(k_values)}
#    - 使用者擁有的技能 (s)：{', '.join(s_values)}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
# 2. **對應的職業**：
#    根據使用者的職能分析，以下是最相關的職業：
#    - 職業1：{matched_jobs[0]}
#    - 職業2：{matched_jobs[1]}
#    - 職業3：{matched_jobs[2]}
#    - 職業4：{matched_jobs[3]}
#    - 職業5：{matched_jobs[4]}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
# 3. **推薦的職缺概述**：
#    最後，這裡是針對上述職業的推薦職缺的簡短概述。這些職缺的詳細資料如公司名稱、上班地點、職缺連結等，將在使用者進一步詢問時提供：
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
#    - 職缺1：{vacancies[0]}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
#    - 職缺2：{vacancies[1]}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
#    - 職缺3：{vacancies[2]}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
#    - 職缺4：{vacancies[3]}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
#    - 職缺5：{vacancies[4]}
# '''
# conversation_history.append({"role":"system","content":prompt})
# prompt = f'''
# 請根據以上信息，生成一份詳細的職能分析報告，請注意包含推薦的職缺概述，並且明確告知使用者可以要求更多詳細資料。詳細資料包括但不限於公司名稱、上班地點、職缺連結等。
# '''
# conversation_history.append({"role":"system","content":prompt})





# prompt = f'''
# 請根據以上信息，生成一份詳細的職能分析報告，*請使用此模板來生成報告*
# 【分析報告】

# ### 1. 你所擁有的職能：
# - **職業內涵(知識k)：** 
#   - 嵌入式系統基礎
#   - 機器學習概念
#   - 數位電子學
#   - 控制系統基本原理
#   - 電子元器件及其特性

# - **職業內涵(技能s)：**
#   - 系統設計與開發
#   - 問題解決能力
#   - 軟體設計
#   - 硬體整合
#   - 測試與驗證能力
#   - 文獻檢索知識

# ### 2. 對應的職業：
# 根據使用者的職能分析，以下是最相關的職業：
# - **職業1：** 物聯網研發工程人員
# - **職業2：** 電腦週邊設備硬體研發工程人員
# - **職業3：** 消費性電子產品機構設計人員
# - **職業4：** 製造業CAD_CAM工程人員
# - **職業5：** 物聯網研發助理工程人員

# ### 3. 推薦的職缺概述：
# 以下是針對上述職業的推薦職缺的概述。注意：這裡只提供簡要概述，如需詳細信息（包括公司名稱、上班地點、工作待遇等），請使用者進一步詢問。
# - **職缺1：** 
#   - **職缺名稱**: 硬體工程師 HW Engineer
#   - **學歷要求**: 碩士
#   - **工作經歷**: 經歷不拘
#   - **科系要求**: 電機電子工程相關
#   - **工作內容**: 負責機器人的電力規劃/電子電路設計，與跨功能團隊合作，技術調研等。
# - **職缺2：**
#   - **職缺名稱**: USB System Design Engineer
#   - **學歷要求**: 專科
#   - **工作經歷**: 1年以上
#   - **科系要求**: 電機電子工程相關
#   - **工作內容**: 負責USB相關電路設計與PCB焊接、驗證等。
# - **職缺3：**
#   - **職缺名稱**: 研發主管
#   - **學歷要求**: 專科
#   - **工作經歷**: 6年以上
#   - **科系要求**: 電機電子工程相關
#   - **工作內容**: 負責新產品的研發設計和管控，電子電路設計與程式語言設計等。
# - **職缺4：**
#   - **職缺名稱**: 軟體設計工程師
#   - **學歷要求**: 大學
#   - **工作經歷**: 經歷不拘
#   - **科系要求**: 光電工程相關, 電機電子工程相關
#   - **工作內容**: 負責新產品的研發設計和管控，電子電路設計與程式語言設計等。
# - **職缺5：**
#   - **職缺名稱**: 機構工程師-ME
#   - **學歷要求**: 專科
#   - **工作經歷**: 2年以上
#   - **科系要求**: 機械工程相關
#   - **工作內容**: 負責產品機構設計與開發階段的相關測試等。

# ### 4. 結論與建議：
# 請根據以上分析提供一個總結，並給出職業發展的建議。提醒使用者可以進一步詢問以獲得更詳細的職缺資料。
# '''
conversation_history.append({"role":"system","content":prompt})


conversation_history.append({"role":"user","content":"請產出分析報告"})


import ollama
while True:
  stream = ollama.chat(
     model="llama3.1",
     messages=conversation_history,
     stream=True
  )
  # stream = client.chat.completions.create(
  #   model="gpt-4o-mini",
  #   messages=conversation_history,
  #   stream=True
  # )

  ai_response = ""
  print("ai: ", end="")
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)
  # for chunk in stream:
  #     if chunk.choices[0].delta.content is not None:
  #         ai_response += chunk.choices[0].delta.content
  #         print(chunk.choices[0].delta.content, end="")

  print("")
  conversation_history.append({"role":"assistant","content":ai_response})
  
  user_input = input("user: ")

  conversation_history.append({"role":"user","content":user_input})