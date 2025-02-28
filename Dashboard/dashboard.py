import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
day = pd.read_csv('https://raw.githubusercontent.com/rmdlaska11/Analisis-Data/main/data/day.csv')
hour = pd.read_csv('https://raw.githubusercontent.com/rmdlaska11/Analisis-Data/main/data/hour.csv')

# Ubah format dteday menjadi datetime
day['dteday'] = pd.to_datetime(day['dteday'])
hour['dteday'] = pd.to_datetime(hour['dteday'])

# --- Streamlit App ---
st.title('Dashboard Penyewaan Sepeda')

# Filter data
min_date = day["dteday"].min()
max_date = day["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://raw.githubusercontent.com/rmdlaska11/Analisis-Data/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

# Konversi start_date & end_date ke datetime64
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Gunakan filter dengan datetime yang benar
day_df = day[(day["dteday"] >= start_date) & (day["dteday"] <= end_date)]
hour_df = hour[(hour["dteday"] >= start_date) & (hour["dteday"] <= end_date)]

# --- Metric ---
col1, col2, col3 = st.columns(3)

with col1:
    total_rentals = day_df['cnt'].sum()
    st.metric("Total Penyewaan", value=total_rentals)

with col2:
    avg_weekday_rentals = day_df[day_df['weekday'].isin(range(0, 5))]['cnt'].mean()
    st.metric("Rata-rata Penyewaan Weekday", value=int(avg_weekday_rentals))

with col3:
    avg_weekend_rentals = day_df[day_df['weekday'].isin(range(5, 7))]['cnt'].mean()
    st.metric("Rata-rata Penyewaan Weekend/Holiday", value=int(avg_weekend_rentals))

# Tab untuk mengelompokkan visualisasi
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Tren Harian", "Pengaruh Cuaca", "Hari Kerja vs Akhir Pekan",
    "Jenis Pengguna", "Pola Jam", "Kelompok Pelanggan"
])

with tab1:
    # Visualisasi Pertanyaan 1: Tren Penyewaan Sepeda Harian (diubah)
    st.header('Tren Penyewaan Sepeda Harian')  # Judul diubah
    daily_rentals = day_df.groupby('dteday')['cnt'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x='dteday', y='cnt', data=daily_rentals, marker='o', ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%d-%m-%Y'))  # Formatter sumbu x
    st.pyplot(fig)

with tab2:
    st.header('Pengaruh Cuaca terhadap Jumlah Penyewaan Sepeda')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit', y='cnt', data=day_df, palette=[ "#72BCD4", "#D3D3D3", "#D3D3D3"], ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticklabels(['Cerah', 'Berawan/Kabut', 'Hujan Ringan/Salju'])
    st.pyplot(fig)

with tab3:
    st.header('Jumlah Penyewaan Sepeda: Hari Kerja vs. Akhir Pekan/Libur')
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x='workingday', y='cnt', data=day_df, palette=["#D3D3D3", "#72BCD4"], ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.set_xticklabels(['Akhir Pekan/Libur', 'Hari Kerja'])
    st.pyplot(fig)

with tab4:
    st.header('Distribusi Penyewaan Sepeda Berdasarkan Jenis Pengguna')
    user_counts = day_df[['casual', 'registered']].sum()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(user_counts, labels=user_counts.index, autopct='%1.1f%%', startangle=90, colors=["#D3D3D3", "#72BCD4"])
    st.pyplot(fig)

with tab5:
    st.header('Pola Penyewaan Sepeda Per Jam (Hari Kerja vs. Akhir Pekan)')
    hourly_rentals = hour_df.pivot_table(values='cnt', index='hr', columns='weekday')
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(hourly_rentals, cmap='YlGnBu', annot=False, ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    st.pyplot(fig)

with tab6:
    st.header('Pengelompokan Pelanggan Berdasarkan Total Penyewaan')
    bins = [0, 3000, 6000, float('inf')]
    labels = ['Rendah', 'Sedang', 'Tinggi']
    day_df['kelompok_penyewaan'] = pd.cut(day_df['cnt'], bins=bins, labels=labels)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.countplot(x='kelompok_penyewaan', data=day_df, palette=["#D3D3D3", "#72BCD4", "#D3D3D3"], ax=ax)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    st.pyplot(fig)
