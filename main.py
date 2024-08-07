# main.py
import streamlit as st
from utils.db_utils import upload_data, process_query
from utils.visualization_utils import determine_visualization_type
from utils.app_utils import initialize_session_state, display_uploaded_data, display_query_results, display_chat_history

# Streamlit app configuration
st.set_page_config(page_title="InsightGenie", page_icon=":crystal_ball:", layout="wide")

st.title("InsightGenie :crystal_ball:")
st.write("""
Welcome to InsightGenie! Your go-to tool for generating insightful visualizations from your data. 
Simply upload your data, ask questions, and let InsightGenie do the rest.
""")

# Upload section
st.sidebar.header("Upload Data and API Keys")
uploaded_files = st.sidebar.file_uploader("Choose CSV files", type="csv", accept_multiple_files=True)
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
db_name = 'New_Sales_data.db'

initialize_session_state()

dataframes = []
if uploaded_files and openai_api_key:
    for file in uploaded_files:
        table_name = file.name.split('.')[0]
        df = upload_data(file, table_name, db_name, openai_api_key)
        if df is not None:
            dataframes.append(df)
            display_uploaded_data(df, table_name)

# Query section
st.header("Ask a Question")
query = st.text_input("Enter your query:")
if st.button("Submit Query"):
    if query and openai_api_key:
        result_df, fig, sql_query = process_query(query, db_name)
        if result_df is not None and fig is not None:
            display_query_results(result_df, fig)
            st.session_state['chat_history'].append((query, sql_query, fig))

# Display chat history
if st.session_state['chat_history']:
    st.sidebar.header("Chat History")
    display_chat_history()

# footer
st.markdown("""
    <style>
    footer {visibility: hidden;}
    .css-1q8dd3e {background-color: #fafafa; padding: 10px;}
    .stSidebar {width: 300px;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
    <div style='text-align: center;'>
        <h4>InsightGenie</h4>
        <p>Your data. Your insights. Simplified.</p>
    </div>
""", unsafe_allow_html=True)
