#Unh_Code_V
import streamlit as st
import pandas as pd


if category == "Unit Types":
    selected_item = st.sidebar.selectbox(
            "Select a Unit Type", 
            options=[None] + df['Unh_Code_V'].unique().tolist(),
            format_func=lambda x: "-- Select a Unit Type --" if x is None else x,
            key='item_selectbox')
    column_name = 'Unh_Code_V'