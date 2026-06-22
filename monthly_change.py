import streamlit as st
import pandas as pd

def show_monthly_change(df):
    """Displays monthly percent changes in stock, stockouts, and costs."""
    df = df.copy()
    df['ReportDate'] = pd.to_datetime(df['ReportDate'])
    df['YearMonth'] = df['ReportDate'].dt.to_period('M')
    monthly_stock = df.groupby('YearMonth')['Stk_Stock_N'].sum()
    monthly_stockouts = df.groupby('YearMonth').apply(lambda x: (x['Stk_Stock_N'] == 0).sum())
    monthly_costs = df.groupby('YearMonth')['Stk_Cost_N'].sum()
    monthly_stock_pct = monthly_stock.pct_change() * 100
    monthly_stockouts_pct = monthly_stockouts.pct_change() * 100
    monthly_costs_pct = monthly_costs.pct_change() * 100

    st.subheader("Monthly Percent Change in Stock, Stockouts, and Costs")
    st.markdown("**% change calculated month-over-month**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(":package: **Stock Level % Change**")
        st.line_chart(monthly_stock_pct)
    with col2:
        st.write(":x: **Stockouts % Change**")
        st.line_chart(monthly_stockouts_pct)
    with col3:
        st.write(":moneybag: **Value/Cost % Change**")
        st.line_chart(monthly_costs_pct)
    st.markdown("---")
    st.write("**Raw data (% change):**")
    pct_df = pd.DataFrame({
        'Stock Level % Change': monthly_stock_pct,
        'Stockouts % Change': monthly_stockouts_pct,
        'Costs % Change': monthly_costs_pct,
    })
    st.dataframe(pct_df, use_container_width=True)
