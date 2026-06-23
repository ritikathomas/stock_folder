import streamlit as st
import matplotlib.pyplot as plt

def plot_manufacturer_contribution(df):
    # Ensure the columns exist
    if 'Mfg_Name_V' not in df or 'Stk_Stock_N' not in df:
        st.error("Column 'Mfg_Name_V' or 'Stk_Stock_N' not found in DataFrame!")
        return

    grouped = df.dropna(subset=['Mfg_Name_V']).groupby('Mfg_Name_V')['Stk_Stock_N'].sum()
    if grouped.empty:
        st.error("Grouping by 'Mfg_Name_V' yielded no results.")
        return
    grouped = grouped.sort_values(ascending=False)
    latest_date = df['ReportDate'].max()

    plt.figure(figsize=(12, 10))
    top_n = 10
    other_value = grouped.iloc[top_n:].sum()
    manufacturer_stock_value_plot = grouped.iloc[:top_n]
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