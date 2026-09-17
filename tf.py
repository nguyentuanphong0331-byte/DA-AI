import pandas as pd
import json

with open("tf(1).json", "r", encoding="utf-8") as f:
    data_json = json.load(f)

df_json = pd.DataFrame(data_json)

df_csv = pd.read_csv("web_traffic.csv")

columns = [
    "date",
    "sessions",
    "unique_visitors",
    "page_views",
    "bounce_rate",
    "avg_session_duration_sec",
    "traffic_source"
]

df_json = df_json[columns]
df_csv = df_csv[columns]

df_json["traffic_source"] = (
    df_json["traffic_source"]
    .str.replace(r"\s+Variant\s+\d+$", "", regex=True)
    .str.strip()
)

# Chuyển date về kiểu datetime
df_json["date"] = pd.to_datetime(
    df_json["date"],
    errors="coerce"
)

df_csv["date"] = pd.to_datetime(
    df_csv["date"],
    errors="coerce"
)

numeric_columns = [
    "sessions",
    "unique_visitors",
    "page_views",
    "bounce_rate",
    "avg_session_duration_sec"
]

for column in numeric_columns:
    df_json[column] = pd.to_numeric(
        df_json[column],
        errors="coerce"
    )

    df_csv[column] = pd.to_numeric(
        df_csv[column],
        errors="coerce"
    )
    
for column in [
    "sessions",
    "unique_visitors",
    "page_views",
    "bounce_rate",
    "avg_session_duration_sec"
]:
    df_json.loc[df_json[column] < 0, column] = None
    df_csv.loc[df_csv[column] < 0, column] = None


df_json = df_json.dropna(subset=["date"])
df_csv = df_csv.dropna(subset=["date"])

df = pd.concat(
    [df_csv, df_json],
    ignore_index=True
)

df = df.drop_duplicates()

df = df.dropna()

df = df.sort_values("date")

df["date"] = df["date"].dt.strftime("%Y-%m-%d")

df.to_csv(
    "web_traffic_cleaned_merged.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Đã làm sạch và gộp dữ liệu!")
print("Số dòng:", len(df))
print("Số cột:", len(df.columns))

print("\n5 dòng đầu:")
print(df.head())

print("\nThông tin dữ liệu:")
print(df.info())
