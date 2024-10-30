import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='whitegrid')

def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby("hours").agg({"count_cr": "sum"}).reset_index()
    hour_count_df.columns = ["hours", "count_cr"]  # Pastikan kolom yang dihasilkan bernama "count_cr"
    return hour_count_df

def sum_order(hour_df):
    sum_order_items_df = hour_df.groupby("hours").count_cr.sum().sort_values(ascending=False).reset_index()
    sum_order_items_df.columns = ["hours", "count_cr"]  # Pastikan nama kolom sama seperti yang dibutuhkan
    return sum_order_items_df


# Membaca data
days_df = pd.read_csv("dashboard/day_clean.csv")
hours_df = pd.read_csv("dashboard/hour_clean.csv")

datetime_columns = ["dteday"]
days_df["dteday"] = pd.to_datetime(days_df["dteday"])
hours_df["dteday"] = pd.to_datetime(hours_df["dteday"])

# Sidebar untuk pilihan tanggal
with st.sidebar:
    st.image("https://storage.googleapis.com/gweb-uniblog-publish-prod/original_images/image1_hH9B4gs.jpg")
    start_date, end_date = st.date_input("Rentang Waktu", value=[days_df["dteday"].min(), days_df["dteday"].max()])

main_df_days = days_df[(days_df["dteday"] >= pd.to_datetime(start_date)) & 
                       (days_df["dteday"] <= pd.to_datetime(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= pd.to_datetime(start_date)) & 
                        (hours_df["dteday"] <= pd.to_datetime(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
sum_order_items_df = hour_count_df.reset_index()

# Header
st.header('Bike Sharing Dashboard :sparkles:')

# Bagian Summary
st.subheader("Daily Sharing Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sharing Bike", value=main_df_days["count_cr"].sum())
with col2:
    st.metric("Total Registered", value=main_df_days["registered"].sum())
with col3:
    st.metric("Total Casual", value=main_df_days["casual"].sum())

# Plot Garis - Performa Penjualan
st.subheader("Performa Penyewaan Sepeda 2012")
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    days_df["dteday"],
    days_df["count_cr"],
    marker='o', 
    linewidth=2,
    color="#1976D2",
    label="Penyewaan Harian"
)
ax.set_title("Jumlah Penyewaan Sepeda Harian", fontsize=20)
ax.set_xlabel("Tanggal", fontsize=16)
ax.set_ylabel("Jumlah Penyewaan", fontsize=16)
ax.legend()
st.pyplot(fig)

# Plot Bar - Jam dengan Penyewaan Terbanyak dan Tersedikit
st.subheader("Jam dengan Penyewaan Terbanyak dan Tersedikit")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))

# Barplot Jam Terbanyak
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.head(5), palette="Blues", ax=ax[0])
ax[0].set_title("Top 5 Jam dengan Penyewaan Tertinggi", fontsize=14)
ax[0].set_xlabel("Jam", fontsize=12)
ax[0].set_ylabel("Jumlah Penyewaan", fontsize=12)

# Barplot Jam Tersedikit
sns.barplot(x="hours", y="count_cr", data=sum_order_items_df.tail(5), palette="Greys", ax=ax[1])
ax[1].set_title("Bottom 5 Jam dengan Penyewaan Terendah", fontsize=14)
ax[1].set_xlabel("Jam", fontsize=12)
ax[1].set_ylabel("")

st.pyplot(fig)

# Plot Bar - Musim dengan Penyewaan Terbanyak
st.subheader("Penyewaan Berdasarkan Musim")
season_df = main_df_days.groupby("season").agg({"count_cr": "sum"}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="season", y="count_cr", data=season_df, palette="coolwarm", ax=ax)
for i, v in enumerate(season_df["count_cr"]):
    ax.text(i, v + 10000, str(v), ha='center', color='black', fontsize=12)
ax.set_title("Jumlah Penyewaan Sepeda per Musim", fontsize=18)
ax.set_xlabel("Musim", fontsize=14)
ax.set_ylabel("Jumlah Penyewaan", fontsize=14)
st.pyplot(fig)

# Pie Chart - Perbandingan Casual dan Registered
st.subheader("Perbandingan Penyewa Casual dan Registered")
labels = 'Casual', 'Registered'
sizes = [18.8, 81.2]
colors = ["#FFC107", "#1976D2"]

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, explode=(0, 0.1), shadow=True, startangle=140)
ax1.set_title("Persentase Penyewa Casual vs Registered", fontsize=16)
st.pyplot(fig1)
