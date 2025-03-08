import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='white')

#Muat data
bike_df = pd.read_csv("bike_df.csv")
# Konversi dteday ke datetime
bike_df['dteday'] = pd.to_datetime(bike_df['dteday'])

# Tambahkan kolom time_period
time_bins = [0, 6, 10, 16, 20, 24]
time_labels = ['late_night', 'morning_rush', 'midday', 'evening_rush', 'evening']
bike_df['time_period'] = pd.cut(bike_df['hr'], bins=time_bins, labels=time_labels, right=False)

# Sidebar
with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")

    st.sidebar.header('Filter Data berdasarkan Pilihan Berikut:')
    #Tanggal
    min_date = bike_df["dteday"].min()
    max_date = bike_df["dteday"].max()

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    #Musim
    selected_seasons = st.sidebar.multiselect('Pilih Musim', bike_df['season_name'].unique(), default=bike_df['season_name'].unique())
    res_filtered = bike_df[bike_df['season_name'].isin(selected_seasons)]
    
    # Filter data berdasarkan tanggal
    res_filtered = bike_df[(bike_df['dteday'] >= pd.to_datetime(start_date)) & (bike_df['dteday'] <= pd.to_datetime(end_date))]
    # Filter data berdasarkan musim
    res_filtered = res_filtered[res_filtered['season_name'].isin(selected_seasons)]

# Menambahkan kolom time_period (menggunakan bins)
time_bins = [0, 6, 10, 16, 20, 24]
time_labels = ['Late night (00:00-05:00)', 'Morning rush (06:00-09:00)', 'Midday (10:00-15:00)', 'Evening rush (16:00-19:00)', 'Evening (20:00-23:00)']
res_filtered['time_period'] = pd.cut(res_filtered['hr'], bins=time_bins, labels=time_labels, right=False)

# Main Panel
st.title('Dashboard Penyewaan Sepeda')

# Tampilkan data yang telah difilter
st.write('### Data yang difilter')
st.caption('This only displays the first 3 rows of data')
st.dataframe(res_filtered.head(3))

# Data perbandingan pengguna casual dan 
# Pertanyaan 1: Korelasi atemp dan cnt
#Line
st.header('Hubungan antara Suhu yang Dirasakan dan Jumlah Sewa Sepeda (Line Chart)')
fig0, ax0 = plt.subplots(figsize=(10, 6))
ax0.plot(res_filtered.groupby('atemp')['cnt'].mean(), marker='o')
ax0.set_title('Hubungan antara Suhu yang Dirasakan dan Jumlah Sewa Sepeda (Line Chart)')
ax0.set_xlabel('Suhu yang Dirasakan (atemp) (°C)')
ax0.set_ylabel('Rata-rata Jumlah Sewa Sepeda (cnt)')
ax0.grid(True)
st.pyplot(fig0)
#Scatter
st.header('Korelasi Suhu yang Dirasakan (atemp) dan Jumlah Sewa Sepeda (cnt)')
fig1, ax1 = plt.subplots()
sns.scatterplot(x='atemp', y='cnt', data=res_filtered, ax=ax1)
ax1.set_xlabel('Feeling Temperature (atemp)')
ax1.set_ylabel('Count of Rent (cnt)')
# Garis Regresi
z = np.polyfit(res_filtered['atemp'], res_filtered['cnt'], 1)
p = np.poly1d(z)
ax1.plot(res_filtered['atemp'], p(res_filtered['atemp']), "r--", linewidth=2)

st.pyplot(fig1)

# Pertanyaan 2: Distribusi cnt berdasarkan season
st.header('Distribusi Jumlah Sewa Sepeda (cnt) Berdasarkan Musim (season)')
col1, col2 = st.columns(2)

with col1:
    #Bar Plot
    st.subheader('Bar Plot')
    fig2, ax2 = plt.subplots()
    sns.barplot(x='season_name', y='cnt', data=res_filtered, ax=ax2)
    ax2.set_xlabel('Season')
    ax2.set_ylabel('Count of Rent (cnt)')
    st.pyplot(fig2)

with col2:
    #Kelompokkan
    season_cnt = res_filtered.groupby('season_name')['cnt'].sum()
    #Pie Chart
    st.subheader('Pie Chart')
    fig3, ax3 = plt.subplots()
    ax3.pie(season_cnt, labels=season_cnt.index, autopct='%1.1f%%', startangle=140)
    st.pyplot(fig3)

# Rata-rata penyewaan berdasar time period
average_rentals = res_filtered.groupby('time_period', observed=True)['cnt'].mean().reindex(time_labels)

st.header('Rata-Rata Penyewaan Sepeda berdasarkan Waktu Penyewaan')
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(x=average_rentals.index, y=average_rentals.values, order=time_labels, ax=ax4)
ax4.set_title('Rata-Rata Penyewaan Sepeda berdasarkan Waktu Penyewaan')
ax4.set_xlabel('Time Period')
ax4.set_ylabel('Average Number of Rentals')
ax4.tick_params(axis='x', rotation=45)
plt.tight_layout()
st.pyplot(fig4)

st.caption('Made by: Cinta C')
