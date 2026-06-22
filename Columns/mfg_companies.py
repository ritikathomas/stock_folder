#Mfg_Name_V

import streamlit as st
import pandas as pd


if category == "Manufacturing Companies":        
    selected_item = st.sidebar.selectbox(
            "Select a Company", 
            options=[None] + df['Mfg_Name_V'].unique().tolist(),
            format_func=lambda x: "-- Select a Company --" if x is None else x,
            key='item_selectbox')
    column_name = 'Mfg_Name_V'

with col1:
    manufacturers = st.multiselect(
        "Manufacturers",
        options=filtered_data['Mfg_Name_V'].unique().tolist(),
        default=filtered_data['Mfg_Name_V'].unique().tolist(),
        key='mfg_filter'
                )

