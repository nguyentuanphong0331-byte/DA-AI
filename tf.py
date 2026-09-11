import pandas as pd

df = pd.read_csv('web_traffic.csv')

df['date'] = pd.to_datetime(df['date'])

# Chuẩn hóa cột nguồn lưu lượng về dạng viết thường và loại bỏ khoảng trắng thừa
df['traffic_source'] = df['traffic_source'].str.strip().str.lower()

valid_mask = (
    (df['unique_visitors'] <= df['sessions']) &
    (df['page_views'] >= df['sessions']) &
    (df['bounce_rate'].between(0, 1)) &
    (df['avg_session_duration_sec'] >= 0)
)
df_clean = df[valid_mask].copy()

df_clean = df_clean.drop_duplicates(subset=['date', 'traffic_source'], keep='first')

df_clean['pages_per_session'] = (df_clean['page_views'] / df_clean['sessions']).round(2)

df_clean.to_csv('web_traffic_cleaned.csv', index=False)
print("Đã làm sạch và lưu file thành công tại web_traffic_cleaned.csv!")