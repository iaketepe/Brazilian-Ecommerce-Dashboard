

import streamlit as st

st.title("Brazilian-Ecommerce-Dashboard")

with st.sidebar:

    st.title("SideBar")
    st.button("<Year>")
    col1, col2, col3 = st.columns(3)

    options = ["A","B","C"]
    st.segmented_control(
        "Options", options,
        selection_mode="single",
    )
