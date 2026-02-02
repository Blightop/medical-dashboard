# 🏥 Hong Kong Hospital Authority: Financial Dashboard
A data science project analyzing 3 years of HK Hospital Authority income and expenditure data (2021-2024), visualized using Streamlit.

# 📌 Project Overview
The goal of this project is to provide a clear visualization of how public funds are allocated within the HK hospital system. This dashboard allows users to track spending trends across staff costs, drugs, and medical equipment.

# 🛠️ The "Data Rebuilding" Process
The raw data from the Hospital Authority was provided in a format intended for reading, not for computing (merged headers and complex strings). I performed the following ETL (Extract, Transform, Load) steps:
- Data Cleaning: Used Pandas to skip non-data headers and rename columns for programmatic use.
- Lambda Transformations: Simplified financial year strings (e.g., converting "2021-22 (for the year ended...)" to "2021-22").
- Type Casting: Converted financial strings into numeric floats for calculation.

# 📊 Key Insights
# STILL IN PROGRESS. INFORMATION IN DEVELOPMENT.

# 🚀 How to Run the App (NOT RECOMMEND YET)
1. Clone the repo:
```
git clone https://github.com/yourusername/hk-hospital-dashboard.git
```
2. Install dependencies: (NOT AVAILABLE YET)
```
pip install -r requirements.txt
```
3. Run the Streamlit app:
```
streamlit run app.py
```

# 🧰 Tech Stack

Language: Python

Library: Pandas (Data Wrangling)

Visualization: Streamlit & Plotly

Data Source: [HK Hospital Authority Open Data](https://www3.ha.org.hk/Data/HAStatistics/MajorReport)
