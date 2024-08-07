# InsightGenie :crystal_ball:

## Overview
InsightGenie is an AI-based natural language to visualization tool designed to improve employee productivity by allowing users to generate insightful visualizations from their data with ease. Users can upload multiple data files, input natural language queries, and InsightGenie will convert these queries into SQL queries, fetch data from the appropriate tables, and generate visualizations based on the query and fetched data.

## Features
- Upload multiple CSV files and store them in SQLite database.
- Natural language to SQL query translation using OpenAI GPT-4.
- Automatic determination of the best type of visualization for the query.
- Visualizations including Histogram, Scatter Plot, Line Chart, Bar Chart, Pie Chart, Heat Map, and Map.
- Session-based chat history for query and response tracking.

## Installation
   Clone the repository:
   
   git clone https://github.com/your-username/insightgenie.git

   cd insightgenie

## Install the required dependencies:
   pip install -r requirements.txt

## Run the Streamlit application:
   streamlit run main.py

## Usage

- Upload your CSV data files using the sidebar file uploader.
- Enter your OpenAI API Key in the sidebar.
- Ask a question in the natural language query input box.
- Submit the query and view the generated insights and visualizations.
- Review your chat history on the sidebar.

## File Structure

- main.py: Main application file for the Streamlit interface.
- utils/: Directory containing utility modules for database operations, visualization handling, and application specific utilities.
- db_utils.py: Functions for database operations.
- visualization_utils.py: Functions for determining and generating visualizations.
- app_utils.py: Helper functions for initializing session state and displaying data in the Streamlit app.

## License

This project is licensed under the MIT License.
