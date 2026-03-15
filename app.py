import streamlit as st
import pandas as pd

from src.validator import validate_data, filter_valid_records
from src.transformer import transform_data


st.title("SaaS Billing Data Migration Tool")
st.write("Upload a billing CSV file to validate, transform, and preview the data.")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

    errors, invalid_indices = validate_data(df)

    if errors:
        st.subheader("Validation Issues")
        for e in errors:
            st.warning(e)

        valid_df, rejected_df = filter_valid_records(df, invalid_indices)

        col1, col2 = st.columns(2)
        col1.metric("Valid Records", len(valid_df))
        col2.metric("Rejected Records", len(rejected_df))

        if not rejected_df.empty:
            st.subheader("Rejected Records")
            st.dataframe(rejected_df, use_container_width=True)
    else:
        st.success("No validation errors found")
        valid_df = df

    if not valid_df.empty:
        records = transform_data(valid_df)

        st.subheader("Transformed Data (API Format)")
        st.json(records)
    else:
        st.error("No valid records to transform.")
