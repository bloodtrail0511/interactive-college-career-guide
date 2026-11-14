from FlagEmbedding import BGEM3FlagModel
embedding_model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)

test1 = ["你今天早上幾點起床?", "老師在哪裡?"]
test2 = ["我早上6點起床", "老師在門口"]

encode1 = embedding_model.encode(test1, return_dense=True, return_sparse=False, return_colbert_vecs=False)
encode2 = embedding_model.encode(test2, return_dense=True, return_sparse=False, return_colbert_vecs=False)
# print(encode1["dense_vecs"][0]@encode2["dense_vecs"][0].T)

from rich import print as pprint
pprint(embedding_model.compute_score([test1[0], test2[0]], weights_for_different_modes=[1, 1, 1]))
pprint(embedding_model.compute_score([test1[1], test2[1]], weights_for_different_modes=[1, 1, 1]))
pprint(embedding_model.compute_score([test1[0], test2[1]], weights_for_different_modes=[1, 1, 1]))
pprint(embedding_model.compute_score([test1[1], test2[0]], weights_for_different_modes=[1, 1, 1]))

test3 = '職缺名稱: 擴線需求探針卡(Probe Card)測試副工程師工程師 (依學經歷核定職稱)精材科技股份有限公司_9/13(五)實體媒合會現場面談。工作地點: 桃園市中壢區中園路188號 (中壢工業區)。學歷要求: 大學。工作經歷: 經歷不拘。科系要求: 化學工程相關, 電機電子工程相關。公司名稱: 企業專案招募104未來無限整合招募中心。公司產業類別: 網際網路相關業。工作待遇: 月薪33,000~60,000元。更新日期: 20240816。工作內容: 應徵本職缺經審核通過者，將邀約出席9/13(五) 媒合會現場面談，本實體活動為桃園市政府青年事務局之專案活動  1. 探針卡問題分析/排除 2. 探針卡驗證維修 3. 專案事項處理 4. 其他主管交辦事項  週40小時制(類做二休二)，約3~6個月輪調日夜 休假日加班優於勞基法全日以兩倍計算加班費。'
test4 = '職缺名稱: 機構工程師-擴編。工作地點: 桃園市龜山區龍校街121巷4弄9號。學歷要求: 專科。工作經歷: 經歷不拘。科系要求: 。公司名稱: 鑫宏益科技有限公司。公司產業類別: 其他電子零組件相關業。工作待遇: 月薪35,000元以上。更新日期: 20240826。工作內容: 系統產品之機構規劃相關作業，包含  1. 參與產品開發、研製工作、制定開發計畫。 2. 熟2D/3D繪圖軟體 (soildwork, ProE etc)。 3. 按照研發計畫完成技術文件,質量文件編制,並記錄各種工作要素編制完整的產品文件及技術標準之轉移。 4. 協助製造部門完成試產,處理試產中的設計問題, 並對生產過程中的技術、加工組裝方式有一定之指導權,並於試產後進行檢討。 5. 規劃與執行機構設計類產品BOM手稿提供與確認。 (零件承認、文件準備) 6. 執行機構設計類零部件結構/功能設計。(設計繪圖、設計驗證) 7. 協助業務部門解決技術問題。 8. 根據設計圖紙或產品樣本,完成新產品試制任務。 9. 負責開模前檢討並追蹤進度。 10. 負責研製新產品中有關的工裝治具。 11. 接受部門主管分配的專項任務或臨時性任務。  熟機械原理,注重外觀設計,細心為加分項目 歡迎符合條件者加入我們的團隊! 。'
query = '我畢業自機械科系，有學過機構學以及繪圖軟體'

print(embedding_model.compute_score([test3, query], weights_for_different_modes=[1, 1, 1]))
print(embedding_model.compute_score([test4, query], weights_for_different_modes=[1, 1, 1]))

