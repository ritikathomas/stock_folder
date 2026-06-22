import streamlit as st
import pandas as pd
from view import (
    show_data_overview,
    show_category_chart,
    show_search_product_id,
    show_top_manufacturer,
)


@st.cache_data
def load_data():
    df = pd.read_parquet(r"C:\Users\ritik\Downloads\stock_daily_cleaned.parquet")
    return df

def main():
    st.set_page_config(page_title="Inventory Analysis", layout="wide")
    st.title('Inventory Analysis Dashboard')
    df = load_data()

    st.sidebar.title("Navigation")
    # Out-of-stock and low-stock sets (must be defined before nav labels)
    LOW_STOCK_THRESHOLD = 5
    out_of_stock = df[df['Stk_Stock_N'] == 0]
    low_stock = df[(df['Stk_Stock_N'] > 0) & (df['Stk_Stock_N'] <= LOW_STOCK_THRESHOLD)]

    # Compose navigation labels to include counts
    out_of_stock_label = f"Out-of-Stock ({len(out_of_stock)})" if not out_of_stock.empty else "Out-of-Stock"
    low_stock_label = f"Critically Low Stock ({len(low_stock)})" if not low_stock.empty else "Critically Low Stock"
    # Calculate top over- and under-stocked manufacturers (display only names for nav)
    overstock_threshold = df['Stk_Stock_N'].quantile(0.9)
    understock_threshold = 5
    overstock_counts = df[df['Stk_Stock_N'] >= overstock_threshold].groupby('Mfg_Name_V').size().sort_values(ascending=False)
    understock_counts = df[df['Stk_Stock_N'] <= understock_threshold].groupby('Mfg_Name_V').size().sort_values(ascending=False)
    top_overstock = overstock_counts.head(3)
    top_understock = understock_counts.head(3)
    # --- Trend Data ---
    df['ReportDate'] = pd.to_datetime(df['ReportDate'])
    df['YearMonth'] = df['ReportDate'].dt.to_period('M')
    monthly_over = df[df['Stk_Stock_N'] >= overstock_threshold].groupby(['YearMonth', 'Mfg_Name_V']).size().unstack(fill_value=0)
    monthly_under = df[df['Stk_Stock_N'] <= understock_threshold].groupby(['YearMonth', 'Mfg_Name_V']).size().unstack(fill_value=0)
    trend_overstock_mfgs = monthly_over[top_overstock.index]
    trend_understock_mfgs = monthly_under[top_understock.index]
    overstock_trend_label = "Overstock Trend"
    understock_trend_label = "Understock Trend"
    nav_options = [
        "Overview",
        "Category Analysis",
        "Top Manufacturer",
        "Search",
        out_of_stock_label,
        low_stock_label,
        overstock_trend_label,
        understock_trend_label,
    ]
    page = st.sidebar.radio(
        " ",
        nav_options
    )
    st.sidebar.divider()
    st.sidebar.info(f"Total Records: {len(df):,}")

    # Show main navigation
    if page == "Overview":
        show_data_overview(df)
    elif page == "Category Analysis":
        show_category_chart(df)
    elif page == "Top Manufacturer":
        show_top_manufacturer(df)
    elif page == "Search":
        show_search_product_id(df)
    elif page == out_of_stock_label:
        st.subheader("Out-of-Stock Items")
        if not out_of_stock.empty:
            st.dataframe(out_of_stock, use_container_width=True)
        else:
            st.info("No items are currently out of stock.")
    elif page == low_stock_label:
        st.subheader(f"Critically Low Stock (≤ {LOW_STOCK_THRESHOLD} units)")
        if not low_stock.empty:
            st.dataframe(low_stock, use_container_width=True)
        else:
            st.info(f"No items are below critical stock threshold (≤ {LOW_STOCK_THRESHOLD} units).")
    elif page == overstock_trend_label:
        st.subheader("Monthly Trend: Overstocked Items by Top Manufacturers")
        if not trend_overstock_mfgs.empty:
            st.line_chart(trend_overstock_mfgs)
            st.subheader("Top Manufacturers with Overstocked Items (≥ 90th percentile)")
            st.write(top_overstock.to_frame('Overstocked Items').reset_index())
        else:
            st.info("No overstocked trend data available.")
    elif page == understock_trend_label:
        st.subheader("Monthly Trend: Understocked Items by Top Manufacturers")
        if not trend_understock_mfgs.empty:
            st.line_chart(trend_understock_mfgs)
            st.subheader(f"Top Manufacturers with Understocked Items (≤ {understock_threshold} units)")
            st.write(top_understock.to_frame('Understocked Items').reset_index())
        else:
            st.info("No understocked trend data available.")
    

    


if __name__ == '__main__':
    main()


