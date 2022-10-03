#create_product_master_data
#商品マスタCSVのデモデータの作成
#2018~2022年度のデータの作成

import random
import string
import time
import datetime

N = 30

#商品コードの生成する関数
def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

f = open("dummy_product_master.csv", "w")

# 販売終了日初期データ
indate = datetime.date(2019, 10, 1)


# ハッカソン当日date
nowdate = datetime.date(2022, 10, 9)

for i in range(N):

    if i < 4:
        pdate = indate + datetime.timedelta(days=5000)
    else:
        pdate = indate + datetime.timedelta(random.randint(0, 5000))
        
    date_format = pdate.strftime("%Y%m%d")
    if pdate > nowdate:
        date_format = ""

# 商品コード（４０桁）の生成
    pcode = randomname(40)
# 倉庫システム品名（注文サイト品名は同じ）
    name = "Product" + str(i)

# 現時点の在庫数
    Inventory = random.randrange(10, 1000, 1)
    if pdate <= nowdate:
        Inventory = 0

    print('"","' + pcode + '","","","","","' + name + '","' + name + '","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","' + str(Inventory) + '","","","","","","","","","","","","","","","","","","","","","","","","' + date_format +'"', file=f)

f.close()
print("実行完了")


# 曜日
# def what_day_is_it(date):
#     days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
#     day = date.weekday()
#     print(days[day])

# what_day_is_it(date(int(fdate[0:4]), int(fdate[4:6]), int(fdate[6:8])))
    
    