# 合理房價預估

此專案為台北市中山區房價預測，由於台北市各區房價分散，因此將範圍縮小為中山區，提高模型準確性。


## 使用套件及工具
* Python
* Pandas
* Dash
* Plotly
* Bootstrap
* Orange Data Mining


## 作業流程
1. [獲取資料](#data)
2. [資料工程](#data_cleaning)
3. [模型建置](#Model)
4. [網頁視覺化呈現](#dash)

<a name="data"></a>
### 1. 獲取資料
    1.1 於實價登錄網站上下載不動產成交案件資料【台北市107年~112年第二季資料】，共13萬筆資料，欄位包括交易日期、建物型態、土地位置建物門牌、土地移轉總面積平方公尺...等34欄。
    
    1.2 於政府資料開放平台取得捷運站、超商、醫院、警察局、殯儀館及寺廟等設施資料。


<a name="data_cleaning"></a>
### 2. 資料工程
    2.1 數據清理：
        * 僅保留中山區資料，並刪除非相關資料。
        * 切割交易日期為三欄(交易年、交易月、交易日)，並刪除不正常日期資料。

    2.2 資料補空值：
        將'總樓層數'為五層以下的'電梯'欄位填充為'無'，其餘填充'有'。
        
    2.3 擴增資料：
        * 新增'建物坪數'欄位，由原始資料中'建物移轉總面積平方公尺'計算；並計算'單坪價格'。
        * 將'路名'由房屋地址中切片提出。
        * 由另一份資料表中取得'屋齡'及'建築完成日期'。
        * 將房屋地址進行爬蟲取得經緯度及郵遞區號，並計算各設施距離(捷運站、超商、醫院、警察局、殯儀館及寺廟等設施)。
        將上述資料添加至原資料中，供後續模型建置使用。

    2.4 數據轉換：
        將房屋總價資料取log，使其呈現常態分布，並刪除離群值，進而提升模型的預測效能。
| ![image](https://github.com/sylvia1830/House-price/assets/137684401/0229e765-45e5-462f-a348-21052de31ce1) | ![image](https://github.com/sylvia1830/House-price/assets/137684401/02eeac1d-c48a-476d-9333-4d5ca6d31c25) |
|:-----------------------------------:|:------------------------------------:|


    2.5 資料離散化：
        使用Orange Data Mining工具，將移轉層次分為低中高樓層，建物坪數、屋齡以區間表示。
<img src="https://github.com/sylvia1830/House-price/assets/137684401/e53d67d3-8566-4b64-a34d-cddc2e4ce4f0" alt="image" width="400">

| ![image](https://github.com/sylvia1830/House-price/assets/137684401/23dc085a-7af6-4975-a27e-e406fc13c4cf) | ![image](https://github.com/sylvia1830/House-price/assets/137684401/66326c62-ec43-4570-86ec-e56a5572af02) |
|:-----------------------------------:|:------------------------------------:|

    2.6 以Spearman Correlation(斯皮爾曼相關係數)，查看各項設施與房屋總價相關性：
        發現各設施與房價為弱正相關，且關聯程度皆並不高，因此附近設施將不列入接下來的建置模型參數中。
| ![image](https://github.com/sylvia1830/House-price/assets/137684401/8af9493c-e65c-4d35-a17e-aaa43652a371) | ![image](https://github.com/sylvia1830/House-price/assets/137684401/0cd927ef-f0d3-4232-9cef-c23edf759e8a) |
|:-----------------------------------:|:------------------------------------:|

    
    
    

<a name="Model"></a>
### 3. 模型建置(Orange Data Mining)
<img src="https://github.com/sylvia1830/House-price/assets/137684401/0fdac221-cdfe-44bb-b761-f3eecd6c8fe3" alt="image" width="900">

    3.1 選擇建置模型所需參數
<img src="https://github.com/sylvia1830/House-price/assets/137684401/3299c06e-975c-43ab-95e4-d6e3c82efdc7" alt="image" width="200">


    3.2 拆分資料：
        以stratify sample(分層抽樣)方式，將資料拆分為訓練資料(80%)及測試資料(20%)。
<img src="https://github.com/sylvia1830/House-price/assets/137684401/66ebaa33-f390-4808-a92f-49148ed6789c" alt="image" width="200">



    3.3 將訓練資料以線性回歸建置模型：
<img src="https://github.com/sylvia1830/House-price/assets/137684401/ab176a89-792a-4434-9756-5f44f394ec08" alt="image" width="250">


    3.4 模型訓練結果：
<img src="https://github.com/sylvia1830/House-price/assets/137684401/b9573bad-7497-4c49-9846-a6500aefcff9" alt="image" width="400">


    3.5 將測試資料放入模型，查看預測結果：
![image](https://github.com/sylvia1830/House-price/assets/137684401/ec510130-fcc0-4484-8dbd-104c2091a439)

<img src="https://github.com/sylvia1830/House-price/assets/137684401/0e6089f1-274d-4bd6-b233-01282f2fca60" alt="image" width="600">


    3.6 匯出模型，供前端網頁使用。



<a name="dash"></a>
### 4. 網頁視覺化呈現(Python Dash)
將Orange建置完成模型導入Python中，以Python Dash呈現房價預估使用者介面。

https://github.com/sylvia1830/House-price/assets/137684401/f6b63402-d38f-404d-a294-9bedbc5b67ca






## 資料來源
* 內政部不動產成交案件(https://plvr.land.moi.gov.tw/DownloadOpenData)  
* 政府資料開放平台(https://data.gov.tw/)
    
