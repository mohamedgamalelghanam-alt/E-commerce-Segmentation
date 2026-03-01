import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="E-commerce Analytics Pro", layout="wide", initial_sidebar_state="expanded")

# 2. دالة تحميل البيانات مع معالجة الأعمدة
@st.cache_data
def load_data():
    df = pd.read_csv('Cleaned_Ecommerce_Data.csv')
    
    # حساب الـ Revenue لو مش موجود
    if 'Revenue' not in df.columns:
        if 'Quantity' in df.columns and 'UnitPrice' in df.columns:
            df['Revenue'] = df['Quantity'] * df['UnitPrice']
        elif 'TotalAmount' in df.columns:
            df.rename(columns={'TotalAmount': 'Revenue'}, inplace=True)
            
    # التأكد من نوع بيانات التاريخ لو موجود
    if 'InvoiceDate' in df.columns:
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
        
    return df

try:
    df = load_data()

    # 3. السايد بار (Sidebar)
    st.sidebar.header("📊 Control Panel")
    st.sidebar.markdown("Filter your data here:")
    
    countries = st.sidebar.multiselect(
        "Select Countries:", 
        options=df['Country'].unique().tolist(), 
        default=df['Country'].unique().tolist()[:3]
    )
    
    filtered_df = df[df['Country'].isin(countries)]

    # 4. العنوان الرئيسي
    st.title("🚀 E-commerce Customer Strategy Dashboard")
    st.info("This dashboard provides real-time insights into customer behavior and sales performance.")
    st.markdown("---")

    # 5. قسم الأرقام المحورية (KPIs)
    col1, col2, col3, col4 = st.columns(4)
    
    total_rev = filtered_df['Revenue'].sum()
    total_orders = filtered_df['InvoiceNo'].nunique()
    total_customers = filtered_df['CustomerID'].nunique()
    avg_order = total_rev / total_orders if total_orders > 0 else 0

    col1.metric("Total Revenue", f"${total_rev:,.0f}")
    col2.metric("Total Orders", f"{total_orders:,}")
    col3.metric("Total Customers", f"{total_customers:,}")
    col4.metric("Avg Order Value", f"${avg_order:.2f}")

    st.markdown("---")

    # 6. قسم الرسوم البيانية (توزيع احترافي)
    row1_col1, row1_col2 = st.columns([6, 4])

    with row1_col1:
        st.subheader("📦 Top Selling Products")
        top_products = filtered_df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_products = px.bar(top_products, x='Quantity', y='Description', orientation='h', 
                             color='Quantity', color_continuous_scale='Viridis',
                             labels={'Description': 'Product Name', 'Quantity': 'Units Sold'})
        fig_products.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_products, use_container_width=True)

    with row1_col2:
        st.subheader("🌍 Revenue by Country")
        rev_country = filtered_df.groupby('Country')['Revenue'].sum().reset_index()
        fig_country = px.pie(rev_country, values='Revenue', names='Country', hole=0.5,
                            color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_country, use_container_width=True)

    # 7. قسم تحليل الـ Clusters (لو البيانات فيها تقسيم)
    st.markdown("---")
    if 'Cluster' in filtered_df.columns:
        st.subheader("👥 Customer Segments Distribution")
        fig_clusters = px.scatter(filtered_df, x='Quantity', y='Revenue', color='Cluster',
                                 title="Customer Value Segmentation",
                                 log_x=True, size_max=40)
        st.plotly_chart(fig_clusters, use_container_width=True)
    else:
        st.subheader("💡 Business Insight")
        st.write("Most of your revenue is coming from the top 3 countries selected. Consider targeted marketing campaigns in these regions.")

except Exception as e:
    st.error(f"Something went wrong: {e}")
    st.info("Check if 'Cleaned_Ecommerce_Data.csv' is uploaded to your GitHub repository.")
