import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# 商品データの読み込み
df = pd.read_csv('sort_demo_shipment_result.csv', encoding="cp932")
df = df.iloc[:, [20, 40, 44, 47, 52]]


#出荷数を決めた関数の読み込み
df_func = pd.read_csv('demo_shipment_function.csv', header=None)
a = df_func.iloc[:, 0].values.T
b = df_func.iloc[:, 1].values.T
c = df_func.iloc[:, 2].values.T
d = df_func.iloc[:, 3].values.T
e = df_func.iloc[:, 4].values.T
# f = df_func.iloc[5].values.T
g = df_func.iloc[:, 6].values.T


for k in range(4):

    # 商品名
    prod = " Product" + str(k)

    # 抽出
    df_one = df[df["47"] == prod]
    df_one = df_one.loc[:,["40", "52"]]
    print(df_one)

    # 最初の出荷日
    initd = str(df_one["40"].min())
    initdate = datetime.date(int(initd[0:4]), int(initd[4:6]), int(initd[6:8]))

    #現在日
    now_date = datetime.date(2022, 10, 9)

    # 現在日との差日
    lenday = now_date - initdate

    # グラフ化データ
    data = np.zeros((lenday.days, 2))

    # 同じ日にちに出荷された出荷数を統合してデータに格納
    for i in range(lenday.days):

        # 調べる日にち
        date = initdate + datetime.timedelta(days=i)
        date_format = date.strftime("%Y%m%d")

        # 絞り込み
        df_samedate = df_one[df_one["40"] == int(date_format)]
        
        if df_samedate.empty:
            data[i] = [i, 0]
            continue

        data[i] = [i, df_samedate.iat[0,1]*df_samedate.shape[0]]
        
        
    plt.plot(data.T[0], data.T[1])
    

    
    # 関数の表示
    s = 2*data.T[0].max() #表示範囲
    x = np.linspace(0, s, 1000)
    func = a[k] + b[k]*np.sin(c[k]*x*(g[k]/data.T[0].max())) + d[k]*np.cos(e[k]*x*(g[k]/data.T[0].max()))
    plt.plot(x, func)

    plt.show()
     









