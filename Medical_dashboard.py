#import libs
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from datetime import datetime


#load data
@st.cache_data
def load_data():
    df_agg = pd.read_excel('raw data\eng\Key-financial-information-HA-en.xlsx', engine='openpyxl').iloc[3:,:]
    df_agg.columns = ['year','gov_subvention','med_fee','non_med_fee','donate','cap_donate','total','staff_cost','drugs','med_supplies','other_exp','total_exp','surplus_deficit']
    #cleaning years
    df_agg['year'] = df_agg['year'].apply(lambda x: str(x).split('-')[0])
    df_agg['year'] = pd.to_datetime(df_agg['year'])
    #turn to float types
    cols_to_fix = ['staff_cost', 'drugs', 'med_supplies', 'other_exp', 'total_exp']
    for col in cols_to_fix:
        df_agg[col] = pd.to_numeric(df_agg[col], errors='coerce')
    return df_agg


