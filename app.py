import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Lapas iestatījumi
st.set_page_config(page_title="NordTech Analītika", layout="wide")
st.title("📊 NordTech Datu Analīzes Panelis")

# 2. Funkcija datu ielādei
@st.cache_data
def load_data():
# Svarīgi: failam jābūt tajā pašā mapē, kur šim app.py failam!
df = pd.read_csv('enriched_data.csv')
df['Date'] = pd.to_datetime(df['Date'])
return df

try:
df = load_data()

# 3. FILTRI sānu malā
st.sidebar.header("Izvēlieties filtrus")
category = st.sidebar.multiselect(
"Produktu kategorija:",
options=df['Product_Category'].unique(),
default=df['Product_Category'].unique()
)

filtered_df = df[df['Product_Category'].isin(category)]

# 4. Galvenie rādītāji (KPI)
c1, c2, c3 = st.columns(3)
with c1:
st.metric("Kopējie ieņēmumi", f"{filtered_df['Revenue'].sum():,.2f} EUR")
with c2:
ret_rate = (filtered_df['is_returned'].sum() / len(filtered_df)) * 100
st.metric("Atgriešanas %", f"{ret_rate:.2f}%")
with c3:
st.metric("Sūdzību skaits", filtered_df['issue_category'].count())

# 5. Grafiki
col_left, col_right = st.columns(2)
with col_left:
fig_rev = px.line(filtered_df.groupby('Date')['Revenue'].sum().reset_index(),
x="Date", y="Revenue", title="Ieņēmumu tendence")
st.plotly_chart(fig_rev, use_container_width=True)
with col_right:
fig_pie = px.pie(filtered_df, names="issue_category", title="Sūdzību iemesli")
st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
st.warning("⚠️ Lūdzu, pārliecinieties, ka fails 'enriched_data.csv' atrodas tajā pašā mapē!")