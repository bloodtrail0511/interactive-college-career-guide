# coding:utf-8
from Database_sqlite import Database
import Database_chroma
# import re
db = Database(path="./job.db")


# 提取並格式化
k_values = ['電子電路知識', '控制系統設計', '程式設計', '嵌入式系統概論', '系統建模與識別', '機械原理、運作、性能與應用', '基本 RF 電路理論', '數據分析理論', '基本通訊協定', 'CAD 製圖理論']
s_values = ['C++ 程式設計能力', 'MATLAB 數據分析與繪圖技能', '問題分析與解決能力', '團隊合作與專案管理能力', '嵌入式系統設計與實作技能', '數據蒐集與分析能力', '系統整合能力', '自我學習能力', '技術文檔撰寫能力', '溝通協調能']

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
   n_results=3
)["ids"][0]

job_summary = db_chroma.query(
   table_name="job_104",
   key_words=[query],
   n_results=3,
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

conversation_history = [{'role': 'system','content': '\n你是一位職業顧問，專注於幫助使用者發現他們的職業內涵，包括職業內涵k(知識)和職業內涵s(技能)。請根據使用者的回答來判斷他們擁有的職能。以下是職能的敘述與列表：\n\n職能內涵k(知識)：指執行某項任務所需瞭解可應用於該領域的原則與事實。\n職能內涵s(技能)：指執行某項任務所需具備可幫助任務進行的認知層面能力或技術性操作層面的能力(通稱hard skills)，以及跟個人有關之社交、溝通、自我管理行為等能力(通稱soft skills)。\n'},
 {'role': 'assistant',
  'content': '你好！很高興與你交流。為了更好地了解你的背景和興趣，我想先問你一個問題：你目前的職業是什麼？或者如果你是學生，學習的是什麼專業呢？'},
 {'role': 'user', 'content': '我現在是機械系大四，我對未來很迷茫，我對於嵌入式系統的領域有興趣，之前有做過基於單片機的專題'},
 {'role': 'assistant',
  'content': '謝謝你的分享！機械系的專業背景加上對嵌入式系統的興趣，聽起來非常有前景。那麼，第二個問題是：在過去的學習或實踐中，有哪些技能或知識是你覺得自己特別擅長的呢？比如說，編程、問題解決、團隊合作等。'},
 {'role': 'user', 'content': '使用了c++做為開發語言，並用matlab做數據繪製與分析'},
 {'role': 'assistant',
  'content': '非常好！你提到的C++和MATLAB在嵌入式系統和數據處理方面都非常重要。接下來，我想問的是：除了嵌入式系統之外，還有沒有其他你感興趣的領域或工作職位呢？如果有的話，能分享一下具體是哪些方面嗎？'},
 {'role': 'user', 'content': '我希望在嵌入式系統的領域擔任工程師，我享受項目經由我建構起來並成功運行'},
 {'role': 'assistant',
  'content': '了解了，謝謝你分享這些資訊！根據你的回答，我來判斷一下你可能擁有的職業內涵k(知識)和職業內涵s(技能)。\n\n### 職業內涵k(知識):\n- 電子電路知識\n- 控制系統設計\n- 程式設計\n- 嵌入式系統概論\n- 系統建模與識別\n- 機械原理、運作、性能與應用\n- 基本 RF 電路理論\n- 數據分析理論\n- 基本通訊協定\n- CAD 製圖理論\n\n### 職業內涵s(技能):\n- C++ 程式設計能力\n- MATLAB 數據分析與繪圖技能\n- 問題分析與解決能力\n- 團隊合作與專案管理能力\n- 嵌入式系統設計與實作技能\n- 數據蒐集與分析能力\n- 系統整合能力\n- 自我學習能力\n- 技術文檔撰寫能力\n- 溝通協調能\n\n判斷已完成，對話結束。'}]

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
3. **推薦的職缺概述**：
   最後，這裡是針對上述職業的推薦職缺的簡短概述。這些職缺的詳細資料如公司名稱、上班地點、職缺連結等，將在使用者進一步詢問時提供：
   - 職缺1：{vacancies[0]}
   - 職缺2：{vacancies[1]}
   - 職缺3：{vacancies[2]}
請根據以上信息，生成一份詳細的職能分析報告，請注意包含推薦的職缺概述，並且明確告知使用者可以要求更多詳細資料。詳細資料包括但不限於公司名稱、上班地點等。
'''
conversation_history.append({"role":"system","content":prompt})




prompt = f'''
請根據以上信息，生成一份詳細的職能分析報告，*請使用此模板來生成報告*
【分析報告】

### 1. 你所擁有的職能：
- **職業內涵(知識k)：** 
  - 內涵1
  - 內涵2
  ...

- **職業內涵(技能s)：**
  - 內涵1
  - 內涵2
  ...

### 2. 對應的職業：
根據使用者的職能分析，以下是最相關的職業：
- **職業1：** 
- **職業2：** 
- **職業3：** 

### 3. 推薦的職缺概述：
以下是針對上述職業的推薦職缺的概述。注意：這裡只提供簡要概述，如需詳細信息（包括公司名稱、上班地點、工作待遇等），請使用者進一步詢問。
- **職缺1：** 
  - **職缺名稱**: 
  - **學歷要求**: 
  - **工作經歷**: 
  - **科系要求**: 
  - **工作內容**: 
- **職缺2：**
  - **職缺名稱**: 
  - **學歷要求**: 
  - **工作經歷**: 
  - **科系要求**: 
  - **工作內容**: 
- **職缺3：**
  - **職缺名稱**: 
  - **學歷要求**: 
  - **工作經歷**: 
  - **科系要求**: 
  - **工作內容**: 

### 4. 結論與建議：
請根據以上分析提供一個總結，並給出職業發展的建議。提醒使用者可以進一步詢問以獲得更詳細的職缺資料。
'''
conversation_history.append({"role":"system","content":prompt})


conversation_history.append({"role":"user","content":"請產出分析報告，職缺名稱請完全按照資料庫搜索之資料"})


import ollama
while True:
  stream = ollama.chat(
     model="llama3.1",
     messages=conversation_history,
     stream=True
  )

  ai_response = ""
  print("ai: ", end="")
  for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

  print("")
  conversation_history.append({"role":"assistant","content":ai_response})
  
  user_input = input("user: ")
  if user_input.lower() == "exit":
    break

  conversation_history.append({"role":"user","content":user_input})