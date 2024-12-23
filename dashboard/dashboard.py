import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import datetime

sns.set(style='dark')
plt.style.use('dark_background')

# Fungsi untuk menghitung total pengguna casual dan registered per tahun
def summarize_casual_registered(data):
    """
    Menghitung jumlah pengguna casual dan registered per tahun
    dan mengembalikan data dalam format total keseluruhan.
    """
    casual_total = data["casual"].sum()
    registered_total = data["registered"].sum()
    
    summary = pd.DataFrame({
        "User Type": ["Casual", "Registered"],
        "Total": [casual_total, registered_total]
    })
    
    return summary


# Fungsi untuk menganalisis penggunaan sepeda per bulan
def analyze_monthly_usage(data):
    """
    Menghitung total jumlah pengguna sepeda per bulan dan tahun.
    """
    monthly_usage = data.groupby(["mnth", "yr"])["cnt"].sum().reset_index()
    monthly_usage["yr"] = monthly_usage["yr"].replace({0: 2011, 1: 2012})
    monthly_usage["month_name"] = monthly_usage["mnth"].map({
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 
        6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 
        11: "Nov", 12: "Dec"
    })
    return monthly_usage

# Fungsi untuk penggunaan sepeda per jam
def analyze_hourly_usage(data):
    """
    Menghitung jumlah pengguna sepeda per jam.
    """
    hourly_usage = data.groupby("hr")["cnt"].sum().reset_index()
    return hourly_usage


# Fungsi untuk analisis hari libur
def summarize_holiday_usage(data):
    """
    Mengelompokkan data berdasarkan hari libur dan tahun.
    """
    holiday_usage = data.groupby(["holiday", "yr"])["cnt"].sum().reset_index()
    holiday_usage["yr"] = holiday_usage["yr"].replace({0: 2011, 1: 2012})
    holiday_usage["day_type"] = holiday_usage["holiday"].map({0: "Non-Holiday", 1: "Holiday"})
    return holiday_usage

# Fungsi untuk menganalisis hari kerja
def summarize_workday_usage(data):
    """
    Mengelompokkan data berdasarkan hari kerja dan tahun.
    """
    workday_usage = data.groupby(["workingday", "yr"])["cnt"].sum().reset_index()
    workday_usage["yr"] = workday_usage["yr"].replace({0: 2011, 1: 2012})
    workday_usage["day_category"] = workday_usage["workingday"].map({0: "Non-Workday", 1: "Workday"})
    return workday_usage

# Fungsi untuk menganalisis penggunaan sepeda berdasarkan musim
def summarize_season_usage(data):
    """
    Menghitung jumlah pengguna sepeda berdasarkan musim dan tahun.
    """
    season_usage = data.groupby(["season", "yr"])["cnt"].sum().reset_index()
    season_usage["yr"] = season_usage["yr"].replace({0: 2011, 1: 2012})
    season_usage["season_label"] = season_usage["season"].map({
        1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"
    })
    return season_usage

# Fungsi untuk analisis penggunaan berdasarkan kondisi cuaca
def summarize_weather_usage(data):
    """
    Mengelompokkan data berdasarkan kondisi cuaca dan tahun.
    """
    weather_usage = data.groupby(["weathersit", "yr"])["cnt"].sum().reset_index()
    weather_usage["yr"] = weather_usage["yr"].replace({0: 2011, 1: 2012})
    weather_usage["weather_condition"] = weather_usage["weathersit"].map({
        1: "Clear", 2: "Mist/Cloudy", 3: "Light Rain/Snow", 4: "Heavy Rain/Snow"
    })
    return weather_usage


day_df = pd.read_csv("main_day_df_data.csv")
hour_df = pd.read_csv("main_hour_df_data.csv")

# Mengonversi kolom tanggal menjadi tipe datetime
day_df["date"] = pd.to_datetime(day_df["dteday"])
hour_df["date"] = pd.to_datetime(hour_df["dteday"])

# Mendapatkan rentang tanggal minimum dan maksimum dari dataset
earliest_date = day_df["date"].min()
latest_date = day_df["date"].max()

