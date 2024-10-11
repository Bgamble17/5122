import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Data App Assignment, on Oct 7th")

df = pd.read_csv("Superstore_Sales_utf8.csv")
st.dataframe(df)

# This bar chart will not have solid bars--but lines--because the detail data is being graphed independently
st.bar_chart(df, x="Category", y="Sales")

# Now let's do the same graph where we do the aggregation first in Pandas... (this results in a chart with solid bars)
st.dataframe(df.groupby("Category").sum())
# Using as_index=False here preserves the Category as a column.  If we exclude that, Category would become the datafram index and we would need to use x=None to tell bar_chart to use the index
st.bar_chart(df.groupby("Category", as_index=False).sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
# Here we ensure Order_Date is in datetime format, then set is as an index to our dataframe
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)

# Here the Grouper is using our newly set index to group by Month ('M')
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)

# Here the grouped months are the index and automatically used for the x axis
st.line_chart(sales_by_month, y="Sales")

#1 Dropdown for selecting Category 
if 'Category' in df.columns:
    categories = df["Category"].unique()
    selected_category= st.selectbox("Select a Category", categories)

#Filtering the dataframe 
df_category=df[df["Category"]== selected_category]

#2 Multi-select for Sub-category based on selected category(1)
if not df_category.empty:
    sub_categories = df_category["Sub_Category"].unique()
    selected_sub_categories = st.multiselect("Select Sub_Categories", sub_categories, sub_categories)
 
 #Filtering subcategory data 
df_filtered = df_category[df_category["Sub_Category"].isin(selected_sub_categories)]

#3 Line chart of sales for selected items in (2)
if not df_filtered.empty:
     sales_by_month_filtered = df_filtered['Sales'].resample('M').sum()
st.line_chart(sales_by_month_filtered, use_container_width=True)
 
 #4 Calculate metrics: total sales, total profit, and overall profit margin
total_sales = df_filtered['Sales'].sum()
total_profit = df_filtered['Profit'].sum()
                
# Calculate overall profit margin as a percentage
overall_profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
                

#5 Calculate overall average profit margin across all categories with delta option icnluded in metrics
overall_total_profit = df['Profit'].sum()
overall_total_sales = df['Sales'].sum()
overall_average_profit_margin = (overall_total_profit / overall_total_sales * 100) if overall_total_sales > 0 else 0


# Display the metrics
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Overall Profit Margin",
        value=f"{overall_profit_margin:.2f}%",
        delta=f"{overall_profit_margin - overall_average_profit_margin:.2f}%"
)
        