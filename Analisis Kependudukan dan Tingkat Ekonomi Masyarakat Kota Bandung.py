# -*- coding: utf-8 -*-
"""
# **Analisis Kependudukan dan Kondisi Ekonomi Masyarakat Kota Bandung**

## **Business Understanding**

Pemerintah Kota Bandung memiliki program kerja untuk memberikan bantuan sosial kepada fakir miskin. 
Agar dana tersebut dapat disalurkan secara efektif dan efisien, dibutuhkan data yang valid mengenai 
kondisi perekonomian masyarakat di setiap kelurahan. Hal ini relevan dengan situasi pandemi Covid-19, 
yang menuntut Pemerintah Kota Bandung untuk memprioritaskan masyarakat berpenghasilan rendah.

**Rumusan Masalah:**
1. Berapa banyak kependudukan di suatu wilayah?
2. Daerah mana yang memiliki kepadatan penduduk tertinggi dan terendah?
3. Berapa banyak masyarakat berpenghasilan tinggi di setiap kelurahan?
4. Daerah mana saja yang memiliki masyarakat berpenghasilan tinggi?
5. Daerah mana saja yang berpenghasilan rendah?
6. Berapa jumlah kepala keluarga di setiap kecamatan?

## **Data Understanding**
"""

# ==============================
# Load Library
# ==============================
from google.colab import drive
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==============================
# Mount Google Drive
# ==============================
drive.mount('/content/gdrive')

# ==============================
# Load Dataset
# ==============================
data1 = pd.read_csv("/dataset/tahun-2021-s1---jumlah-kepala-keluarga-berdasarkan-kelurahan.csv")
data2 = pd.read_csv("/dataset/jumlah-penduduk-luas-wilayah-dan-kepadatan-penduduk-per-kecamatan-di-kota-bandung-tahun-2014.csv")
data3 = pd.read_csv("/dataset/data-jumlah-kepala-rumah-tangga-mbr-dan-non-mbr-per-kelurahan-tahun-2017.csv")

# Gabungkan data berdasarkan Kecamatan dan Kelurahan
df = pd.merge(data3, data1, on=["Kecamatan", "Kelurahan"], how="left")
df.head()

# ==============================
# Summary Function
# ==============================
def summary(df, pred=None):
    obs = df.shape[0]
    types = df.dtypes
    counts = df.apply(lambda x: x.count())
    mins = df.min(numeric_only=True)
    uniques = df.apply(lambda x: x.nunique())
    nulls = df.isnull().sum()
    
    print('Data shape:', df.shape)
    
    if pred is None:
        cols = ['types', 'counts', 'uniques', 'nulls', 'min']
        info = pd.concat([types, counts, uniques, nulls, mins], axis=1)
        info.columns = cols
    
    print('___________________________\nData types:')
    print(info.types.value_counts())
    print('___________________________')
    
    return info

details = summary(df)
display(details.sort_values(by='nulls', ascending=False))

# ==============================
# Data Cleaning and Preparation
# ==============================
df = df.drop(columns=['No.'], errors='ignore')
df = df.dropna().reset_index(drop=True)

# Ubah nama kolom agar konsisten
df = df.rename(columns={
    'Jumlah Kepala Keluarga': 'Jumlah_KK',
    'Jumlah Kepala Rumah Tangga MBR': 'Jumlah_KRT_MBR',
    'Jumlah Kepala Rumah Tangga Non MBR': 'Jumlah_KRT_NONMBR'
})

details = summary(df)
display(details.sort_values(by='nulls', ascending=False))

# Simpan dataset hasil penggabungan
df.to_csv("DataGabungan.csv", index=False)

# ==============================
# Exploratory Data Analysis (EDA)
# ==============================

# Atur gaya visualisasi
sns.set(style="whitegrid")
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['figure.figsize'] = (12, 6)

# Top 5 Kecamatan dengan jumlah KK terbanyak
plt.figure()
df.groupby('Kecamatan')['Jumlah_KK'].sum().sort_values(ascending=False).head(5).plot(
    kind='bar', color='blue', title='Top 5 Kecamatan dengan Jumlah KK Terbanyak'
)
plt.ylabel('Jumlah Kepala Keluarga')
plt.show()

# Top 5 Kecamatan dengan jumlah KK terendah
plt.figure()
df.groupby('Kecamatan')['Jumlah_KK'].sum().sort_values(ascending=True).head(5).plot(
    kind='bar', color='green', title='Top 5 Kecamatan dengan Jumlah KK Terendah'
)
plt.ylabel('Jumlah Kepala Keluarga')
plt.show()

# Top 5 Kecamatan dengan jumlah MBR terbanyak (penghasilan rendah)
plt.figure()
df.groupby('Kecamatan')['Jumlah_KRT_MBR'].sum().sort_values(ascending=False).head(5).plot(
    kind='bar', color='purple', title='Top 5 Kecamatan dengan Masyarakat Berpenghasilan Rendah (MBR) Terbanyak'
)
plt.ylabel('Jumlah Kepala Rumah Tangga MBR')
plt.show()

# Top 5 Kecamatan dengan jumlah Non-MBR terbanyak (penghasilan tinggi)
plt.figure()
df.groupby('Kecamatan')['Jumlah_KRT_NONMBR'].sum().sort_values(ascending=False).head(5).plot(
    kind='bar', color='orange', title='Top 5 Kecamatan dengan Masyarakat Berpenghasilan Tinggi (Non-MBR) Terbanyak'
)
plt.ylabel('Jumlah Kepala Rumah Tangga Non-MBR')
plt.show()

# Jumlah KK pada setiap Kecamatan
plt.figure(figsize=(14, 6))
df.groupby('Kecamatan')['Jumlah_KK'].sum().sort_values(ascending=False).plot(
    kind='bar', color='teal', title='Jumlah Kepala Keluarga per Kecamatan di Kota Bandung'
)
plt.ylabel('Jumlah Kepala Keluarga')
plt.show()