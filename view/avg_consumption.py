import difflib
import pandas as pd
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