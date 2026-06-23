import streamlit as st
import pandas as pd
from view import (
    show_data_overview,
    show_category_chart,
    show_search_product_id,
    show_top_manufacturer,
)

# Inserted supply days calculation sub-function
import difflib
import re

def calculate_supply_days(
    df,
    product_input: str,
    avg_consumption_days: int
):
    """
    Returns: dict with keys:
      - selected_product
      - current_stock
      - average_daily_consumption
      - days_of_supply
      - message (for errors or info)
      - daily_stock_summary (pd.Series)
    """
    result = {
        "selected_product": None,
        "current_stock": None,
        "average_daily_consumption": None,
        "days_of_supply": None,
        "message": "",
        "daily_stock_summary": None
    }
    available_products = df['Stm_SalesDesc_V'].unique()
    selected_product_for_display = product_input
    product_name_for_filtering = product_input
    escaped_product_input = re.escape(product_input)
    initial_matches_df = df[df['Stm_SalesDesc_V'].str.contains(escaped_product_input, case=False, na=False)].copy()

    if initial_matches_df.empty:
        close_matches = difflib.get_close_matches(
            product_input.upper(),
            [name.upper() for name in available_products],
            n=1, cutoff=0.7
        )
        if close_matches:
            corrected = next(
                (name for name in available_products if name.upper() == close_matches[0]),
                product_input
            )
            selected_product_for_display = corrected
            product_name_for_filtering = corrected
            escaped_product_for_filtering = re.escape(product_name_for_filtering)
            initial_matches_df = df[df['Stm_SalesDesc_V'].str.contains(escaped_product_for_filtering, case=False, na=False)].copy()
            if initial_matches_df.empty:
                result["message"] = f"No data found for suggested product '{corrected}'."
                return result
        else:
            result["message"] = f"No match or suggestion found for '{product_input}'."
            return result
    else:
        unique_names = initial_matches_df['Stm_SalesDesc_V'].unique()
        if len(unique_names) == 1:
            selected_product_for_display = unique_names[0]
            product_name_for_filtering = unique_names[0]
            escaped_product_for_filtering = re.escape(product_name_for_filtering)
        else:
            result["message"] = f"Multiple matches for '{product_input}', aggregating."
            escaped_product_for_filtering = escaped_product_input

    if not pd.api.types.is_datetime64_any_dtype(df['ReportDate']):
        df['ReportDate'] = pd.to_datetime(df['ReportDate'])
    latest_date = df['ReportDate'].max()
    lookback_start_date = latest_date - pd.Timedelta(days=avg_consumption_days - 1)
    product_df = df[
        (df['Stm_SalesDesc_V'].str.contains(escaped_product_for_filtering, case=False, na=False)) &
        (df['ReportDate'] >= lookback_start_date) &
        (df['ReportDate'] <= latest_date)
    ].copy()

    if product_df.empty:
        result["message"] = f"No data found for '{selected_product_for_display}' in the last {avg_consumption_days} days."
        return result

    daily_stock_summary = product_df.groupby('ReportDate')['Stk_Stock_N'].sum().sort_index()
    raw_consumption = -daily_stock_summary.diff().dropna().sum()
    consumption = max(raw_consumption, 0)
    num_active_days = daily_stock_summary.shape[0]
    average_daily_consumption = consumption / num_active_days if num_active_days > 0 and consumption > 0 else 0

    current_stock_df = df[
        (df['Stm_SalesDesc_V'].str.contains(escaped_product_for_filtering, case=False, na=False)) & 
        (df['ReportDate'] == latest_date)
    ]
    if current_stock_df.empty:
        result["message"] = f"No current stock data for '{selected_product_for_display}' on {latest_date.strftime('%Y-%m-%d')}."
        return result

    current_stock = current_stock_df['Stk_Stock_N'].sum()
    if average_daily_consumption > 0:
        days_of_supply = current_stock / average_daily_consumption
    else:
        days_of_supply = None

    result.update({
        "selected_product": selected_product_for_display,
        "current_stock": current_stock,
        "average_daily_consumption": average_daily_consumption,
        "days_of_supply": days_of_supply,
        "daily_stock_summary": daily_stock_summary
    })

    return result

@st.cache_data
def load_data():
    df = pd.read_parquet("stock_daily_cleaned.parquet")
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
        "Avg Consumption/Supply Days"
    ]
    page = st.sidebar.radio(
        " ",
        nav_options,
        key="main_nav"
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
    elif page == "Avg Consumption/Supply Days":
        st.subheader("Average Consumption & Days of Supply")
        product_input = st.text_input("Enter product name")
        num_days = st.number_input("Number of days", min_value=1, value=30)
        if st.button("Calculate") and product_input:
            result = calculate_supply_days(df, product_input, num_days)
            if result["message"]:
                st.error(result["message"])
            else:
                st.write(f"Selected product: {result['selected_product']}")
                st.write(f"Current stock: {result['current_stock']}")
                st.write(f"Average daily consumption: {result['average_daily_consumption']}")
                if result["days_of_supply"] is not None:
                    st.success(f"Days of supply: {result['days_of_supply']:.2f}")
                if result["daily_stock_summary"] is not None:
                    st.line_chart(result["daily_stock_summary"])

    

    


if __name__ == '__main__':
    main()
