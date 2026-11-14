import requests
import json
import csv
from rich.progress import track

url = "https://www.104.com.tw/jobs/search/list"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
    'Referer': 'https://www.104.com.tw/jobs/search/',
}

params = "&jobcat=2008001000"   # 職務類別--工程研發類人員
params += "&asc=0"              # 降冪排序
params += "&order=12"           # 使用相關性 + EVAL_PR 混合排序
params += "&ro=0"               # 工作性質--全部工作
params += "&mode=s"
params += "&jobsource=index_s"
params += "&page=1"
response = requests.get(url=url, headers=headers, params=params)

with open('output.json', 'w', encoding='utf-8') as f:
  json.dump(response.json(), f, ensure_ascii=False, indent=4)

result = response.json()
# result["data"]["totalPage"]
# result["data"]["list"][0]["jobName"]
"""
jobName             職位名稱
jobAddrNoDesc       工作地址(縣市)
jobAddress          工作地址(路名)
optionEdu           學歷要求
periodDesc          工作經歷
major               科系要求
custName            公司名稱
coIndustryDesc      公司產業類別
salaryLow           最低薪資
salaryHigh          最高薪資
salaryDesc          工作待遇
appearDate          更新日期
link_applyAnalyze   應徵分析
link_job            職位連結
link_cust           公司連結
description         工作內容
"""
import re
def clean_text(text):
    if type(text) == list:
      temp = ""
      for obj in text:
        if obj != text[-1]:
          temp += f"{obj}, "
        else:
          temp += f"{obj}"
      text = temp
    text = text.replace("\r\n", " ")
    text = text.replace("\n", " ")
    text = re.sub("[^\u4e00-\u9fff\w\s.,!?&~、，。/+-=()]", "", text)
    return str(text)

with open('jobs.csv', 'a+', newline="", encoding='utf-8') as csvfile:
  write = csv.writer(csvfile)
  write.writerow(['jobName', 'jobAddress', 'optionEdu', 'periodDesc', 'major', 'custName', 'coIndustryDesc', 'salaryDesc', 'appearDate', 'description', 'link_applyAnalyze', 'link_job', 'link_cust'])
  print(f"totalPage: {int(result['data']['totalPage'])}")
  # for i in range(1):
  for i in track(range(int(result["data"]["totalPage"])), description="[purple]爬蟲ing..."):
    if i != 0:
      params = params.replace(f"page={i}", f"page={i+1}")
      response = requests.get(url=url, headers=headers, params=params)
      result = response.json()
    for job in result["data"]['list']:
      job_list = []
      jobName = clean_text(job["jobName"])
      jobAddress = clean_text(job["jobAddrNoDesc"]+job["jobAddress"])
      optionEdu = clean_text(job["optionEdu"])
      periodDesc = clean_text(job["periodDesc"])
      major = clean_text(job["major"])
      custName = clean_text(job["custName"])
      coIndustryDesc = clean_text(job["coIndustryDesc"])
      salaryDesc = clean_text(job["salaryDesc"])
      appearDate = clean_text(job["appearDate"])
      describtion = clean_text(job["description"])
      link_applyAnalyze = clean_text(job["link"]["applyAnalyze"])
      link_job = clean_text(job["link"]["job"])
      link_cust = clean_text(job["link"]["cust"])
      job_list.append(jobName)
      job_list.append(jobAddress)
      job_list.append(optionEdu)
      job_list.append(periodDesc)
      job_list.append(major)
      job_list.append(custName)
      job_list.append(coIndustryDesc)
      job_list.append(salaryDesc)
      job_list.append(appearDate)
      job_list.append(describtion)
      job_list.append(link_applyAnalyze)
      job_list.append(link_job)
      job_list.append(link_cust)
      write.writerow(job_list)