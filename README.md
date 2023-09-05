# THSR Ticket Booking System

This is a simple script to automate the booking process for Taiwan High-Speed Rail (THSR) tickets.

## Usage

1. Clone the repository using the following command:
   ```shell
   git clone https://github.com/Raito-95/THSR-Ticket.git
   ```

2. Navigate to the repository directory with the following command:
   ```shell
   cd THSR-Ticket
   ```

3. Install the required Python packages listed in requirements.txt by running the following command:

   ```shell
   python -m pip install -r requirements.txt
   ```

4. Run the script main.py with Python:
   ```shell
   python ./thsr_ticket/main.py
   ```

The script will guide you through the ticket booking process. You will be prompted to provide the following details:

**Start Station:** Please enter the station number where your journey begins. Valid inputs are integers from 1 to 12, corresponding to the following stations:

```
1  - Nangang
2  - Taipei
3  - Banqiao
4  - Taoyuan
5  - Hsinchu
6  - Miaoli
7  - Taichung
8  - Changhua
9  - Yunlin
10 - Chiayi
11 - Tainan
12 - Zuoying
```

**Destination Station:** Please enter the station number where your journey ends. Use the same station numbers as mentioned above.

**Date:** Please enter the date of your journey in the format YYYY-MM-DD.

**Time:** Please enter the time slot for your journey. There are 38 choices available, corresponding to the departure times listed below. The system will automatically select the earliest available train within the next 1 hour that has seats based on your input time.
```
1 -  12:01 AM
2 -  12:30 AM
3 -  06:00 AM
4 -  06:30 AM
5 -  07:00 AM
6 -  07:30 AM
7 -  08:00 AM
8 -  08:30 AM
9 -  09:00 AM
10 - 09:30 AM
11 - 10:00 AM
12 - 10:30 AM
13 - 11:00 AM
14 - 11:30 AM
15 - 12:00 PM
16 - 12:30 PM
17 - 01:00 PM
18 - 01:30 PM
19 - 02:00 PM
20 - 02:30 PM
21 - 03:00 PM
22 - 03:30 PM
23 - 04:00 PM
24 - 04:30 PM
25 - 05:00 PM
26 - 05:30 PM
27 - 06:00 PM
28 - 06:30 PM
29 - 07:00 PM
30 - 07:30 PM
31 - 08:00 PM
32 - 08:30 PM
33 - 09:00 PM
34 - 09:30 PM
35 - 10:00 PM
36 - 10:30 PM
37 - 11:00 PM
38 - 11:30 PM
```

**ID Number:** Please enter your identification number.

**Phone Number:** Please enter your contact phone number.

**Email Address:** Please enter your email address where the booking confirmation will be sent.

The script will validate your inputs to ensure they are in the correct format. If an input is invalid, you will be prompted to re-enter it. Once all the details are provided, the script will proceed to book your ticket.

Please note: This script is for demonstration purposes only. Ensure that you comply with the booking website's terms of use when using this script.

---

# 高鐵訂票小幫手

**!!--純研究用途，請勿用於不當用途--!!**

此程式提供另一種輕便的方式訂購高鐵車票，操作介面為命令列介面。相較於使用網頁訂購，本程式因為省卻了渲染網頁介面的時間，只保留最核心的訂購功能，因此能省下大量等待的時間。

## 執行

本程式由python語言所寫成，因此必須先安裝python才能夠使用。官方下載網址[點這裡](https://www.python.org/downloads/release/python-381/)

### 方法一 （快速）
在已經有安裝好python的環境下，執行以下指令
``` bash
pip install git+https://github.com/BreezeWhite/THSR-Ticket.git

# 執行
thsr-ticket
```

### 方法二
首先先將程式碼下載到本機，執行以下指令或是直接按右上方的下載按鈕

```
git clone https://github.com/BreezeWhite/THSR-Ticket.git
```

再來進入到資料夾中

```
cd thsr_ticket
```

安裝必要的套件

```
python -m pip install -r requirements.txt
```

最後執行程式

```
python thsr_ticket/main.py
```



## 注意事項!!!

本程式依舊有許多尚未完成的部分，僅具備基本訂購的功能，若是僅需要訂購成人票、且無特殊需求者，此程式對您而言是加速訂購流程的方便小工具。不符合以上描述者，目前仍建議使用官方網頁進行訂購。

#### 提供功能

- [x] 選擇啟程、到達站
- [x] 選擇出發日期、時間
- [x] 選擇班次
- [x] 選擇**"成人"**票數
- [x] 輸入驗證碼
- [x] 輸入身分證字號
- [x] 輸入手機號碼
- [x] 保留此次輸入紀錄，下次可快速選擇此次紀錄

#### 未提供功能

以下功能為未提供輸入的選項，但程式具備相關功能，可依照自身需求、對程式進行修改

- [ ] 選擇車廂種類(標準/商務)
- [ ] 座位喜好(靠窗/走道)
- [ ] 訂位方式(依時間搜尋車次/直接輸入車次號碼)
- [ ] 輸入孩童/愛心/敬老/學生優惠票數
- [ ] 僅顯示早鳥優惠票

#### 未完成功能

- [ ] 重新產生認證碼
- [ ] 語音播放認證碼
- [ ] 重新查詢車次
- [ ] 輸入護照號碼
- [ ] 輸入市話
- [ ] 輸入電子郵件
- [ ] 會員購票
