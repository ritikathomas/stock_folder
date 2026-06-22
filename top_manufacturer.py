import streamlit as st
import pandas as pd


def show_top_manufacturer(df):
    st.subheader("Top Manufacturer by Stock Value")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_date = st.date_input("Select Date:", value=pd.to_datetime(df['ReportDate'].max()).date())
        selected_date_ts = pd.to_datetime(selected_date)
        date_data = df[df['ReportDate'] == selected_date_ts]
        
        if not date_data.empty:
            manufacturer_stock_value = date_data.groupby('Mfg_Name_V')['Stk_Cost_N'].sum()
            top_manufacturer = manufacturer_stock_value.idxmax()
            top_value = manufacturer_stock_value.max()
            
            with col2:
                st.write(f"**Top Manufacturer:**")
                st.write(f"{top_manufacturer}")
            with col3:
                st.write(f"**Stock Value:**")
                st.write(f"${top_value:,.2f}")
        else:
            with col2:
                st.warning(f"No data for {selected_date}")
    
    st.divider()

    # If top_manufacturer was found, plot its stock time-series + styled table
    if 'top_manufacturer' in locals() and top_manufacturer:
        st.subheader(f"Stock Levels Over Time for {top_manufacturer}")
        # Filter df for the top manufacturer
        top_mfg_data = df[df['Mfg_Name_V'] == top_manufacturer]
        stock_over_time = top_mfg_data.groupby('ReportDate')['Stk_Stock_N'].sum().sort_index()
        st.line_chart(stock_over_time)

        st.subheader(f"Detailed Records for {top_manufacturer}")
        st.dataframe(top_mfg_data, use_container_width=True)

