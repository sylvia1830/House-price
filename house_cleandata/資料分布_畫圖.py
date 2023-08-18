import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# df = pd.read_csv('./ZS_原資料log.csv')
df = pd.read_csv('./ZS_final.csv')


# 欄位名稱
column_names = ['總價(萬元)log','總價(萬元)', '單坪價格(萬元)', '交易時屋齡', '建物坪數']

# 創建子圖表
fig = make_subplots(rows=2, cols=len(column_names),
                    subplot_titles=column_names,
                    vertical_spacing=0.2)

# 添加盒狀圖和分布圖到子圖表
for i, column in enumerate(column_names):
    # 繪製盒狀圖
    fig.add_trace(go.Box(y=df[column], name=column), row=1, col=i+1)

    # 繪製分布圖
    fig.add_trace(go.Histogram(x=df[column], name=column), row=2, col=i+1)

# 設置圖表佈局
fig.update_layout(title='調整後資料分布情形',
                   height=600, width=900)

# 顯示圖表
fig.show()
