import pandas as pd

df = pd.read_csv('shipments_realistic.csv')

date_columns = ['ship_date', 'delivery_date', 'join_date']
for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors='coerce')

df['shipper_phone'] = df['shipper_phone'].astype(str).str.zfill(10)

df = df.drop_duplicates()

df = df.drop_duplicates(subset=['order_id'], keep='first')

df = df[df['delivery_date'] >= df['ship_date']]

df['delivery_duration_days'] = (df['delivery_date'] - df['ship_date']).dt.days

df.to_csv('shipments_cleaned.csv', index=False)
print("Hoàn tất làm sạch dữ liệu và đã xuất file shipments_cleaned.csv!")