# Sidebar untuk filter
with st.sidebar:
    # Menampilkan logo aplikasi di sidebar
    st.image("logo.png")
    
    # Input tanggal untuk filter
    start_date, end_date = st.date_input(
        label="Pilih Rentang Tanggal",
        min_value=earliest_date,
        max_value=latest_date,
        value=[earliest_date, latest_date]
    )
    
 

# Filter data harian berdasarkan tanggal yang dipilih
filtered_day_df = day_df[(day_df["date"] >= pd.to_datetime(start_date)) & 
                               (day_df["date"] <= pd.to_datetime(end_date))]

# Filter data per jam berdasarkan tanggal dan jam yang dipilih
filtered_hour_df = hour_df[(hour_df["date"] >= pd.to_datetime(start_date)) & 
                           (hour_df["date"] <= pd.to_datetime(end_date))]

# Menyiapkan berbagai dataframe untuk analisis
def prepare_dataframes(day_df, hour_df):
    # Membuat dataframe casual vs registered berdasarkan tahun
    casual_register_df = summarize_casual_registered(day_df)
    
    # Membuat dataframe bulanan berdasarkan tahun
    monthly_df = analyze_monthly_usage(day_df)
    
    # Membuat dataframe penggunaan sepeda per jam
    hourly_df = analyze_hourly_usage(hour_df)
    
    # Membuat dataframe berdasarkan hari libur
    holiday_df = summarize_holiday_usage(day_df)
    
    # Membuat dataframe berdasarkan hari kerja
    workingday_df = summarize_workday_usage(day_df)
    
    # Membuat dataframe berdasarkan musim
    season_df = summarize_season_usage(day_df)
    
    # Membuat dataframe berdasarkan kondisi cuaca
    weather_df = summarize_weather_usage(day_df)
    
    # Mengganti nilai tahun dari 0/1 menjadi 2011/2012
    hourly_df = hourly_df.replace({"yr": {0: 2011, 1: 2012}})
    
    return {
        "casual_register_df": casual_register_df,
        "monthly_df": monthly_df,
        "hourly_df": hourly_df,
        "holiday_df": holiday_df,
        "workingday_df": workingday_df,
        "season_df": season_df,
        "weather_df": weather_df
    }

# Menyiapkan data dengan fungsi yang dirancang
dataframes = prepare_dataframes(day_df, hour_df)

# Mengakses dataframe individual
casual_register_df = dataframes["casual_register_df"]
monthly_df = dataframes["monthly_df"]
hourly_df = dataframes["hourly_df"]
holiday_df = dataframes["holiday_df"]
workingday_df = dataframes["workingday_df"]
season_df = dataframes["season_df"]
weather_df = dataframes["weather_df"]


# Header untuk dashboard
st.header('Bike Sharing Dashboard 🚵')

