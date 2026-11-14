import sqlite3
import faiss

conn = sqlite3.connect('job.db')
cursor = conn.cursor()




# 將104職缺資料、表格標題取出
job_104 = cursor.execute("select * from job_104")
job_104_title = []
for i in job_104.description:
  job_104_title.append(i[0])
job_104_total_data = job_104.fetchall()


job_104_for_embedding = []
# file = open("jobs.txt", 'w', encoding='utf-8')
# 將職缺資料置於對應標題後方，組合成要向量化的文本
for job_104_data in job_104_total_data:
  chunk = ""
  for i in range(len(job_104_title)):
    chunk += f"{job_104_title[i]}: "
    chunk += f"{job_104_data[i]}。"
  job_104_for_embedding.append(chunk)
  # file.write(chunk+"\n")
# file.close()
# '職缺名稱: 擴線需求探針卡(Probe Card)測試副工程師工程師 (依學經歷核定職稱)精材科技股份有限公司_9/13(五)實體媒合會現場面談。工作地點: 桃園市中壢區中園路188號 (中壢工業區)。學歷要求: 大學。工作經歷: 經歷不拘。科系要求: 化學工程相關, 電機電子工程相關。公司名稱: 企業專案招募104未來無限整合招募中心。公司產業類別: 網際網路相關業。工作待遇: 月薪33,000~60,000元。更新日期: 20240816。工作內容: 應徵本職缺經審核通過者，將邀約出席9/13(五) 媒合會現場面談，本實體活動為桃園市政府青年事務局之專案活動  1. 探針卡問題分析/排除 2. 探針卡驗證維修 3. 專案事項處理 4. 其他主管交辦事項  週40小時制(類做二休二)，約3~6個月輪調日夜 休假日加班優於勞基法全日以兩倍計算加班費。應徵分析: //www.104.com.tw/jobs/apply/analysis/8g71j?channel=104rpt&jobsource=hotjob_chr。職缺連結: //www.104.com.tw/job/8g71j?jobsource=hotjob_chr。公司連結: //www.104.com.tw/company/19xtf120?jobsource=hotjob_chr。職業: 。'


# 將職缺資料置於對應標題後方，組合成要向量化的文本
# for job_104_data in job_104_total_data:
#   chunk = []
#   for i in range(len(job_104_title)):
#     temp = ""
#     temp += f"{job_104_title[i]}: "
#     temp += f"{job_104_data[i]}"
#     chunk.append(temp)
#   job_104_for_embedding.append(chunk)
# ['職缺名稱: 擴線需求探針卡(Probe Card)測試副工程師工程師 (依學經歷核定職稱)精材科技股份有限公司_9/13(五)實體媒合會現場面談',
#  '工作地點: 桃園市中壢區中園路188號 (中壢工業區)',
#  '學歷要求: 大學',
#  '工作經歷: 經歷不拘',
#  '科系要求: 化學工程相關, 電機電子工程相關',
#  '公司名稱: 企業專案招募104未來無限整合招募中心',
#  '公司產業類別: 網際網路相關業',
#  '工作待遇: 月薪33,000~60,000元',
#  '更新日期: 20240816',
#  '工作內容: 應徵本職缺經審核通過者，將邀約出席9/13(五) 媒合會現場面談，本實體活動為桃園市政府青年事務局之專案活動  1. 探針卡問題分析/排除 2. 探針卡驗證維修 3. 專案事項處理 4. 其他主管交辦事項  週40小時制(類做二休二)，約3~6個月輪調日夜 休假日加班優於勞基法全日以兩倍計算加班費',
#  '應徵分析: //www.104.com.tw/jobs/apply/analysis/8g71j?channel=104rpt&jobsource=hotjob_chr',
#  '職缺連結: //www.104.com.tw/job/8g71j?jobsource=hotjob_chr',
#  '公司連結: //www.104.com.tw/company/19xtf120?jobsource=hotjob_chr',
#  '職業: ']


from FlagEmbedding import BGEM3FlagModel
embedding_model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)


job_104_after_embedding = embedding_model.encode(
  job_104_for_embedding[:2],
  return_dense=True,
  return_sparse=False,
  return_colbert_vecs=False)
job_104_after_embedding.keys()




cursor.close()
conn.close()