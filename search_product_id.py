import streamlit as st
import pandas as pd


def show_search_product_id(df):
    """General multi-field search and display product details"""
    st.subheader("Search")
    search_term = st.text_input("Enter search term:")

    if search_term:
        df_str = df.astype(str)
        mask = pd.DataFrame(False, index=df_str.index, columns=df_str.columns)
        for col in df_str.columns:
            mask[col] = df_str[col].str.contains(search_term, case=False, na=False)
        matches = df[mask.any(axis=1)]
        if not matches.empty:
            st.success(f"Found {len(matches)} result(s) matching: '{search_term}'")
            for idx, row in matches.iterrows():
                with st.expander(f"Product ID: {row.get('product_id', idx)}", expanded=False):
                    for col in matches.columns:
                        st.write(f"**{col}:** {row[col]}")
        else:
            st.error(f"No matching results found for: '{search_term}'")
    st.divider()
    

    