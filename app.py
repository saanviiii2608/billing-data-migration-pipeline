import streamlit as st
import pandas as pd

from src.validator import validate_data
from src.transformer import transform_data


st.title("SaaS Billing Data Migration Tool")

st.write("Upload a billing CSV file to validate and transform the data.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df)

    errors = validate_data(df)

    if errors:

        st.subheader("Validation Issues")

        for e in errors:
            st.warning(e)

    else:
        st.success("No validation errors found")

    records = transform_data(df)

    st.subheader("Transformed Data (API Format)")

    st.json(records[:2])