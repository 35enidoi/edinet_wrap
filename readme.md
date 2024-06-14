# 説明
EDINET APIのラッパーです。  
# 使い方
```py
from edinet import Edinet
from datetime import datetime
import json


# APIのトークン
API_TOKEN = "your token here"

# init時にAPIキーが必要なので注意。
edn = Edinet(API_TOKEN)

# ドキュメントを取得
doc_list = edn.get_document_list(datetime.today(), type_=2)

# 会社別の提出書のリスト
# 提出書の種類、EDINET ID、証券コード
documents_class_by_filer: dict[str, list[tuple[str, str, str]]] = {}

for i in doc_list["results"]:
    # 縦覧できる事を確認
    if i["legalStatus"] != 0:
        # もし変数の中に登録されてない場合、作成。
        if not documents_class_by_filer_name.get(i["filerName"]):
            documents_class_by_filer_name[i["filerName"]] = []
        # 追加
        documents_class_by_filer_name[i["filerName"]].append((
            i["docDescription"],
            i["docID"],
            i["secCode"]
        ))

# 保存する
with open("documents.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(documents_class_by_filer_name,
                       indent=4,
                       ensure_ascii=False))

```
