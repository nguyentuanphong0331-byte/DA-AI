import pandas as pd

INPUT = "web_traffic(1).csv"
OUTPUT = "web_traffic_cleaned.csv"

df = pd.read_csv(INPUT)

# 1. Chuẩn hóa tên cột
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(r"[^\w]+", "_", regex=True)
    .str.strip("_")
)

# 2. Chuẩn hóa kiểu dữ liệu
df["date"] = pd.to_datetime(df["date"], errors="coerce")

numeric_cols = [
    "sessions", "unique_visitors", "page_views",
    "bounce_rate", "avg_session_duration_sec"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["traffic_source"] = (
    df["traffic_source"].astype("string")
    .str.strip().str.lower()
)

# 3. Missing values
df = df.dropna(subset=["date", "traffic_source"])

for col in numeric_cols:
    if df[col].isna().any():
        df[col] = df[col].fillna(df[col].median())

# 4. Giá trị không hợp lệ
for col in ["sessions", "unique_visitors", "page_views",
            "avg_session_duration_sec"]:
    df = df[df[col] > 0]

df = df[(df["bounce_rate"] >= 0) & (df["bounce_rate"] <= 1)]

# 5. Ràng buộc logic
df = df[df["unique_visitors"] <= df["sessions"]]
df = df[df["page_views"] >= df["sessions"]]

# 6. Trùng lặp
df = df.drop_duplicates(
    subset=["date", "traffic_source"],
    keep="first"
)

# 7. Chuẩn hóa format
df["date"] = df["date"].dt.strftime("%Y-%m-%d")
df["traffic_source"] = df["traffic_source"].astype(str)

df = df.sort_values(
    ["date", "traffic_source"]
).reset_index(drop=True)

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

print("Đã làm sạch dữ liệu.")
print("Kích thước:", df.shape)
print("File:", OUTPUT)
