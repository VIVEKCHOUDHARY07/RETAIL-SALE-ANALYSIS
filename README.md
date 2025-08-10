🏪 Retail Sales Analytics Dashboard

A comprehensive Business Intelligence Dashboard built with Streamlit for real-time retail sales analysis. This interactive web application provides executives and analysts with powerful insights into sales performance, customer demographics, and profitability metrics through dynamic visualizations and filtering capabilities.

📊 Interactive Business Intelligence

    Real-time KPI calculations (Revenue, Profit, Transactions, Customer metrics)

    Dynamic filtering by date range, product categories, and customer demographics

    Executive-level insights with automated business recommendations

📈 Advanced Analytics & Visualizations

    Sales Trend Analysis: Monthly revenue trends and transaction patterns

    Customer Demographics: Age group and gender-based purchasing analysis

    Profitability Analysis: Profit margin distributions and top/bottom transactions

    Category Performance: Revenue analysis across product categories

    Advanced Insights: Category vs profitability scatter plots and revenue heatmaps

🗄️ Database Integration

    MySQL database connectivity with SQLAlchemy ORM

    Live data extraction with optimized SQL queries

    Advanced data preprocessing and feature engineering

    Automated data caching for improved performance

📤 Export & Reporting

    CSV export functionality for filtered datasets

    Automated business insights generation

    Professional dashboard styling with dark theme

🛠️ Tech Stack

    Frontend: Streamlit, HTML/CSS

    Visualization: Plotly Express, Plotly Graph Objects

    Database: MySQL, SQLAlchemy

    Data Processing: Pandas, NumPy

    Backend: Python 3.9+

📋 Prerequisites

    Python 3.9 or higher

    MySQL Server

    Git



## Installation

1. Clone the Repository

```bash
 git clone https://github.com/VIVEKCHOUDHARY07/REATAIL-SALES-ANALYSIS.git
cd RETAIL-SALES-ANALYSIS

```
2. Create Virtual Environment

```bash
 python -m venv streamlit_env
# Windows
streamlit_env\Scripts\activate
# Mac/Linux
source streamlit_env/bin/activate

```
3. Install Dependencies

```bash
 pip install -r requirements.txt

```
4. Database Setup

```bash
 -- Create database
CREATE DATABASE retail_sales_db;

-- Create table structure
USE retail_sales_db;
CREATE TABLE retail_sales (
    transaction_id INT PRIMARY KEY,
    sale_date DATE,
    customer_id INT,
    gender VARCHAR(10),
    age INT,
    category VARCHAR(50),
    quantity INT,
    price_per_unit DECIMAL(10,2),
    total_sale DECIMAL(10,2),
    cogs DECIMAL(10,2)
);

-- Import your retail sales data
LOAD DATA INFILE 'path/to/your/retail_data.csv' 
INTO TABLE retail_sales 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS;


```
5. Configure Database Connection

```bash
#add your mysql server credentials
 engine = create_engine("mysql+mysqlconnector://username:password@localhost/retail_sales_db")

```
6. Usage

```bash
 streamlit run retail_dashboard.py

```
🔮 Future Enhancements

    Predictive Analytics: Sales forecasting with machine learning

    Real-time Updates: Live data streaming capabilities

    Multi-store Support: Geographic analysis and store comparison

    Advanced Filters: Product-level filtering and search

    Mobile Optimization: Responsive design for mobile devices

    User Authentication: Role-based access control

    API Integration: RESTful API for external integrations

🤝 Contributing

    Fork the repository

    Create your feature branch (git checkout -b feature/AmazingFeature)

    Commit your changes (git commit -m 'Add some AmazingFeature')

    Push to the branch (git push origin feature/AmazingFeature)

    Open a Pull Request

📞 Support

If you encounter any issues or have questions:

    🐛 Bug Reports: GitHub Issues

    💡 Feature Requests: GitHub Discussions

    📧 Email Support: vivek.choudhary.0779@gmail.com

⭐ Show Your Support

If this project helped you, please consider giving it a ⭐ on GitHub!

Built with by Vivek Choudhary
