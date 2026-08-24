"""
## 情境說明

你正在製作一個便利商店自助結帳系統。顧客可以把商品加入購物車、查看購物車、移除商品，最後結帳產生訂單檔案。

訂單檔案會儲存在 `orders` 資料夾中。程式需能列出目前有哪些訂單 CSV，並讀取指定訂單顯示在螢幕上。
"""
import csv
import os
from datetime import datetime

ORDER_DIR = "orders"

# --- 目錄 ---
catalog = {
    "御飯糰": 35,
    "礦泉水": 20,
    "布丁": 25,
    "關東煮": 15,
    "飯糰": 30,
}


cart = {} # 空字典


# --- 啟動時檢查訂單資料夾是否建立 ---
try:
    if not os.path.exists("orders"):
        os.makedirs("orders")
        print("已建立 orders 資料夾")
except OSError as error:
    print(f"建立資料夾失敗：{error}")


# --- 建立使用者介面 ---
while True:
    print(f"{' 便利商店購物車訂單系統 ':=^25}")
    print("1. 顯示商品目錄")
    print("2. 新增商品到購物車")
    print("3. 移除購物車商品")
    print("4. 查看購物車")
    print("5. 結帳並產生 CSV 訂單")
    print("6. 列出訂單檔案")
    print("7. 讀取訂單 CSV")
    print("0. 離開")

    choice = input("請選擇：").strip()
    
    if choice == "0":
        break # 不然會有無限迴圈
    if choice == "1":
        print(f"{' 商品目錄 ':=^18}")
        for name, price in catalog.items():
            if len(name) == 2: # 如果名稱是兩個字
                display_name = name + "　"  # 兩個自加空格，統一是三個字
            else:
                display_name = name
            print(f"{display_name:10}{price:>3} 元")

    if choice == "2":
        print("新增商品到購物車: ")
        print(catalog)
        pname = input("請輸入商品名稱(輸入商品名稱要完全一致): ").strip()
        if pname not in catalog:
            print("\n商品名稱不存在，請重新輸入！\n")
        else:
            try:
                qty = int(input("請輸入數量: "))
                
                if qty <= 0: # 數量必是正整數
                    print("\n數量必須大於 0\n")
                else:
                    print(f"輸入數量：{qty}")
                    cart[pname] = cart.get(pname, 0) + qty # 寫入購物車pname當作key => 產品名稱要用唯一值 - 品號
                    print("\n已放入購物車！\n")
            except ValueError:
                print("\n數量必須是整數\n")

    if choice == "3":
        pname = input("請輸入你要移除的商品: ")
        if pname in cart:
            del cart[pname]
            print("\n商品已移除！\n")
        else:
            print("\n商品不存在，請重新輸入！\n")

    if choice == "4":
        if not cart:
            print("\n購物車是空的，請重新輸入!\n")
        else:
            print(f"\n{' 購物車 ':=^17}") # 迴圈外
        
            total = 0 #初始值
            for name ,qty in cart.items(): # 因為會加入一個以上的商品 => 用迴圈
                price = catalog[name]
                subtotal = catalog[name] * qty
                total += subtotal # 把每一項商品的小計加進總金額
                print(f"{name}    {price:,} 元 x {qty} = {subtotal:,} 元") # 迴圈內商品明細
            print("-" * 17) # 迴圈外
            print(f"總金額: {total:,} 元\n") # 迴圈外

    if choice == "5":
        # 結帳並產生CSV訂單
        print("檢查購物車內容:", cart)
        if not cart:
            print("\n購物車是空的，不可結帳！\n")
        else:
            # 訂單檔名
            order_time = datetime.now().strftime("%Y%m%d_%H%M%S") # 購物車有東西，開始抓現在的時間
            filename = f"order_{order_time}.csv" # 組合出老師要求的檔名
            filepath = os.path.join("orders", filename) # 把資料夾路徑與檔名組合在一起
            print(f"\n準備寫入檔案，路徑為: {filepath}\n") # 測試路徑是否正確
            
            # 寫入CSV範例
            try:
                with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
                    writer = csv.writer(file)
                    writer.writerow(["訂單時間", "商品名稱", "單價", "數量", "小計"])
                    current_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 動態寫入購物車真實資料
                    for name, qty in cart.items():
                        price = catalog[name]
                        subtotal = price * qty
                        writer.writerow([current_time_str, name, price, qty, subtotal])
                    
                print(f"訂單已建立：{filepath}")
            except OSError as error:
                print(f"寫入訂單失敗：{error}")

    if choice == "6":
        # 列出訂單檔案
        try:
            files = os.listdir("orders")
            csv_files = []

            for file_name in files:
                if file_name.endswith(".csv"):
                    csv_files.append(file_name)
            
            if not csv_files:
                print("目前沒有任何訂單檔案")
            else:
                for file_name in csv_files:
                    print(file_name)
        except OSError as error:
            print(f"讀取訂單資料夾失敗：{error}")

    if choice == "7":
        # 讀取指定訂單CSV並顯示
        print("\n--- 讀取指定訂單 ---")
        target_file = input("請輸入要讀取的訂單檔名 (例如order_20260519_114210.csv)：").strip()
        try:
            with open(filepath, "r", encoding="utf-8-sig") as file:
                reader = csv.reader(file)
                
                for row in reader:
                    print(row)
        except FileNotFoundError:
            print("找不到指定的訂單檔案")
        
        except OSError as error:
            print(f"讀取訂單失敗：{error}")
