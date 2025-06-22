import streamlit as st
import pandas as pd

st.title('Fresh Produce Analysis')

uploaded_file = st.file_uploader('Select a CSV file', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    try:
        df = pd.read_csv('data/processed/analysis_summary.csv')
        st.info('Showing default file: analysis_summary.csv')
    except FileNotFoundError:
        st.warning("No file uploaded and default file 'analysis_summary.csv' not found.")
        df = None

if df is not None:
    st.write(df)
