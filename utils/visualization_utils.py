# visualization_utils.py
import openai
import plotly.express as px

def determine_visualization_type(query):
    messages = [
        {"role": "system", "content": "You are an expert in data visualization."},
        {"role": "user", "content": f"Based on the following user query, determine the best type of visualization to represent the data:\nQuery: {query}\nPossible visualizations: Histogram, Scatter Plot, Line Chart, Bar Chart, Pie Chart, Heat Map, Map\nResponse:"}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        max_tokens=20
    )
     
    visualization_type = response.choices[0].message['content'].strip()
    return visualization_type

def generate_visualization(visualization_type, result_df):
    if visualization_type == "Histogram":
        fig = px.histogram(result_df, x=result_df.columns[0])
    elif visualization_type == "Scatter Plot":
        fig = px.scatter(result_df, x=result_df.columns[0], y=result_df.columns[1])
    elif visualization_type == "Line Chart":
        fig = px.line(result_df, x=result_df.columns[0], y=result_df.columns[1])
    elif visualization_type == "Bar Chart":
        fig = px.bar(result_df, x=result_df.columns[0], y=result_df.columns[1])
    elif visualization_type == "Pie Chart":
        fig = px.pie(result_df, names=result_df.columns[0], values=result_df.columns[1])
    elif visualization_type == "Heat Map":
        fig = px.density_heatmap(result_df, x=result_df.columns[0], y=result_df.columns[1])
    elif visualization_type == "Map":
        fig = px.scatter_geo(result_df, lat=result_df.columns[0], lon=result_df.columns[1])
    else:
        fig = px.histogram(result_df, x=result_df.columns[0])  # Default to histogram if type is unclear
    
    return fig
