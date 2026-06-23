import streamlit as st
import matplotlib.pyplot as plt

def plot_manufacturer_contribution(df):
    # Adjust the column names below to match your data!
    manufacturer_stock_value = df.groupby('Mfg_Name_V')['Stk_Stock_N'].sum().sort_values(ascending=False)
    latest_date = df['ReportDate'].max()

    plt.figure(figsize=(12, 10))
    top_n = 10
    other_value = manufacturer_stock_value.iloc[top_n:].sum()
    manufacturer_stock_value_plot = manufacturer_stock_value.iloc[:top_n]
    if other_value > 0:
        manufacturer_stock_value_plot['Others'] = other_value
    plt.pie(
        manufacturer_stock_value_plot,
        labels=manufacturer_stock_value_plot.index,
        autopct='%1.1f%%',
        startangle=140,
        rotatelabels=True,
        pctdistance=0.85
    )
    plt.title(
        f"Manufacturer Contribution to Total Stock (as of {latest_date.strftime('%Y-%m-%d')})",
        fontsize=14
    )
    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(plt)