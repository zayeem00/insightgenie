# db_utils.py
import pandas as pd
import openai
import sqlite3
import streamlit as st

def create_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn, df, table_name):
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def upload_data(file, table_name, db_name, openai_key):
    conn = create_connection(db_name)
    openai.api_key = openai_key
    
    try:
        df = pd.read_csv(file)
    except pd.errors.ParserError as e:
        st.error(f"Error parsing CSV file: {e}")
        return None
    
    create_table(conn, df, table_name)
    
    st.sidebar.success(f"Data uploaded and stored in the {table_name} table successfully.")
    return df

def process_query(query, db_name):
    conn = create_connection(db_name)
    
    # Get columns from the database
    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table'", conn)
    table_names = tables['name'].tolist()
    
    columns = {}
    for table in table_names:
        df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 1", conn)
        columns[table] = df.columns.tolist()
    
    column_info = ' '.join([f"Table {table}: {', '.join(cols)}." for table, cols in columns.items()])

    example_queries = """
    Example queries and their corresponding SQL queries:
    \n1. User query: 'Show me the total sales by date'\n   SQL query: SELECT SaleDate, SUM(TotalPrice) as total_sales FROM sales_data GROUP BY SaleDate;
    \n2. User query: 'Which product has the maximum sales by quantity?'\nSQL query: SELECT ProductName, SUM(Quantity) as total_quantity FROM sales_data INNER JOIN products_data ON sales_data.ProductID = products_data.ProductID GROUP BY ProductName ORDER BY total_quantity DESC LIMIT 1;
    \n3. User query: 'Show a scatter plot of sales vs. quantity'\n SQL query: SELECT SaleDate, Quantity FROM sales_data;
    \n4. User query: 'Show a pie chart of sales distribution by product category'\n SQL query: SELECT Category, SUM(TotalPrice) as total_sales FROM sales_data INNER JOIN products_data ON sales_data.ProductID = products_data.ProductID GROUP BY Category;
    \n5. User query: 'Show the average age of customers by region'\nSQL query: SELECT Region, AVG(Age) as avg_age FROM customers_data GROUP BY Region;
    """

    messages = [
        {"role": "system", "content": f"You are a specialized assistant for converting natural language queries to SQL queries. {column_info}.{example_queries}"},
        {"role": "user", "content": f"Convert this query to a SQL query: {query}. Just respond with the SQL query and nothing else."}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=150
    )
    
    sql_query = response.choices[0].message['content'].strip()
    
    try:
        result_df = pd.read_sql_query(sql_query, conn)
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None, None
    
    if result_df.empty:
        st.warning("No data found for the given query.")
        return None, None
    
    # Determine the type of visualization
    visualization_type = determine_visualization_type(query)
    
    # Generate a visualization based on the determined type
    return result_df, visualization_type, sql_query
