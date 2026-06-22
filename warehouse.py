#Shm_Name_V
import streamlit as st
import pandas as pd


if category == "Warehouse/Storage":
        selected_item = st.sidebar.selectbox(
            "Select a Warehouse/Storage", 
            options=[None] + df['Shm_Name_V'].unique().tolist(),
            format_func=lambda x: "-- Select a Warehouse/Storage --" if x is None else x,
            key='item_selectbox')
        column_name = 'Shm_Name_V'