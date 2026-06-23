import streamlit as st
import matplotlib.pyplot as plt

import streamlit as st
import matplotlib.pyplot as plt

def plot_manufacturer_contribution(df):
    if 'Mfg_Name_V' not in df or 'Stk_Stock_N' not in df:
        st.error("Column 'Mfg_Name_V' or 'Stk_Stock_N' not found in DataFrame!")
        return

    grouped = df.dropna(subset=['Mfg_Name_V']).groupby('Mfg_Name_V')['Stk_Stock_N'].sum()
    if grouped.empty:
        st.error("Grouping by 'Mfg_Name_V' yielded no results.")
        return
    grouped = grouped.sort_values(ascending=False)[:10]  # Top 10

    plt.figure(figsize=(10, 6))
    grouped.plot(kind='barh', color='skyblue')
    plt.xlabel('Total Stock')
    plt.ylabel('Manufacturer')
    plt.title('Top 10 Manufacturers by Total Stock')
    plt.gca().invert_yaxis()
    st.pyplot(plt)