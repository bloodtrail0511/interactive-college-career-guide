import csv
from rich.progress import track
import sqlite3


# csvfile = open('jobs.csv', "r", encoding='utf-8')

# job_list = list(csv.reader(csvfile))
# des_list = []
# for i in job_list:
#    des_list.append(len(i[9]))
# print(des_list)
# print(max(des_list))
# print(des_list.index(4078))
# print(job_list[1334][9])
# print(len(job_list[1334][9]))

# csvfile.close()

with open('jobs.csv', "r", encoding='utf-8') as csvfile:
  reader = csv.reader(csvfile)
  job_list = list(reader)
  print(len(job_list[0]))


  conn = sqlite3.connect('job.db')
  cursor = conn.cursor()


  for i in track(range(len(job_list)), description="[purple]匯入資料庫..."):
    instruction = "INSERT INTO job_104 VALUES ("
    for j in job_list[i]:
        instruction += f"'{j}',"
    instruction += "'',"
    instruction += f"{i-1})"
    # print(instruction)
    cursor.execute(instruction)
    conn.commit()


  cursor.close()
  conn.close()