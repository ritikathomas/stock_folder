#Ctg_Desc_V
import streamlit as st
import pandas as pd


if category == "Categories":
        selected_item = st.sidebar.selectbox(
            "Select a Category", 
            options=[None] + df['Ctg_Desc_V'].unique().tolist(),
            format_func=lambda x: "-- Select a Category --" if x is None else x,
            key='item_selectbox')
        column_name = 'Ctg_Desc_V'

with col3:
    categories = st.multiselect(
        "Categories",
        options=filtered_data['Ctg_Desc_V'].unique().tolist(),
        default=filtered_data['Ctg_Desc_V'].unique().tolist(),
        key='category_filter')