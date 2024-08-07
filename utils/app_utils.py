# app_utils.py
import streamlit as st

def initialize_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

def display_uploaded_data(df, table_name):
    st.subheader(f"Uploaded Data - {table_name}")
    st.dataframe(df.head(3))

def display_query_results(result_df, fig):
    st.subheader("Query Result")
    st.dataframe(result_df)
    st.plotly_chart(fig)

def display_chat_history():
    for i, (q, sql, chart) in enumerate(st.session_state['chat_history']):
        st.sidebar.write(f"**Query {i+1}:** {q}")
        st.sidebar.plotly_chart(chart)
