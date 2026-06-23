import streamlit as st
import matplotlib.pyplot as plt

def plot_manufacturer_contribution(df):
    # Diagnostic output
    st.write("COLUMN NAMES:", df.columns.tolist())
    st.write("Sample Data:", df.head())

    # Use only the ACTUAL column names
    if 'Mfg_Name_V' not in df or 'Stk_Stock_N' not in df:
        st.error("'Mfg_Name_V' or 'Stk_Stock_N' column not found in DataFrame.")
        return

    clean_df = df.dropna(subset=['Mfg_Name_V'])
    if clean_df.empty:
        st.error("No records after dropping rows with missing manufacturer names.")
        return

    # Only use existing columns
    manufacturer_stock_value = clean_df.groupby('Mfg_Name_V')['Stk_Stock_N'].sum().sort_values(ascending=False)
    if manufacturer_stock_value.empty:
        st.warning("No manufacturer data to display.")
        return

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