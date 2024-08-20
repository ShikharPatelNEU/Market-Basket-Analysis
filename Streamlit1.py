import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

# Set the title of the Streamlit app
st.title("🛒 Market Basket Analysis")

# Load the dataset
data = pd.read_csv('market_basket_dataset.csv')

# Calculate total revenue per row
data['Total_Revenue'] = data['Quantity'] * data['Price']

# Sidebar for filters
st.sidebar.header("Filter Options")
selected_items = st.sidebar.multiselect('Select Item(s)', data['Itemname'].unique())

# Filter data based on sidebar selection
filtered_data = data[data['Itemname'].isin(selected_items)] if selected_items else data

# Toggle button for visualizations
visualization_option = st.sidebar.radio("Choose Visualization", [
    "Item Distribution", 
    "Top 10 Popular Items", 
    "Revenue per Item", 
    "Customer Purchase Behavior", 
    "Correlation Matrix", 
    "Item Co-Purchase Network",
    "Pareto Chart"
])

# Visualization 1: Item Distribution Histogram
if visualization_option == "Item Distribution":
    fig_distribution = px.histogram(filtered_data, x='Itemname', title='Item Distribution')
    st.plotly_chart(fig_distribution)

# Visualization 2: Top 10 Popular Items Bar Chart
elif visualization_option == "Top 10 Popular Items":
    item_popularity = filtered_data.groupby('Itemname')['Quantity'].sum().sort_values(ascending=False)
    top_n = 10
    fig_popularity = go.Figure()
    fig_popularity.add_trace(go.Bar(x=item_popularity.index[:top_n], y=item_popularity.values[:top_n],
                                    text=item_popularity.values[:top_n], textposition='auto',
                                    marker=dict(color='skyblue')))
    fig_popularity.update_layout(title=f'Top {top_n} Most Popular Items',
                                 xaxis_title='Item Name', yaxis_title='Total Quantity Sold')
    st.plotly_chart(fig_popularity)

# Visualization 3: Revenue per Item Bar Chart
elif visualization_option == "Revenue per Item":
    revenue_per_item = filtered_data.groupby('Itemname')['Total_Revenue'].sum().sort_values(ascending=False)
    top_n = 10
    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Bar(x=revenue_per_item.index[:top_n], y=revenue_per_item.values[:top_n],
                                 text=revenue_per_item.values[:top_n], textposition='auto',
                                 marker=dict(color='lightgreen')))
    fig_revenue.update_layout(title=f'Top {top_n} Items by Revenue',
                              xaxis_title='Item Name', yaxis_title='Total Revenue Generated')
    st.plotly_chart(fig_revenue)

# Visualization 4: Sales Over Time Line Chart
# elif visualization_option == "Sales Over Time":
#     # Assuming there is a 'Date' column in the dataset
#     data['Date'] = pd.to_datetime(data['Date'])
#     sales_over_time = filtered_data.groupby('Date')['Total_Revenue'].sum()
#     fig_sales_time = px.line(sales_over_time, x=sales_over_time.index, y=sales_over_time.values, 
#                              title='Total Sales Over Time', labels={'x':'Date', 'y':'Total Revenue'})
#     st.plotly_chart(fig_sales_time)

# Visualization 5: Customer Purchase Behavior Box Plot
elif visualization_option == "Customer Purchase Behavior":
    customer_spending = filtered_data.groupby('CustomerID')['Total_Revenue'].sum()
    fig_customer_spending = px.box(customer_spending, y='Total_Revenue', title='Customer Spending Distribution')
    st.plotly_chart(fig_customer_spending)

# Visualization 6: Correlation Matrix Heatmap
elif visualization_option == "Correlation Matrix":
    corr = filtered_data[['Quantity', 'Price', 'Total_Revenue']].corr()
    fig_corr, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    st.pyplot(fig_corr)

# Visualization 7: Item Co-Purchase Network Graph
elif visualization_option == "Item Co-Purchase Network":
    co_purchases = filtered_data.groupby('BillNo')['Itemname'].apply(list)
    edges = []
    for items in co_purchases:
        edges.extend([(item1, item2) for i, item1 in enumerate(items) for item2 in items[i + 1:]])
    edge_count = Counter(edges)
    G = nx.Graph()
    for edge, count in edge_count.items():
        G.add_edge(edge[0], edge[1], weight=count)
    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, k=0.5, seed=42)
    nx.draw_networkx(G, pos, with_labels=True, node_size=3000, node_color='skyblue', edge_color='gray', font_size=10, ax=ax)
    st.pyplot(fig)

# Visualization 8: Pareto Chart
elif visualization_option == "Pareto Chart":
    revenue_sorted = filtered_data.groupby('Itemname')['Total_Revenue'].sum().sort_values(ascending=False)
    cumulative_percentage = revenue_sorted.cumsum() / revenue_sorted.sum() * 100
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(x=revenue_sorted.index, y=revenue_sorted.values, name='Revenue', marker=dict(color='blue')))
    fig_pareto.add_trace(go.Scatter(x=cumulative_percentage.index, y=cumulative_percentage.values, name='Cumulative %', mode='lines+markers', line=dict(color='red')))
    fig_pareto.update_layout(title='Pareto Chart of Item Revenue', yaxis=dict(title='Revenue'), yaxis2=dict(title='Cumulative %', overlaying='y', side='right'))
    st.plotly_chart(fig_pareto)

# Display the filtered data table below the visualizations
st.write("Filtered Data", filtered_data)
