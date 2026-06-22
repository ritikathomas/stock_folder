import streamlit as st
import pandas as pd


def show_search_product_id(df):
    """General multi-field search and display product details"""
    st.subheader("Search")
    search_term = st.text_input("Enter search term:")

    if search_term:
        with st.spinner("Searching, please wait..."):
            df_str = df.astype(str)
            mask = pd.DataFrame(False, index=df_str.index, columns=df_str.columns)
            for col in df_str.columns:
                mask[col] = df_str[col].str.contains(search_term, case=False, na=False)
            matches = df[mask.any(axis=1)]
            if not matches.empty:
                st.success(f"Found {len(matches)} result(s) matching: '{search_term}'")
                st.dataframe(matches, use_container_width=True)
            else:
                st.error(f"No matching results found for: '{search_term}'")
    st.divider()
    

    