from dash import Dash, html, dcc, callback, Output, Input, State, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import pickle
import Orange
import math

df = pd.read_csv('./ZS_final.csv')

# app = Dash(__name__)
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY])

# server = app.server

# ======CSS=========================================

# 下拉式選單css
Dropdown_style = {
    'width':'100%', 
    'margin-right': '5px',
    'height':'40px'
}

input_2_style = {
    'width':'190px', 
    'margin-right': '5px',
    'height':'40px'
}


# =====版面=========================================
app.layout = html.Div([
    dcc.Location(id='url'),  # 用來監聽網址的變化
    dbc.NavbarSimple(
        # children=[
        #     dbc.NavItem(dbc.NavLink("Page 1", href="./畫圖.py")),  
        #     dbc.DropdownMenu(
        #         children=[
        #             dbc.DropdownMenuItem("More pages", header=True),
        #             dbc.DropdownMenuItem("Page 2", href="#"),
        #             dbc.DropdownMenuItem("Page 3", href="#"),
        #         ],
        #         nav=True,
        #         in_navbar=True,
        #         label="More",
        #     ),
        # ],
        
        brand="House Price 中山區房價預測",
        brand_href="#",  #回首頁(重置按鈕)
        color="primary",
        dark=True,
        style={'position': 'fixed',
               'z-index': '1000',
               'top': '0',
               'width': '100%'}
    ),
    html.Br(),

    html.Div([
    html.H4(children='房屋條件：',
            style= {'padding-top': '56px'}),
    # 下拉式選單
    html.Div([
        dcc.Dropdown(id = 'road-dropdown',
            options= df['路名'].unique(),
            placeholder='街道路名',
            style = Dropdown_style  
        ),
        dcc.Dropdown(id = 'building-dropdown',
            options={
                '住宅大樓(11層含以上有電梯)':'住宅大樓(11層含以上)',
                '華廈(10層含以下有電梯)': '華廈(10層含以下)',
                '公寓(5樓含以下無電梯)': '公寓(5樓含以下)',
                '套房(1房1廳1衛)' : '套房(1房1廳1衛)',
                '透天厝' :'透天厝'
            },
            placeholder='建物型態',
            style = Dropdown_style 
        ),
        dcc.Dropdown(id = 'floor-dropdown',
            options={
                '低樓層':'低樓層(5層以下)',
                '中樓層':'中樓層(6~10層)',
                '高樓層':'高樓層(11層以上)',
            },
            placeholder='樓層',
            style = Dropdown_style  
        ),
        dcc.Dropdown(id = 'age-dropdown',
            options = {
                '< 5':'< 5年',
                '5 - 10':'5 - 10年',
                '10 - 20':'10 - 20年',
                '20 - 30':'20 - 30年',
                '30 - 40':'30 - 40年',
                '40 - 50':'40 - 50年',
                '50 - 60':'50 - 60年',
                '≥ 60':'≥ 60',
            },
            placeholder='屋齡',
            style = Dropdown_style  
        ),
        dcc.Dropdown(id = 'elevator-dropdown',
            options={
                '有':'有電梯',
                '無':'無電梯',
            },
            placeholder='電梯',
            style = Dropdown_style 
        ),
        dcc.Dropdown(id = 'parking-dropdown',
            options={
                '有':'有車位',
                '無':'無車位',
            },
            placeholder='車位',
            style = Dropdown_style
        ),              
    ], style={'display': 'flex'}),

    html.Div([
        html.Label('實際坪數：'),
        dcc.Input(
            id='area_number', 
            type='number',    # 设置输入框的类型为数字
            placeholder='請輸入',  # 提示用户输入内容
            min=0,            # 设置允许输入的最小值
            max=1000,         # 设置允许输入的最大值
            value='',          # 设置默认值为空
            style = input_2_style
        ),
        dcc.Dropdown(id = 'area-dropdown',
            options = {
                '< 10':'< 10坪',
                '10 - 20':'10 - 20坪',
                '20 - 30':'20 - 30坪',
                '30 - 40':'30 - 40坪',
                '40 - 50':'40 - 50坪',
                '50 - 60':'50 - 60坪',
                '60 - 80':'60 - 80坪',
                '80 - 100':'80 - 100坪',
                '≥ 100':'≥ 100坪'
            },
            placeholder='坪數',
            style = input_2_style
        ),
        
    ], style= {'padding-top': '8px',
               'display': 'flex',}),

    

    
    html.Br(),

    # 房價預估按鈕
    dbc.Button("房價預估", id='forecast_button', color="primary",
               className="d-grid gap-2 col-6 mx-auto"
               ),
    html.Br(),

    html.Div(id='forecast_result'),  #預測結果
    
    html.Br(),

    html.H5('歷史成交物件：'),

    html.Div(id='table-container'),
    
    
    ], style={'margin': '0 auto', 'width': '90%'}),
    
], style={'backgroundColor': ''})



# =========@callback===================================================

# 選單鎖定------------------
@app.callback(
    Output('elevator-dropdown', 'value'),
    Output('elevator-dropdown', 'disabled'),
    [Input('building-dropdown', 'value')]
)
def lock_elevator(building_value):
    if building_value in ['住宅大樓(11層含以上有電梯)', '華廈(10層含以下有電梯)']:
        return '有', True  
    if building_value in ['公寓(5樓含以下無電梯)']:
        return '無', True  #True禁用下拉式選單
    else:
        return None, False
    
