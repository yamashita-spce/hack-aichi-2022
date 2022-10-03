#demo_shipment_results
# 出荷実績データの作成
import pandas as pd
import numpy as np
import random
import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt


# 地域(人口比で分けられる衆議院比例区を参照)
region = ["北海道", "東北", "北関東","南関東", "東京", "東京", "北陸信越", "東海", "近畿", "近畿", "中国", "四国", "九州"]

# 商品データの読み込み
df_none = pd.read_csv('dummy_product_master.csv', header=None)

code = df_none.iloc[:,1].values.T
name = df_none.iloc[:, 6].values.T #注文サイト品名
inventory = df_none.iloc[:, 44].values.T
fdate = df_none.iloc[:, 68].values.T
fdate = fdate.astype("str")

# 総データ数統計
n = 0

f = open("demo_shipment_result.csv", "w", encoding='shift_jis') #商品マスタデータ
func_f = open("demo_shipment_function.csv", "w")

# 最初の出荷日の初期値（最大を４年前とする）
initdate = datetime.date(2018, 1, 1)

# 当日の日にち
nowdate = datetime.date(2022, 10, 9)

ber = tqdm(total = len(code))
for i in range(len(code)):

    if fdate[i] != "nan":
        # 販売終了日をdate型に変換
        fdate_date = datetime.date(int(fdate[i][0:4]), int(fdate[i][4:6]), int(fdate[i][6:8]))
        # 販売終了日の１００日前以上になるようにする(あまりにも日数が少ないと予期せぬ購入量になりえるため)
        dif = fdate_date - initdate
    else:
        dif = nowdate - initdate

    # 最初の出荷日を決定   
    idate = initdate + datetime.timedelta(days=random.randint(1, int(dif.days) - 100))

    # 出荷されてから、販売終了時もしくは現在までの経過日数
    if fdate[i] != "nan":
        proday = fdate_date - idate
    else:
        proday = nowdate - idate

    # 商品に対する出荷度合をランダムに生成
    d = random.randint(int(proday.days / 10), proday.days*2)
    
    
    # 商品の出荷個数グラフをランダム作成
    x = np.linspace(0, random.uniform(np.pi, 2*np.pi), proday.days)
    sd = random.uniform(0, random.randint(1, 300))
    sc = random.uniform(0, random.randint(1, 300))
    fsin = random.uniform(-2, 2)
    fcos = random.uniform(-2, 2)
    func = sd + sc + sd*np.sin(fsin*x) + sc*np.cos(fcos*x)
    if i < 4:
        plt.plot(x, func)
        plt.show()

    # 関数の保存
    if i < 4:
        #４商品の関数を保存
        # f(τ) = %f + %f×sin(%fτ) + %f×cos(%fτ)の係数を保存
        print("%f,%f,%f,%f,%f,%f,%f" %(sd+sc, sd, fsin, sc, fcos, x[0], x[-1]), file=func_f)
    
    # 出荷日のランダム生成
    ship_datelist = np.zeros(d)
    daylist = np.array([random.randint(0, proday.days - 1) for j in range(d)])
    # print(daylist)

    for j in range(d):
        ship_date = idate + datetime.timedelta(days=int(daylist[j]))
        ship_datelist[j] = int(ship_date.strftime("%Y%m%d"))

    # print(ship_datelist)


    # 出荷データを作成
    for j in range(proday.days):
        
        # この日の出荷数をランダムに発生
        date_format = idate + datetime.timedelta(days=j)
        date_format = date_format.strftime("%Y%m%d")
        
        nn = len(np.where(ship_datelist == int(date_format))[0])
        if nn == 0:
            nn = 1

        for k in range(nn):
             
            # 出荷数量
            Number_of_shipment = int(func[j] / nn) + random.randint(int(-func[j]/(nn*4)), int(func[j]/(nn*4)))

            # 配送地域
            pregion = region[random.randrange(12)]
        
            print('"","","","","","","","","","","","","","","","","","","","","' + pregion + '","","","","","","","","","","","","","","","","","","","","' + date_format +'","","","","' + code[i] + '","",""," ' + name[i] + '","","","","","' + str(Number_of_shipment) +'"', file=f)
            n += 1

    ber.update(1)

f.close()
func_f.close()

# できたデータを日付順にソート
df_new = pd.read_csv('demo_shipment_result.csv', header=None, encoding="cp932")
df_new = df_new.sort_values(by=40, ascending=False)
df_new.to_csv("sort_demo_shipment_result.csv", index=False, encoding="cp932")

print(n)