# 1. Analisis Perubahan Pengguna Sepeda Setiap Bulan
monthly_df = dataframes["monthly_df"]
plt.figure(figsize=(10, 6))
sns.barplot(data=monthly_df, x='mnth', y='cnt', palette='viridis')
plt.title('Monthly Bike Usage', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Usage', fontsize=12)
st.pyplot(plt)
st.write("### Data Penggunaan Sepeda per Bulan:")
st.dataframe(monthly_df)

# 2. Analisis Pengguna Terdaftar vs Biasa
casual_register_df = dataframes["casual_register_df"]
plt.figure(figsize=(8, 6))
sns.barplot(data=casual_register_df, x='User Type', y='Total', palette='coolwarm')
plt.title('Casual vs Registered Users', fontsize=16)
plt.xlabel('User Type', fontsize=12)
plt.ylabel('Total Users', fontsize=12)
st.pyplot(plt)
st.write("### Data Pengguna Berdasarkan Tipe:")
st.dataframe(casual_register_df)

# 3. Pengguna Sepeda pada Hari Libur vs Hari Kerja
holiday_workday_usage = day_df.groupby(['holiday', 'workingday'])['cnt'].mean().reset_index()
holiday_workday_usage['Label'] = holiday_workday_usage.apply(
    lambda x: 'Holiday' if x['holiday'] == 1 else (
        'Working Day' if x['workingday'] == 1 else 'Non-Working Day'
    ), axis=1
)
plt.figure(figsize=(8, 6))
sns.barplot(data=holiday_workday_usage, x='Label', y='cnt', palette='Set2')
plt.title('Bike Usage on Holidays vs Working Days', fontsize=16)
plt.xlabel('Day Type', fontsize=12)
plt.ylabel('Average Usage', fontsize=12)
st.pyplot(plt)
st.write("### Average Bike Usage by Day Type:")
st.dataframe(holiday_workday_usage)

holiday_avg = holiday_workday_usage.loc[holiday_workday_usage['Label'] == 'Holiday', 'cnt'].values[0]
working_day_avg = holiday_workday_usage.loc[holiday_workday_usage['Label'] == 'Working Day', 'cnt'].values[0]
if holiday_avg > working_day_avg:
    st.success(f"Yes, bike usage is higher on holidays ({holiday_avg:.2f}) compared to working days ({working_day_avg:.2f}).")
else:
    st.warning(f"No, bike usage is higher on working days ({working_day_avg:.2f}) compared to holidays ({holiday_avg:.2f}).")

# 4. Penggunaan Sepeda Berdasarkan Musim
season_usage = day_df.groupby('season')['cnt'].mean().reset_index()
season_usage['season'] = season_usage['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
plt.figure(figsize=(8, 6))
sns.barplot(data=season_usage, x='season', y='cnt', palette='pastel')
plt.title('Seasonal Bike Usage', fontsize=16)
plt.xlabel('Season', fontsize=12)
plt.ylabel('Average Usage', fontsize=12)
st.pyplot(plt)
st.write("### Average Bike Usage by Season:")
st.dataframe(season_usage)

highest_season = season_usage.loc[season_usage['cnt'].idxmax()]
st.success(f"The season with the highest bike usage is **{highest_season['season']}**, "
           f"with an average of **{highest_season['cnt']:.2f}** users.")

# 5. Penggunaan Sepeda Berdasarkan Jam
# Penggunaan Sepeda Berdasarkan Jam
hourly_usage = analyze_hourly_usage(hour_df)

# Pastikan semua jam dari 0 hingga 23 ada di data
all_hours = pd.DataFrame({'hr': range(24)})  # Buat daftar jam 0-23
hourly_usage = all_hours.merge(hourly_usage, on='hr', how='left')  # Gabungkan dengan data asli
hourly_usage['cnt'] = hourly_usage['cnt'].fillna(0)  # Isi data yang hilang dengan 0

# Cari jam dengan penggunaan tertinggi
highest_usage_hour = hourly_usage.loc[hourly_usage['cnt'].idxmax()]
st.write("### Hourly Usage Analysis:")
st.write(f"Highest bike usage is at hour {highest_usage_hour['hr']} with {highest_usage_hour['cnt']} total users.")

# Visualisasi penggunaan sepeda per jam
plt.figure(figsize=(10, 6))
sns.lineplot(data=hourly_usage, x='hr', y='cnt', marker='o', color='green')
plt.title('Hourly Bike Usage', fontsize=16)
plt.xlabel('Hour of Day', fontsize=12)
plt.ylabel('Total Usage', fontsize=12)
plt.grid(True)
st.pyplot(plt)



# 6. Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda
weather_usage = summarize_weather_usage(day_df)
weather_summary = weather_usage.groupby("weather_condition")["cnt"].sum().reset_index()
st.write("### Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda")
st.table(weather_summary)
plt.figure(figsize=(8, 6))
sns.barplot(data=weather_summary, x='weather_condition', y='cnt', palette='muted')
plt.title('Bike Usage by Weather Condition', fontsize=16)
plt.xlabel('Weather Condition', fontsize=12)
plt.ylabel('Total Usage', fontsize=12)
plt.xticks(rotation=15)
st.pyplot(plt)