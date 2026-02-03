#import libs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime


#@st.cache
def load_data():
    # --- Fianical ---
    df_finan = pd.read_excel('raw data\eng\Key-financial-information-HA-en.xlsx', engine='openpyxl').iloc[3:,:]
    df_finan.columns = ['year','gov_subvention','med_fee','non_med_fee','donate','cap_donate','total','staff_cost','drugs','med_supplies','other_exp','total_exp','surplus_deficit']
    #cleaning years
    df_finan['year'] = df_finan['year'].apply(lambda x: str(x).split('-')[0])
    df_finan['year'] = pd.to_datetime(df_finan['year'])
    #turn to float types
    cols_to_fix = ['gov_subvention','med_fee','non_med_fee','donate','cap_donate','total','staff_cost','drugs','med_supplies','other_exp','total_exp','surplus_deficit']
    for col in cols_to_fix:
        df_finan[col] = pd.to_numeric(df_finan[col], errors='coerce')

    # --- manpower ---
    df_staffnum = pd.read_excel('raw data\eng\manpower-position-by-staff-group-en.xlsx', engine='openpyxl').iloc[15:18,:]
    df_staffnum.columns = ['year','medical','nursing','allied_health','management','care_support','others','overall']
    #cleaning years
    df_staffnum['year'] = df_staffnum['year'].apply(lambda x: str(x).split('-')[0])
    df_staffnum['year'] = pd.to_datetime(df_staffnum['year'])
    #turn to float types
    cols_to_fix = ['medical','nursing','allied_health','management','care_support','others','overall']
    for col in cols_to_fix:
        df_staffnum[col] = pd.to_numeric(df_staffnum[col], errors='coerce')

    return df_finan, df_staffnum

df_finan, df_staffnum = load_data()

#engineering
#percentage change
df_finan_diff = df_finan.copy()
#median to find the average point (non bias)
median_finana = df_finan_diff.median()

#streamlit properties

#sidebar
add_sidebar = st.sidebar.selectbox('Aggregate or individual variables',('Main menu','Fiance','Individual Year'))

if add_sidebar == 'Main menu':
    st.title("HK Hospital Authority Overview")
    latest_year_val = df_finan['year'].iloc[-1].year
    st.markdown(f"### Median spending comparison with the {latest_year_val} report")
    #data calculate
    metric_cols = ['gov_subvention','med_fee','non_med_fee','donate','cap_donate','total','staff_cost','drugs','med_supplies','other_exp','total_exp','surplus_deficit'] #cols to test
    metric_median = df_finan[metric_cols].median() #median of the entire 3 year period
    latest_year_data = df_finan[metric_cols].iloc[-1] #current data

    

    #build column
    #loop through columns
    for i in range(0, len(metric_cols), 5):
        #fresh column
        cols = st.columns(5)
        #get the next 5 metrics
        chunk = metric_cols[i : i + 5]
        #fill in columns
        for index, col_name in enumerate(chunk):
            with cols[index]:
                #calculate % change: (Current - Median) / Median
                delta = (latest_year_data[col_name] - metric_median[col_name]) / metric_median[col_name]
                
                # Display the card
                st.metric(
                    label=col_name.replace('_', ' ').replace('med','Medical').replace('exp','Expense').title(), #format the names
                    value=f"{latest_year_data[col_name]:,.0f}", #format the value
                    delta="{:.2%}".format(delta) #format percentage
                )

if add_sidebar == 'Individual Year':
    year = tuple(df_finan['year'].dt.year.unique())
    year_select = st.selectbox('Pick a year', year)
    df_selected_year = df_finan[df_finan['year'].dt.year == year_select]


    def calculation(data):
        #data calculate -- first part --
        # Filter the dataframe based on the year selected
        metric_median = df_finan[data].median() #median of the entire 3 year period

        #build column
        #loop through columns
        for i in range(0, len(data), 5):
            #fresh column
            cols = st.columns(5)
            #get the next 5 metrics
            chunk = data[i : i + 5]
            #fill in columns
            for index, col_name in enumerate(chunk):
                with cols[index]:  
                    current_val = df_selected_year[col_name].iloc[0]
                    delta = (current_val - metric_median[col_name]) / metric_median[col_name]
                    # Display the card
                    st.metric(
                        label=col_name.replace('_', ' ').replace('med','Medical').replace('exp','Expense').title(), #format the names
                        value=f"{current_val:,.0f}", #format the value
                        delta="{:.2%}".format(delta) #format percentage
                    )

    #--- calculation of the cost ---
    st.title(f"{year_select} cost report")
    metric_cols = ['staff_cost','drugs','med_supplies','other_exp','total_exp','surplus_deficit'] #cols to test
    calculation(metric_cols)

    #--- bar chart ---
    #define catageroies
    expense_categories = ['staff_cost', 'drugs', 'med_supplies', 'other_exp']

    #get data
    #.melt = cols to rows
    df_bar = df_selected_year[expense_categories].melt(var_name='Category', value_name='Amount')

    #name clean up
    df_bar['Category'] = df_bar['Category'].replace({'staff_cost': 'Staff Costs', 
                                                    'drugs': 'Drugs', 
                                                    'med_supplies': 'Medical Supplies', 
                                                    'other_exp': 'Other Expenses'})
    #Chart
    st.title("Expenditure breadown")
    fig = px.bar(df_bar, 
                x='Category', 
                y='Amount', 
                title=f"Expenditure Breakdown for {year_select}",
                text_auto='.2s', # Shows the values on top of bars automatically
                color='Category') # Colors each bar differently

    #streamlit
    st.plotly_chart(fig, use_container_width=True)


    #--- calculation of government subvention, equipment and donations ---
    st.title("Government Subvention, equipment and donations")
    metric_cols_sec = ['gov_subvention','med_fee','non_med_fee','donate','cap_donate','total'] #cols to test
    calculation(metric_cols_sec)