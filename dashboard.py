# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

# Setting Layout
st.set_page_config(layout="wide")

# Add Title and Tabs
st.title("Proyek Analisis Data: Bike Sharing Dataset")
tab1, tab2 = st.tabs(["Pertanyaan 1", 
                      "Pertanyaan 2",])

# Import Dataframe
day = pd.read_csv("day.csv")

# Change the Data Type of the "dteday" Column 
day["dteday"] = pd.to_datetime(day["dteday"])

# Add Content to Tab
with tab1:
    st.header("")

# Add Content to Tab
with tab1:
    st.header("Apakah permintaan sewa sepeda lebih tinggi selama hari kerja atau akhir pekan?")

    rentals_by_day_type = day.groupby("workingday").agg({
    "instant": "nunique",
    "cnt": ["max", "min"]
    })
    rentals_by_day_type = rentals_by_day_type.reset_index()

    rentals_by_day_type["workingday"] = ["Weekends", "Weekdays"]

    plt.figure(figsize=(16, 8))
    plt.bar(rentals_by_day_type["workingday"],
            rentals_by_day_type[("cnt", "max")],
            label="Maximum Rentals")
    plt.bar(rentals_by_day_type["workingday"],
            rentals_by_day_type[("cnt", "min")],
            label="Minimum Rentals")

    for i in range(len(rentals_by_day_type["workingday"])):
        plt.text(i, rentals_by_day_type[("cnt", "max")][i],
                str(rentals_by_day_type[("cnt", "max")][i]),
                ha="center", va="bottom")
        plt.text(i, rentals_by_day_type[("cnt", "min")][i],
                str(rentals_by_day_type[("cnt", "min")][i]),
                ha="center", va="bottom")

    plt.title("Maximum and Minimum Bike Rentals by Weekdays and Weekends")
    plt.ylabel("Number of Bike Rentals")

    plt.legend(loc="upper left")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.gca().yaxis.set_major_formatter(
        plt.matplotlib.ticker.StrMethodFormatter("{x:,.0f}")
    )
    st.pyplot(plt)

    st.caption("Kesimpulan: Jumlah sewa sepeda tertinggi terjadi pada akhir pekan, mencapai 8.714, sementara jumlah sewa terendah terjadi pada hari kerja, hanya sebesar 8.362.")

# Add Content to Tab
with tab2:
    st.header("Siapakah kelompok pengguna yang paling banyak memanfaatkan layanan penyewaan sepeda?")

    user_counts = day[['casual', 'registered']].sum()

    plt.figure(figsize=(10, 6))
    bars = plt.bar(user_counts.index, user_counts.values)
    plt.title('Total Bike Rentals by User Type')
    plt.xlabel('User Type')
    plt.ylabel('Number of Bike Rentals')

    # Menambahkan label nilai pada setiap bar
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval, round(yval), ha='center', va='bottom')

    st.pyplot(plt)

    st.caption("Kesimpulan: Mayoritas pengguna adalah pengguna terdaftar, dengan total jumlah mencapai 2.672.662.")