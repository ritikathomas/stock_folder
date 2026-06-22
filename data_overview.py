import streamlit as st
import pandas as pd


def show_data_overview(df):
    st.subheader("Data Overview")
    st.write(df.head(10))



    st.subheader("Total Stock Across All Products")
    total_stock = df.groupby('ReportDate')['Stk_Stock_N'].sum()
    st.line_chart(total_stock)
    st.divider()