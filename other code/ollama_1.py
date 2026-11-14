# coding:utf-8
# import ollama

# stream = ollama.chat(
#     model='test',
#     messages=[{'role': 'user', 'content': '簡短介紹meta'}],
#     stream=True,
# )

# for chunk in stream:
#   print(chunk['message']['content'], end='', flush=True)


import ollama

conversation_history = [
{'role': 'system',
  'content': '\n你是一位職業分析師，根據使用者的回答、職能分析結果以及從向量資料庫中查找到的職業和職缺資料，請生成一份職能分析報告。報告應該包括以下內容：\n\n1. **使用者擁有的職能**：\n   - 使用者擁有的知識 (k)：嵌入式系統的基本原理, 單片機的使用和應用, 數據分析與繪製的基礎知識, C++程式設計的理論, MATLAB使用的基本技巧\n   - 使用者擁有的技能 (s)：使用C++進行嵌入式系統開發, 使用MATLAB進行數據分析和繪圖, 閱讀和理解datasheet的能力, 系統串聯與模組整合的技巧, 問題解決能力（如在專案中克服挑戰的經驗）\n\n2. **對應的職業**：\n   根據使用者的職能分析，以下是最相關的職業：\n   - 職業1：製造業CAD_CAM工程人員\n   - 職業2：資料工程人員\n   - 職業3：物聯網研發工程人員\n   - 職業4：機器學習工程師\n   - 職業5：電腦週邊設備硬體研發工程人員\n\n3. **推薦的職缺概述**：\n   以下是針對上述職業的推薦職缺的概述（更詳細的內容如公司名稱、上班地點、職缺連結等可以在使用者詢問時提供）：\n   - 職缺1：職缺名稱: 系統韌體工程師 (System Firmware Engineer)。工作地點: 新竹市東區埔頂里慈雲路118號8樓之5。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 電機電子工程相關, 機械工程相關, 資訊工程相關。公司名稱: 開必拓數據股份有限公司。公司產業類別: 電腦及其週邊設備製造業。工作待遇: 待遇面議。更新日期: 20240823。工作內容: 熟悉 Python/C 任一語言 單板電腦程式設計 (Arduino/樹莓派) 應用經驗 控制系統程式設計 (Modbus) 有HTTP、MQTT、HTML、SQL 等Web服務相關基礎知識。。應徵分析: //www.104.com.tw/jobs/apply/analysis/81wge?channel=104rpt&jobsource=apply_analyze。職缺連結: //www.104.com.tw/job/81wge?jobsource=index_s。公司連結: //www.104.com.tw/company/1a2x6bkz0k?jobsource=index_s。職業: 電腦週邊設備硬體研發工程人員。\n   - 職缺2：職缺名稱: 線上面試車用電子功率模組產品工程師(Power Module)。工作地點: 南投縣草屯鎮太平路一段351巷141號。學歷要求: 大學。工作經歷: 經歷不拘。科系要求: 。公司名稱: 環鴻科技股份有限公司。公司產業類別: 消費性電子產品製造業。工作待遇: 待遇面議。更新日期: 20240828。工作內容: 工作內容 1. Define product process flow with ME, TE. 2.BOM and EC change management in PDM.  3. Lead risk assessment with teams for each PCN / PCR.  4. Host meeting for sample build meeting and debug meeting.  5. Coordinate Yield Improvement to meet phase gating.  6. 2nd sources buy off activities and schedule follow up.  7. Coordinate SFIS/MES route and MFG data traceability setup.  8. DA6.3 /IATF16949 audit preparing and co-work with QA leader.  加分條件 1. 具產品工程師或專案管理師2年工作經驗以上佳 2. 具封測廠2年工作經驗以上佳 3. 具Power module製程設計，料開發或產品開發經驗佳 4. 具半導體封裝相關經驗(etc: die attach, wire bonding, molding)佳 5. Toeic 600分以上佳 6. 具日檢與日語能力者尤佳  職缺投遞https://usiglobal.freshteam.com/jobs。應徵分析: //www.104.com.tw/jobs/apply/analysis/7qy7r?channel=104rpt&jobsource=apply_analyze。職缺連結: //www.104.com.tw/job/7qy7r?jobsource=index_s。公司連結: //www.104.com.tw/company/dbgbm34?jobsource=index_s。職業: 電腦週邊設備硬體研發工程人員。\n   - 職缺3：職缺名稱: 電腦繪圖人員。工作地點: 台北市內湖區安康路147號。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 工程學科類, 工業技藝及機械學科類, 數學及電算機科學學科類。公司名稱: 德佳鋼鐵有限公司。公司產業類別: 其他金屬相關製造業。工作待遇: 月薪35,000~60,000元。更新日期: 20240821。工作內容: 需熟AutoCAD、solidworks繪圖軟體應用。應徵分析: //www.104.com.tw/jobs/apply/analysis/ixtj?channel=104rpt&jobsource=apply_analyze。職缺連結: //www.104.com.tw/job/ixtj?jobsource=index_s。公司連結: //www.104.com.tw/company/9r49lhs?jobsource=index_s。職業: 製造業CAD_CAM工程人員。\n   - 職缺4：職缺名稱: 研發儲備幹部-東莞廠。工作地點: 廣東省東莞市亞洲其他。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 機械維護相關, 電機電子工程相關, 機械工程相關。公司名稱: 東莞信易電熱機械有限公司。公司產業類別: 通用機械設備製造修配業。工作待遇: 待遇面議。更新日期: 20240823。工作內容: 1.使用繪圖工具(Pro-E)及/或電腦輔助設計CAD或相關軟體對既有機械產品進行整改, 並設計新研發產品的機構。'},
 {'role': 'user', 'content': '請產出分析報告'}
]
# len('\n你是一位職業分析師，根據使用者的回答、職能分析結果以及從向量資料庫中查找到的職業和職缺資料，請生成一份職能分析報告。報告應該包括以下內容：\n\n1. **使用者擁有的職能**：\n   - 使用者擁有的知識 (k)：嵌入式系統的基本原理, 單片機的使用和應用, 數據分析與繪製的基礎知識, C++程式設計的理論, MATLAB使用的基本技巧\n   - 使用者擁有的技能 (s)：使用C++進行嵌入式系統開發, 使用MATLAB進行數據分析和繪圖, 閱讀和理解datasheet的能力, 系統串聯與模組整合的技巧, 問題解決能力（如在專案中克服挑戰的經驗）\n\n2. **對應的職業**：\n   根據使用者的職能分析，以下是最相關的職業：\n   - 職業1：製造業CAD_CAM工程人員\n   - 職業2：資料工程人員\n   - 職業3：物聯網研發工程人員\n   - 職業4：機器學習工程師\n   - 職業5：電腦週邊設備硬體研發工程人員\n\n3. **推薦的職缺概述**：\n   以下是針對上述職業的推薦職缺的概述（更詳細的內容如公司名稱、上班地點、職缺連結等可以在使用者詢問時提供）：\n   - 職缺1：職缺名稱: 系統韌體工程師 (System Firmware Engineer)。工作地點: 新竹市東區埔頂里慈雲路118號8樓之5。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 電機電子工程相關, 機械工程相關, 資訊工程相關。公司名稱: 開必拓數據股份有限公司。公司產業類別: 電腦及其週邊設備製造業。工作待遇: 待遇面議。更新日期: 20240823。工作內容: 熟悉 Python/C 任一語言 單板電腦程式設計 (Arduino/樹莓派) 應用經驗 控制系統程式設計 (Modbus) 有HTTP、MQTT、HTML、SQL 等Web服務相關基礎知識。。應徵分析: //www.104.com.tw/jobs/apply/analysis/81wge?channel=104rpt&jobsource=apply_analyze。職缺連結: //www.104.com.tw/job/81wge?jobsource=index_s。公司連結: //www.104.com.tw/company/1a2x6bkz0k?jobsource=index_s。職業: 電腦週邊設備硬體研發工程人員。\n   - 職缺2：職缺名稱: 線上面試車用電子功率模組產品工程師(Power Module)。工作地點: 南投縣草屯鎮太平路一段351巷141號。學歷要求: 大學。工作經歷: 經歷不拘。科系要求: 。公司名稱: 環鴻科技股份有限公司。公司產業類別: 消費性電子產品製造業。工作待遇: 待遇面議。更新日期: 20240828。工作內容: 工作內容 1. Define product process flow with ME, TE. 2.BOM and EC change management in PDM.  3. Lead risk assessment with teams for each PCN / PCR.  4. Host meeting for sample build meeting and debug meeting.  5. Coordinate Yield Improvement to meet phase gating.  6. 2nd sources buy off activities and schedule follow up.  7. Coordinate SFIS/MES route and MFG data traceability setup.  8. DA6.3 /IATF16949 audit preparing and co-work with QA leader.  加分條件 1. 具產品工程師或專案管理師2年工作經驗以上佳 2. 具封測廠2年工作經驗以上佳 3. 具Power module製程設計，料開發或產品開發經驗佳 4. 具半導體封裝相關經驗(etc: die attach, wire bonding, molding)佳 5. Toeic 600分以上佳 6. 具日檢與日語能力者尤佳  職缺投遞https://usiglobal.freshteam.com/jobs。應徵分析: //www.104.com.tw/jobs/apply/analysis/7qy7r?channel=104rpt&jobsource=apply_analyze。職缺連結: //www.104.com.tw/job/7qy7r?jobsource=index_s。公司連結: //www.104.com.tw/company/dbgbm34?jobsource=index_s。職業: 電腦週邊設備硬體研發工程人員。\n   - 職缺3：職缺名稱: 電腦繪圖人員。工作地點: 台北市內湖區安康路147號。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 工程學科類, 工業技藝及機械學科類, 數學及電算機科學學科類。公司名稱: 德佳鋼鐵有限公司。公司產業類別: 其他金屬相關製造業。工作待遇: 月薪35,000~60,000元。更新日期: 20240821。工作內容: 需熟AutoCAD、solidworks繪圖軟體應用。應徵分析: //www.104.com.tw/jobs/apply/analysis/ixtj?channel=104rpt&jobsource=apply_analyze。職缺連結: //www.104.com.tw/job/ixtj?jobsource=index_s。公司連結: //www.104.com.tw/company/9r49lhs?jobsource=index_s。職業: 製造業CAD_CAM工程人員。\n   - 職缺4：職缺名稱: 研發儲備幹部-東莞廠。工作地點: 廣東省東莞市亞洲其他。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 機械維護相關, 電機電子工程相關, 機械工程相關。公司名稱: 東莞信易電熱機械有限公司。公司產業類別: 通用機械設備製造修配業。工作待遇: 待遇面議。更新日期: 20240823。工作內容: 1.使用繪圖工具(Pro-E)及/或電腦輔助設計CAD或相關軟體對既有機械產品進行整改, 並設計新研發產品的機構。')
# while True:
stream = ollama.chat(
    model="llama3.1",
    messages=conversation_history,
    stream=True
)
ai_response = ""
print("ai: ", end="")
for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)

# print(stream)
print("")
conversation_history.append({"role":"assistant","content":ai_response})

user_input = input("user: ")

conversation_history.append({"role":"user","content":user_input})