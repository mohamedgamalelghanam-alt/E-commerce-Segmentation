import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة (بتخليها واسعة وشيك)
st.set_page_config(page_title="E-commerce Analytics", layout="wide")

# 2. تحميل الداتا
@st.cache_data
def load_data():
    df = pd.read_csv('Cleaned_Ecommerce_Data.csv')
    return df

df = load_data()

# 3. السايد بار (Sidebar) للفلاتر
st.sidebar.header("Filter Options")
country = st.sidebar.multiselect("Select Country:", options=df['Country'].unique(), default=df['Country'].unique()[:5])
filtered_df = df[df['Country'].isin(country)]

# 4. العنوان الرئيسي
st.title("📊 Customer Segmentation Dashboard")
st.markdown("---")

# 5. قسم الأرقام السريعة (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Revenue'].sum():,.0f}")
col2.metric("Total Orders", f"{filtered_df['InvoiceNo'].nunique():,}")
col3.metric("Total Customers", f"{filtered_df['CustomerID'].nunique():,}")
col4.metric("Avg Order Value", f"${filtered_df.groupby('InvoiceNo')['Revenue'].sum().mean():.2f}")

st.markdown("---")

# 6. قسم الرسومات البيانية
left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Top Selling Products")
    top_products = filtered_df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
    fig_products = px.bar(top_products, x='Quantity', y='Description', orientation='h', color='Quantity', color_continuous_scale='Blues')
    st.plotly_chart(fig_products, use_container_width=True)

with right_column:
    st.subheader("Revenue by Country")
    rev_country = filtered_df.groupby('Country')['Revenue'].sum().reset_index()
    fig_country = px.pie(rev_country, values='Revenue', names='Country', hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_country, use_container_width=True)

# 7. قسم الـ Segments (لو عامل عمود الـ Cluster)
if 'Cluster' in df.columns:
    st.markdown("---")
    st.subheader("Customer Segments Analysis")
    fig_clusters = px.scatter(filtered_df, x='Recency', y='Monetary', color='Cluster', title="Customer Clusters (RFM)")
    st.plotly_chart(fig_clusters, use_container_width=True)
