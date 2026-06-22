from turtle import st


elif page.startswith("Out-of-Stock"):
    st.subheader("Out-of-Stock Items")
    if not out_of_stock.empty:
        st.dataframe(out_of_stock, use_container_width=True)
    else:
        st.info("No items are currently out of stock.")