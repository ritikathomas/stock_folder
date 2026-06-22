#Stm_SalesDesc_V
import streamlit as st
import pandas as pd

from Columns.mfg_companies import *
from Columns.unit_types import *


if category == "Products":
    selected_item = st.sidebar.selectbox(
        "Select a Product", 
        options=[None] + df['Stm_SalesDesc_V'].unique().tolist(),
        format_func=lambda x: "-- Select a Product --" if x is None else x,
        key='item_selectbox')
    column_name = 'Stm_SalesDesc_V'

with col2:
    products = st.multiselect(
        "Products",
        options=filtered_data['Stm_SalesDesc_V'].unique().tolist(),
        default=filtered_data['Stm_SalesDesc_V'].unique().tolist(),
        key='product_filter' )
    
            