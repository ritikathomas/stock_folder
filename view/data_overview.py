import streamlit as st
import pandas as pd


def show_data_overview(df):
    st.subheader("Product Data Preview")
    st.dataframe(df.head(10), use_container_width=True)
    st.markdown("---")

    st.subheader("Total Stock Over Time")
    total_stock = df.groupby('ReportDate')['Stk_Stock_N'].sum()
    st.line_chart(total_stock)