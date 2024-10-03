import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def get_monthly_counts_2011(df):
    bikeday_2011 = df[df['dteday'].dt.year == 2011]
    monthly_counts = bikeday_2011['cnt'].groupby(bikeday_2011['dteday'].dt.to_period('M')).sum()
    return monthly_counts

def get_monthly_counts_2012(df):
    bikeday_2012 = df[df['dteday'].dt.year == 2012]
    monthly_counts = bikeday_2012['cnt'].groupby(bikeday_2012['dteday'].dt.to_period('M')).sum()
    return monthly_counts

def get_total_hour(df):
    hour_count = df.groupby(by="hr").cnt.sum().reset_index()
    return hour_count

def get_holiday_vs_workingday_data(df):
    holiday_vs_workingday = df.groupby('workingday')['cnt'].sum()
    labels = ['Holiday', 'Working Day']
    data = [holiday_vs_workingday[0], holiday_vs_workingday[1]]
    return labels, data

def calculate_actual_temperature(df):
    df['temp_actual'] = df['temp'] * 41
    return df

def get_season_counts(df):
    season_counts = df.groupby(by=["season", "yr"]).agg({
        "cnt": "sum"
    }).reset_index()
    return season_counts


bikeday_df = pd.read_csv("bike_day.csv")
bikehour_df = pd.read_csv("bike_hour.csv")

datetime_columns = ["dteday"]
bikeday_df.sort_values(by="dteday", inplace=True)
bikeday_df.reset_index(inplace=True)   

bikehour_df.sort_values(by="dteday", inplace=True)
bikehour_df.reset_index(inplace=True)

for column in datetime_columns:
    bikeday_df[column] = pd.to_datetime(bikeday_df[column])
    bikehour_df[column] = pd.to_datetime(bikehour_df[column])

mindate_day = bikeday_df["dteday"].min()
maxdate_day = bikeday_df["dteday"].max()

mindate_hour = bikehour_df["dteday"].min()
maxdate_hour = bikehour_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrUnWJBlVOI_r_HTHJXtGQi9Ev5jRbUv-bnJgmIQ63FGD-73z5XDsV9xynrZpAkemrPd0&usqp=CAU")
    
        # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=mindate_day,
        max_value=maxdate_day,
        value=[mindate_day, maxdate_day])
  
main_day_df = bikeday_df[(bikeday_df["dteday"] >= str(start_date)) & 
                        (bikeday_df["dteday"] <= str(end_date))]

main_hour_df = bikehour_df[(bikehour_df["dteday"] >= str(start_date)) & 
                        (bikehour_df["dteday"] <= str(end_date))]


monthly_counts_2011 = get_monthly_counts_2011(main_day_df)
monthly_counts_2012 = get_monthly_counts_2012(main_day_df)
hour_count = get_total_hour(main_hour_df)
labels, data = get_holiday_vs_workingday_data(main_day_df)
temp_df = calculate_actual_temperature(main_day_df)
season_counts = get_season_counts(main_day_df)

st.title('Dashboard Penyewaan Sepeda')

st.subheader('Tren Penyewaan Sepeda')
tab1, tab2 = st.tabs(["2011", "2012"])
 
with tab1:
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.scatter(monthly_counts_2011.index.astype(str), monthly_counts_2011.values, c="#90CAF9", s=100, marker='*', label='Jumlah Penyewaan')
    ax.plot(monthly_counts_2011.index.astype(str), monthly_counts_2011.values, label='Trend Penyewaan')

    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Tren Penyewaan Sepeda Pada Tahun 2011')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
 
with tab2:
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.scatter(monthly_counts_2012.index.astype(str), monthly_counts_2012.values, c="#90CAF9", s=100, marker='*', label='Jumlah Penyewaan')
    ax.plot(monthly_counts_2012.index.astype(str), monthly_counts_2012.values, label='Trend Penyewaan')

    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Penyewaan')
    ax.set_title('Tren Penyewaan Sepeda Pada Tahun 2012')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)


st.subheader("Distribusi Penyewaan Sepeda per Jam")
fig, ax = plt.subplots(figsize=(16, 8))

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='hr', y='cnt', data=hour_count, palette=colors, ax=ax)

ax.set_xlabel('Jam (24-Hour Format)', fontsize=14)
ax.set_ylabel('Jumlah Penyewaan', fontsize=14)
ax.tick_params(axis='x', labelsize=15)
ax.tick_params(axis='y', labelsize=15)
ax.grid(axis='y')
st.pyplot(fig)


st.subheader("Perbandingan Jumlah Penyewaan Sepeda pada Holiday (Hari Libur) dan Working Day (Hari Kerja)")
fig, ax = plt.subplots(figsize=(8, 8))  

ax.pie(data, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#72BCD4"], startangle=90)
st.pyplot(fig)


st.subheader("Korelasi antara Suhu dengan Jumlah Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(12, 6))

sns.regplot(x=temp_df["temp_actual"], y=temp_df["cnt"], ax=ax)

ax.set_xlabel("Suhu (Celcius)", fontsize=14)
ax.set_ylabel("Total Penyewaan Sepeda", fontsize=14)
st.pyplot(fig)


st.subheader("Total Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(10, 6))  

sns.barplot(data=season_counts, x="season", y="cnt", hue="yr", palette=["#D3D3D3", "#72BCD4"], ax=ax)

ax.set_ylabel("Jumlah")
ax.set_xlabel("Musim")
ax.legend(title="Tahun", loc="upper right")
plt.tight_layout()
st.pyplot(fig)

st.caption('Sisilia Dwi Febrianti (c) Dicoding 2024')

