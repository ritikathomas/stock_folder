import streamlit as st
import pandas as pd


def show_category_chart(df):
    st.subheader("Category Analysis")
    
    category_options = ["Manufacturing Companies", "Products", "Unit Types", "Categories", "Warehouse/Storage"]
    selected_category = st.selectbox("Select Category", options=category_options, key='category_filter')

    # Map selections to column names
    column_mapping = {
        "Manufacturing Companies": "Mfg_Name_V",
        "Products": "Stm_SalesDesc_V",
        "Unit Types": "Unh_Code_V",
        "Categories": "Ctg_Desc_V",
        "Warehouse/Storage": "Shm_Name_V"  # Changed to existing warehouse name field
    }

    column_name = column_mapping[selected_category]
    unique_values = df[column_name].unique().tolist()


    # Use a multi-select as the primary filter for all category types
    multi_select_items = st.multiselect(
        f"Select {selected_category}",
        options=unique_values,
        key='main_multi_select_box'
    )

    selected_item = None

    # Prepare DataFrame based on multi-select filter(s)
    filtered_df = df.copy()
    if multi_select_items:
        filtered_df = filtered_df[filtered_df[column_name].isin(multi_select_items)]

    # Tabs for Summary, Trends, Table
    tab1, tab2, tab3 = st.tabs(["Summary", "Trends", "Table"])
    with tab1:
        st.write(f"**Total {selected_category}:** {filtered_df[column_name].nunique()}")
        st.write(f"**Total Stock Shown:** {filtered_df['Stk_Stock_N'].sum():,.2f}")
    with tab2:
        # Aggregated view by ReportDate
        st.subheader(f"{selected_category} Trends Over Time")
        if not filtered_df.empty and 'ReportDate' in filtered_df:
            trend = filtered_df.groupby('ReportDate')['Stk_Stock_N'].sum()
            st.line_chart(trend)
        else:
            st.info("No data to display in selected range or filters.")
    with tab3:
        st.subheader(f"Filtered Data Table")
        st.dataframe(filtered_df, use_container_width=True)

    # Optionally show quick insights for single selected item
    if selected_item is not None:
        st.success(f"Data for {selected_item}")
        item_df = df[df[column_name] == selected_item]
        st.write(f"**Total Stock:** {item_df['Stk_Stock_N'].sum():,.2f}")

    st.divider()
