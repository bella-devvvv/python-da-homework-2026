"""
M6 Plotly 互動儀表板 & Capstone — 課後作業
===========================================
情境：從原始資料到互動式儀表板，完成完整的資料分析 pipeline。

資料路徑：
  - datasets/ecommerce/orders_raw.csv（原始髒資料）
  - datasets/ecommerce/customers.csv
  - datasets/ecommerce/products.csv
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ============================================================
# 🟢 送分題（每題 10 分，共 30 分）
# ============================================================

def green_plotly_bar():
    """
    用 Plotly Express 畫出每個商品類別 (category) 的總營收長條圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.bar()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("../datasets/ecommerce/orders_enriched.csv")

    category_revenue = df.groupby("category")["amount"].sum().reset_index().rename(
        columns={"amount" : "revenue"}
    )

    fig = px.bar(category_revenue,
                x = "category",
                y = "revenue", 
                )
    return fig
    pass


def green_plotly_line():
    """
    用 Plotly Express 畫出月營收趨勢折線圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：先 groupby 月份算總營收，再 px.line()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("../datasets/ecommerce/orders_enriched.csv")
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    monthly_revenue = df.groupby("month")["amount"].sum().reset_index().rename(columns={"amount" : "revenue"})
    fig = px.line(monthly_revenue, x = "month", y = "revenue", markers = "o")
    return fig
    pass


def green_plotly_pie():
    """
    用 Plotly Express 畫出 VIP 等級 (vip_level) 的訂單數佔比圓餅圖
    資料來源：orders_enriched.csv
    回傳 plotly Figure 物件
    提示：px.pie()
    """
    # TODO: 你的程式碼
    df = pd.read_csv("../datasets/ecommerce/orders_enriched.csv")
    
    vip_order_count = df["vip_level"].value_counts().reset_index().rename(columns={"count" : "order_count"})

    fig = px.pie(vip_order_count, names="vip_level", values="order_count")
    return fig
    pass


# ============================================================
# 🟡 核心題（每題 15 分，共 45 分）
# ============================================================

def yellow_clean_and_merge(raw_path, customers_path, products_path):
    """
    完整 ETL：從髒資料到合併完成的 DataFrame
    1. 讀取 orders_raw.csv 並清理（欄位名稱、金額、日期、缺值、去重）
    2. 合併 customers.csv 和 products.csv
    回傳：合併後的 DataFrame
    """
    # TODO: 你的程式碼
    orders = pd.read_csv(raw_path)
    customers = pd.read_csv(customers_path)
    products = pd.read_csv(products_path)
    orders.columns = orders.columns.str.strip().str.lower()

    orders["amount"] = (
        orders["amount"]
        .astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
    )

    orders["amount"] = pd.to_numeric(orders["amount"], errors="coerce")
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")

    orders = orders.dropna(subset=["amount", "order_date", "qty"])
    orders = orders.drop_duplicates()

    new_df = pd.merge(orders, customers, on="customer_id", how="left")
    new_df = pd.merge(new_df, products, on="product_id", how="left")

    return new_df
    pass


def yellow_kpi_summary(df):
    """
    計算 4 個核心 KPI，回傳 dict：
    {
        "total_revenue": float,       # 總營收
        "order_count": int,           # 訂單數
        "active_customers": int,      # 不重複客戶數
        "avg_order_value": float,     # 平均客單價
    }
    """
    # TODO: 你的程式碼
    total_revenue = df["amount"].sum()
    order_count = len(df)
    active_customers = df["customer_id"].nunique()
    avg_order_value = total_revenue / order_count

    return {
        "total_revenue": float(total_revenue),
        "order_count": int(order_count),
        "active_customers": int(active_customers),
        "avg_order_value": float(avg_order_value),
    }
    pass


def yellow_plotly_scatter(df):
    """
    用 Plotly Express 畫互動散佈圖：
    - X：商品單價 (unit_price)
    - Y：訂單金額 (amount)
    - 顏色：商品類別 (category)
    - hover 顯示：商品名稱 (product_name)
    回傳 plotly Figure 物件
    提示：px.scatter(hover_data=['product_name'])
    """
    # TODO: 你的程式碼
    fig = px.scatter(data_frame = df, x = "unit_price", y = "amount", color="category", hover_data=['product_name'] )
    return fig
    pass


# ============================================================
# 🔴 挑戰題（25 分）
# ============================================================

def red_dashboard():
    """
    Capstone：完整的互動式儀表板

    流程：
    1. 清理 orders_raw.csv + 合併三張表
    2. 建立 2×2 subplot dashboard（用 plotly make_subplots）：
       - 左上：月營收趨勢 (line)
       - 右上：Top 10 商品營收 (bar)
       - 左下：各地區營收 (bar)
       - 右下：類別營收佔比 (pie/donut)
    3. 設定整體標題

    回傳 plotly Figure 物件
    提示：from plotly.subplots import make_subplots
    """
    # TODO: 你的程式碼
    orders = pd.read_csv("../datasets/ecommerce/orders_raw.csv")
    customers = pd.read_csv("../datasets/ecommerce/customers.csv")
    products = pd.read_csv("../datasets/ecommerce/products.csv")
    orders.columns = orders.columns.str.strip().str.lower()
    orders["amount"] = orders["amount"].str.replace("$","",regex=False).replace(",","",regex=False).astype(float, errors = "coerce")
    orders["order_Date"] = pd.to_datetime(orders["order_Date"], errors = "coerce")
    orders = orders.dropna(subset=["amount", "order_date","qty"])
    orders = orders.drop_duplicates()
    df = pd.merge(orders, customers, on="customer_id", how="left")
    df = pd.merge(df, products, on="product_id", how="left")

    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    month_revenue = df.groupby("month")["amount"].sum().reset_index().rename(columns={"amount" :"revenue"})

    top10_products = df.groupby("product_name")["amount"].sum().reset_index().rename(columns ={"amount" : "revenue"} ).sort_values("revenue",ascending=False).head(10)

    region_revenue = (df.groupby("region")["amount"]
    .sum()
    .reset_index()
    .rename(columns ={"amount" : "revenue"})    
    )

    category_revenue = (
    df.groupby("category")["amount"]
    .sum()
    .reset_index()
    .rename(columns={"amount": "revenue"})
)
    fig = make_subplots(
        rows = 2,
        cols = 2,
        subplot_titles=[
        "月營收趨勢",
        "Top 10 商品營收",
        "各地區營收",
        "類別營收佔比"
    ],
        specs = [
            [("type" : "xy"), {"type" : "xy"}],
            [("type" : "xy"), {"type" : "domain"}],
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=month_revenue["month"],
            y=month_revenue["revenue"],
            mode="lines+markers",
            name="月營收"
        ),
        row=1,
        col=1
    )

    fig.add_trace(
        go.Bar(
            x=top10_products["product_name"],
            y=top10_products["revenue"],
            name="Top 10 商品營收"
        ),
        row=1,
        col=2
    )

    fig.add_trace(
        go.Bar(
            x=region_revenue["region"],
            y=region_revenue["revenue"],
            name="各地區營收"
        ),
        row=2,
        col=1
    )

    fig.add_trace(
        go.Pie(
            labels=category_revenue["category"],
            values=category_revenue["revenue"],
            hole=0.4,
            name="類別營收佔比"
        ),
        row=2,
        col=2
    )

    fig.update_layout(
        title_text="E-commerce 互動式營運儀表板",
        height=800,
        showlegend=True
    )

    return fig
    pass
