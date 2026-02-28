
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")
st.title("📊 E-commerce Sales & Customer Segmentation")

# قراءة الداتا (تأكد أن الملف موجود في نفس المكان)
df = pd.read_csv('Cleaned_Ecommerce_Data.csv')

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['TotalAmount'].sum():,.2f}")
col2.metric("Total Transactions", df['InvoiceNo'].nunique())
col3.metric("Total Customers", df['CustomerID'].nunique())

st.subheader("Revenue by Country")
fig = px.bar(df.groupby('Country')['TotalAmount'].sum().reset_index(), x='Country', y='TotalAmount')
st.plotly_chart(fig, use_container_width=True)
    
