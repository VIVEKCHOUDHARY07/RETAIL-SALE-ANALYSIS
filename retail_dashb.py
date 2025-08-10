import streamlit as st
from datetime import datetime
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="RETAIL SALE ANALYSIS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Complete CSS styling with dark blue theme and turquoise headings
st.markdown(
    """
    <style>
    /* Dark navy blue background for the entire dashboard */
    .stApp {
        background-color: #001F3F !important;
        color: white !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #003366 !important;
    }

    /* Turquoise headings for all h2, h3, h4 tags */
    h1, h2, h3, h4 {
        color: #40E0D0 !important;
        font-weight: bold;
    }

    /* Title container: turquoise background with dark navy text */
    .container {
        background-color: #40E0D0 !important;
        border-radius: 10px;
        margin: 0px;
        padding: 10px;
    }

    /* Title text style */
    .main-header {
        font-size: 3rem;
        text-align: center;
        margin-bottom: 0rem;
        font-weight: 600;
        color: #001F3F !important;
    }

    /* KPI metric containers */
    .metric-container {
        background-color: #003366 !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
        color: white !important;
    }

    /* Ensure all text elements are white */
    .stMarkdown, .stText, p, span, div {
        color: white !important;
    }

    /* Metric values styling */
    [data-testid="metric-container"] {
        background-color: #003366 !important;
        border: 1px solid #40E0D0;
        padding: 1rem;
        border-radius: 10px;
        color: white !important;
    }

    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #003366 !important;
        color: white !important;
    }

    /* Success/warning/error message styling */
    .stAlert {
        color: #001F3F !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# MAIN TITLE
st.markdown('<div class="container"><h1 class="main-header">RETAIL SALE ANALYSIS DASHBOARD</h1></div>',
            unsafe_allow_html=True)


@st.cache_data(ttl=300)
def load_retail_data():
    try:
        engine = create_engine("mysql+mysqlconnector://root:vivek123@localhost/retail_sales_db")
        query = "SELECT * FROM RETAIL_SALES"
        df = pd.read_sql(query, engine)

        # Data preprocessing
        df['sale_date'] = pd.to_datetime(df['sale_date'])
        df['year'] = df['sale_date'].dt.year
        df['month'] = df['sale_date'].dt.month
        df['quarter'] = df['sale_date'].dt.quarter
        df['week_day'] = df['sale_date'].dt.day_name()

        # Calculate profit metrics
        df['profit'] = df['total_sale'] - df['cogs']
        df['profit_margin'] = (df['profit'] / df['total_sale']) * 100

        # Success message for debugging
        st.sidebar.success(f"Data loaded: {len(df):,} records")

        return df
    except Exception as e:
        st.error(f"Database Connection Failed: {e}")
        return None


def calculate_kpis(df):
    if df is None or df.empty:
        return None

    kpis = {
        'total_revenue': df['total_sale'].sum(),
        'total_transactions': len(df),
        'avg_transaction': df['total_sale'].mean(),
        'total_profit': df['profit'].sum(),
        'profit_margin': (df['profit'].sum() / df['total_sale'].sum()) * 100,
        'unique_customers': df['customer_id'].nunique(),
        'avg_revenue_per_customer': df['total_sale'].sum() / df['customer_id'].nunique(),
        'date_range_days': (df['sale_date'].max() - df['sale_date'].min()).days + 1
    }

    return kpis


# Load data
with st.spinner("Loading retail sales data..."):
    retail_data = load_retail_data()

if retail_data is None:
    st.error("Could not load data. Please check your database connection.")
    st.stop()

# SIDEBAR FILTERS
st.sidebar.header("Filter Your Data")

# Date range filter
min_date = retail_data['sale_date'].min().date()
max_date = retail_data['sale_date'].max().date()

date_range = st.sidebar.date_input(
    "Select sale date range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Category filter
category_list = retail_data['category'].unique()
selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    options=category_list,
    default=category_list
)

# Gender filter
gender_list = retail_data['gender'].unique()
selected_genders = st.sidebar.multiselect(
    "Select Customer Gender",
    options=gender_list,
    default=gender_list
)

# Filter data based on selections
filtered_data = retail_data[
    (retail_data['sale_date'].dt.date >= date_range[0]) &
    (retail_data['sale_date'].dt.date <= date_range[1]) &
    (retail_data['category'].isin(selected_categories)) &
    (retail_data['gender'].isin(selected_genders))
    ]

# Show filtered data count
st.sidebar.markdown(f"**{len(filtered_data):,} records match your filters**")

# Preview filtered data
with st.expander("Preview Filtered Data"):
    st.dataframe(filtered_data.head())

# KPI METRICS DASHBOARD
st.markdown("## Executive Snapshot")

if not filtered_data.empty:
    # Calculate KPIs
    total_revenue = filtered_data['total_sale'].sum()
    total_cogs = filtered_data['cogs'].sum()
    total_profit = filtered_data['profit'].sum()
    avg_transaction = filtered_data['total_sale'].mean()
    gross_profit_margin = (total_profit / total_revenue) * 100 if total_revenue != 0 else 0
    total_transactions = len(filtered_data)
    unique_customers = filtered_data['customer_id'].nunique()
    avg_revenue_per_customer = total_revenue / unique_customers if unique_customers > 0 else 0
    avg_profit_per_transaction = filtered_data['profit'].mean()
    top_category = filtered_data.groupby('category')['total_sale'].sum().idxmax() if not filtered_data.empty else None
    top_category_revenue = filtered_data.groupby('category')['total_sale'].sum().max() if not filtered_data.empty else 0
    date_range_days = (filtered_data['sale_date'].max() - filtered_data[
        'sale_date'].min()).days + 1 if total_transactions > 0 else 0

    # Display KPIs across 4 columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Revenue", f"${total_revenue:,.2f}")
    kpi2.metric("Total Profit", f"${total_profit:,.2f}", f"{gross_profit_margin:.2f}% margin")
    kpi3.metric("Transactions", f"{total_transactions:,}")
    kpi4.metric("Unique Customers", f"{unique_customers:,}")

    # Additional KPIs in second row
    kpi5, kpi6, kpi7, kpi8 = st.columns(4)
    kpi5.metric("Avg Transaction Value", f"${avg_transaction:.2f}")
    kpi6.metric("Avg Profit per Transaction", f"${avg_profit_per_transaction:.2f}")
    kpi7.metric("Top Category", f"{top_category if top_category else 'N/A'}")
    kpi8.metric("Days Shown", f"{date_range_days:,}")

    st.divider()

else:
    st.warning("No data for selected filters. Please expand filters.")

# SALES TREND VISUALIZATIONS
st.markdown("## Sales Trend Analysis")

if not filtered_data.empty:
    # Monthly Revenue Trend
    monthly_sales = (
        filtered_data
        .groupby([filtered_data['sale_date'].dt.to_period("M")])
        .agg(total_sales=('total_sale', 'sum'),
             transaction_count=('transaction_id', 'count'))
        .reset_index()
    )
    monthly_sales['sale_date'] = monthly_sales['sale_date'].dt.to_timestamp()

    fig_monthly = px.line(
        monthly_sales,
        x='sale_date',
        y='total_sales',
        title="Monthly Revenue Trend",
        markers=True,
        labels={'sale_date': 'Month', 'total_sales': 'Total Sales ($)'},
        template="plotly_dark"
    )
    fig_monthly.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        legend=dict(
            font_color='white'
        )
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Revenue by Category
    category_sales = (
        filtered_data.groupby('category')['total_sale']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )

    fig_category = px.bar(
        category_sales,
        x='category',
        y='total_sale',
        title="Revenue by Category",
        labels={'total_sale': 'Total Sales ($)', 'category': 'Category'},
        template="plotly_dark"
    )
    fig_category.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        legend=dict(
            font_color='white'
        )
    )
    st.plotly_chart(fig_category, use_container_width=True)

    # Sales by Day of Week
    weekday_sales = (
        filtered_data.groupby('week_day')['total_sale']
        .sum()
        .reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
        .reset_index()
    )

    fig_weekday = px.bar(
        weekday_sales,
        x='week_day',
        y='total_sale',
        title="Revenue by Day of Week",
        labels={'total_sale': 'Total Sales ($)', 'week_day': 'Weekday'},
        template="plotly_dark"
    )
    fig_weekday.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        legend=dict(
            font_color='white'
        )
    )
    st.plotly_chart(fig_weekday, use_container_width=True)

else:
    st.warning("No data available to display charts for selected filters.")

# CUSTOMER DEMOGRAPHICS & PROFITABILITY
st.markdown("## Customer Demographics & Profitability Analysis")

if not filtered_data.empty:
    # Layout: two charts side by side
    demo_col1, demo_col2 = st.columns(2)

    # Gender Sales Distribution
    gender_sales = filtered_data.groupby('gender')['total_sale'].sum().reset_index()

    fig_gender = px.pie(
        gender_sales,
        names='gender',
        values='total_sale',
        title="Sales by Gender",
        hole=0.4,
        template="plotly_dark"
    )
    fig_gender.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        legend=dict(
            font_color='white'
        )
    )
    fig_gender.update_traces(
        textfont_color='white'
    )
    demo_col1.plotly_chart(fig_gender, use_container_width=True)

    # Age Group Sales
    age_bins = [0, 25, 35, 45, 55, 100]
    age_labels = ['18-25', '26-35', '36-45', '46-55', '55+']
    filtered_data['age_group'] = pd.cut(filtered_data['age'], bins=age_bins, labels=age_labels)

    age_sales = (
        filtered_data.groupby('age_group')['total_sale']
        .sum()
        .reindex(age_labels)
        .reset_index()
    )

    fig_age = px.bar(
        age_sales,
        x='age_group',
        y='total_sale',
        title="Sales by Age Group",
        labels={'total_sale': 'Total Sales ($)', 'age_group': 'Age Group'},
        template="plotly_dark"
    )
    fig_age.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        legend=dict(
            font_color='white'
        )
    )
    demo_col2.plotly_chart(fig_age, use_container_width=True)

    st.divider()

    # Profitability Section
    prof_col1, prof_col2 = st.columns(2)

    # Profit Margin Distribution
    fig_margin = px.histogram(
        filtered_data,
        x='profit_margin',
        nbins=20,
        title="Profit Margin Distribution",
        labels={'profit_margin': 'Profit Margin (%)'},
        template="plotly_dark"
    )
    fig_margin.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        legend=dict(
            font_color='white'
        )
    )
    prof_col1.plotly_chart(fig_margin, use_container_width=True)

    # Top 5 & Bottom 5 Transactions
    top_trans = filtered_data.nlargest(5, 'profit')[
        ['transaction_id', 'category', 'total_sale', 'cogs', 'profit', 'profit_margin']]
    bottom_trans = filtered_data.nsmallest(5, 'profit')[
        ['transaction_id', 'category', 'total_sale', 'cogs', 'profit', 'profit_margin']]

    prof_col2.markdown("### Top 5 Profitable Transactions")
    prof_col2.dataframe(
        top_trans.style.format({
            'total_sale': '${:,.2f}',
            'cogs': '${:,.2f}',
            'profit': '${:,.2f}',
            'profit_margin': '{:.2f}%'
        }),
        use_container_width=True
    )

    with st.expander("Bottom 5 Least Profitable Transactions"):
        st.dataframe(
            bottom_trans.style.format({
                'total_sale': '${:,.2f}',
                'cogs': '${:,.2f}',
                'profit': '${:,.2f}',
                'profit_margin': '{:.2f}%'
            }),
            use_container_width=True
        )

else:
    st.warning("No demographic or profitability data for selected filters.")

# ADVANCED INSIGHTS & EXPORT
st.markdown("## Advanced Insights")

if not filtered_data.empty:
    adv_col1, adv_col2 = st.columns(2)

    # Category vs Average Profitability Scatter
    category_profit = (
        filtered_data
        .groupby('category')
        .agg(avg_profit=('profit', 'mean'),
             total_sales=('total_sale', 'sum'))
        .reset_index()
    )

    fig_profit_scatter = px.scatter(
        category_profit,
        x='total_sales',
        y='avg_profit',
        text='category',
        size='total_sales',
        color='avg_profit',
        title="Category vs Average Profitability",
        labels={'total_sales': 'Total Sales ($)', 'avg_profit': 'Average Profit ($)'},
        template="plotly_dark",
        color_continuous_scale='Viridis'
    )
    fig_profit_scatter.update_traces(
        textposition='top center',
        textfont_color='white'
    )
    fig_profit_scatter.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white',
            gridcolor='rgba(255,255,255,0.2)'
        ),
        legend=dict(
            font_color='white'
        ),
        coloraxis_colorbar=dict(
            title_font_color='white',
            tickfont_color='white'
        )
    )
    adv_col1.plotly_chart(fig_profit_scatter, use_container_width=True)

    # Monthly Revenue Heatmap
    monthly_matrix = (
        filtered_data
        .groupby(['year', 'month'])
        .agg(total_sales=('total_sale', 'sum'),
             total_profit=('profit', 'sum'))
        .reset_index()
    )

    monthly_matrix['month_name'] = monthly_matrix['month'].apply(lambda x: datetime(1900, x, 1).strftime('%b'))
    pivot_sales = monthly_matrix.pivot(index='year', columns='month_name', values='total_sales')

    fig_heatmap = px.imshow(
        pivot_sales,
        labels=dict(x="Month", y="Year", color="Revenue ($)"),
        x=pivot_sales.columns,
        y=pivot_sales.index,
        text_auto=True,
        aspect="auto",
        title="Monthly Revenue Heatmap",
        color_continuous_scale="Blues"
    )
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        title_font_color='white',
        xaxis=dict(
            title_font_color='white',
            tickfont_color='white'
        ),
        yaxis=dict(
            title_font_color='white',
            tickfont_color='white'
        ),
        coloraxis_colorbar=dict(
            title_font_color='white',
            tickfont_color='white'
        )
    )
    fig_heatmap.update_traces(
        textfont_color='white'
    )
    adv_col2.plotly_chart(fig_heatmap, use_container_width=True)

    st.divider()

    # Download Filtered Data
    st.markdown("### Download Filtered Dataset")


    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')


    csv_data = convert_df_to_csv(filtered_data)

    st.download_button(
        label="Download as CSV",
        data=csv_data,
        file_name=f"retail_sales_filtered_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime='text/csv'
    )

else:
    st.warning("No advanced insight data for selected filters.")


# Auto Insights
def generate_auto_insights(df):
    insights = []
    if df.empty:
        return ["No data available for selected filters."]

    total_rev = df['total_sale'].sum()
    top_cat = df.groupby('category')['total_sale'].sum().idxmax()
    top_cat_sales = df.groupby('category')['total_sale'].sum().max()
    best_day = df.groupby('week_day')['total_sale'].sum().idxmax()
    avg_margin = df['profit_margin'].mean()

    insights.append(f"Total revenue in this selection is **${total_rev:,.2f}**.")
    insights.append(f"**{top_cat}** is the top category with ${top_cat_sales:,.2f} in sales.")
    insights.append(f"**{best_day}** has the highest sales in this period.")
    insights.append(f"Average profit margin is **{avg_margin:.2f}%**.")

    # Conditional insights
    if avg_margin < 20:
        insights.append("Profit margins are relatively low — review pricing or costs.")
    elif avg_margin > 40:
        insights.append("High profit margins — pricing strategy is working well.")

    return insights


# Display auto insights
st.markdown("### Auto Insights")
for point in generate_auto_insights(filtered_data):
    st.markdown(f"- {point}")