@app.callback(
    Output('floor-dropdown', 'value'),
    Output('floor-dropdown', 'disabled'),
    [Input('building-dropdown', 'value')]
)
def lock_floor(building_value):
    if building_value in ['公寓(5樓含以下無電梯)']:
        return '低樓層', True  
    else:
        return None, False
    
# 坪數對應鎖定------------------
@app.callback(
    Output('area-dropdown', 'value'),
    Output('area-dropdown', 'disabled'),
    [Input('area_number', 'value')]
)
def update_area_dropdown(value):
    if value is not None and value != '':
        value = float(value)
        if value < 10:
            return '< 10', True
        elif 10 <= value < 20:
            return '10 - 20', True
        elif 20 <= value < 30:
            return '20 - 30', True
        elif 30 <= value < 40:
            return '30 - 40', True
        elif 40 <= value < 50:
            return '40 - 50', True
        elif 50 <= value < 60:
            return '50 - 60', True
        elif 60 <= value < 80:
            return '60 - 80', True
        elif 80 <= value < 100:
            return '80 - 100', True
        else:
            return '≥ 100', True
    else:
        return None, False

    

# 房價預測-------------------
@callback(
    Output('forecast_result', 'children'),
    [Input('forecast_button', 'n_clicks')],
    [State('road-dropdown', 'value'),
     State('building-dropdown', 'value'),
     State('floor-dropdown', 'value'),
     State('area-dropdown', 'value'),
     State('age-dropdown', 'value'),
     State('elevator-dropdown', 'value'),
     State('parking-dropdown', 'value'),
     State('area_number', 'value')]    
)

def house_forecast(n_clicks, road_values, building_values, floor_values, area_values, age_values, elevator_values, parking_values, area_number_value):

    if n_clicks is None:
        return None
    
    elif None in [road_values, building_values, floor_values, area_values, age_values, elevator_values, parking_values, area_number_value]:
        return html.H4("請輸入完整房屋條件再進行預估!",
                       style={"text-align": "center",
                              "color": "red"}
                       )
    
    else:
        # 導入orange模型
        with open('.\model\house_model0816.pkcls', 'rb') as f:
            model = pickle.load(f)

        input_data = {
            '交易年': [2023],
            '路名': [road_values],
            '建物型態': [building_values],
            '移轉層次(區間)': [floor_values],
            '建物坪數(區間)': [area_values],
            '交易時屋齡(區間)': [age_values],
            '電梯': [elevator_values],
            '車位有無': [parking_values],
            '建物坪數': [area_number_value]
        }

        input_df = pd.DataFrame(input_data)

        input_df.to_csv('./csv/input_data.csv', index=False)

    
        # # 加载待预测的數據
        indata = Orange.data.Table('./csv/input_data.csv')

        # # 使用模型進行預測
        predictions = model(indata)

        # log值轉換回原本金額
        price = round(math.exp(predictions), 2)
        unit_price = round(price/area_number_value, 2)

        return html.Div([
            html.H5('合理成交價預估：'),
            html.Hr(style={"border": "1px solid green"}),
            html.H5(f"{price} 萬元"),
            html.H5(f"{unit_price} 萬元/坪"),

            # html.Div(f"輸入的實際坪數為: {area_number_value} 坪"),

        ], style={'border': '2px solid green',
                  'border-radius': '10px',     # 圓角半徑：10px
                  'padding': '20px',           # 內邊距：20px
                  'margin': '0 auto',
                  'width': '50%',
                  "text-align": "center"
    })


# 歷史成交物件table-------------------
@callback(
    Output('table-container', 'children'),
    Input('road-dropdown', 'value'),
    Input('building-dropdown', 'value'),
    Input('floor-dropdown', 'value'),
    Input('area-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('elevator-dropdown', 'value'),
    Input('parking-dropdown', 'value')
)

def update_table(road_values, building_values, floor_values, area_values, age_values, elevator_values, parking_values):
    filtered_df = df.copy()

    # 篩選資料條件
    if road_values:
        filtered_df = filtered_df[filtered_df['路名'] == road_values]

    if building_values:
        filtered_df = filtered_df[filtered_df['建物型態'] == building_values]

    if floor_values:
        filtered_df = filtered_df[filtered_df['移轉層次(區間)'] == floor_values]

    if area_values:
        filtered_df = filtered_df[filtered_df['建物坪數(區間)'] == area_values]

    if age_values:
        filtered_df = filtered_df[filtered_df['交易時屋齡(區間)'] == age_values]

    if elevator_values:
        filtered_df = filtered_df[filtered_df['電梯'] == elevator_values]

    if parking_values:
        filtered_df = filtered_df[filtered_df['車位有無'] == parking_values]


    # 資料表將呈現的欄位
    columns_to_display = ['交易年', '交易月', '總價(萬元)', '單坪價格(萬元)', '土地位置建物門牌', '建物型態', '移轉層次', '建物坪數', '交易時屋齡', '電梯', '車位有無']
    filtered_df = filtered_df[columns_to_display]

    if filtered_df.empty:  # 確認是否有符合條件的資料
        return html.Div("無此條件之歷史物件")
    else:
        table = dash_table.DataTable(
            data=filtered_df.to_dict('records'),
            page_size=5,
            style_table={"overflowX": "auto", "padding": "15px"},
            style_cell={
                "padding": "5px",
                "height": "60px",
                "minWidth":"70px",
                "width": "auto",
                "maxWidth": "190px",  
                "whiteSpace": "normal",  #文字自動換行
            },
            sort_action='native', #使用者自行調整排序

        )
        return table







if __name__ == '__main__':
    app.run(debug=True)