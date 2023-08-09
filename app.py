import pandas as pd
import streamlit as st
import plotly_express as px
from numerize.numerize import numerize
import plotly.graph_objects as go


st.set_page_config(page_title="Sales Dashboard", layout='wide', initial_sidebar_state='collapsed')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

@st.cache
def get_data():
    df = pd.read_csv('data/sales.csv')
    df['Year'] = pd.to_datetime(df['Invoice Date']).dt.year
    df['Month'] = pd.to_datetime(df['Invoice Date']).dt.month_name(locale='English')


    return df
df = get_data()

header_left, header_mid, header_right = st.columns([1,2,1],gap='large')
with header_mid:
    st.markdown("## ECOMMERCE DASHBOARD")

with header_left:
    st.image('images/ICON3.png',use_column_width='Auto')

with st.sidebar:
    Year_filter = st.multiselect(label='Select Year',
                                options=df['Year'].unique(),
                                default=df['Year'].unique())

    Marketplace_filter = st.multiselect(label="Select MarketPlace",
                                options=df["Marketplace"].unique(),
                                default=df["Marketplace"].unique())
    
df1 = df.query('Year == @Year_filter & Marketplace == @Marketplace_filter') 

st.sidebar.markdown('''
---
Created with ❤️ by [Abdul Byahatti](https://instagram.com/excel_funclub/).
''')

Total_Revenue = float(df1['Invoice Amount'].sum())
Total_Customers = round(float(df1['Qty'].count()),0)
Total_Orders = round(float(df1['Qty'].sum()),0)
Avg_Value = round(df1['Invoice Amount'].sum() / df1['Qty'].sum(),0)




# Row A

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image('images/salary.png',use_column_width='Auto')
    st.metric(label="Total Revenue", value=numerize(Total_Revenue,0))
                               
with col2:
    st.image('images/consumer.png',use_column_width='Auto')
    st.metric(label="Total Customers", value=Total_Customers)
with col3:
    st.image('images/add-to-cart.png',use_column_width='Auto')
    st.metric(label="Total Orders", value=Total_Orders)
with col4:
    st.image('images/cost.png',use_column_width='Auto')
    st.metric(label="Average Order Value", value=Avg_Value)

chart1, chart2 = st.columns(2)

with chart1:
    df2 = df1.groupby(by=['Month'])['Invoice Amount'].sum(numeric_only=True).reset_index()
    Amount_by_month = px.area(df2,
    x='Month',
    y={'Invoice Amount':0.5},
    template='simple_white',
    title='<b>Revenue<b>')
    Amount_by_month.update_layout(title={'x' : 0.5},
                            plot_bgcolor = "rgba(0,0,0,0)",
                            xaxis =(dict(showgrid = False)),
                            yaxis =(dict(showgrid = False)),
                            showlegend=False)
    st.plotly_chart(Amount_by_month,use_container_width=True)

with chart2:
    df3 = df1.groupby(by=['Marketplace']).sum()[['Invoice Amount']].reset_index().sort_values(['Invoice Amount'])
    
    markertplace_contrubution = px.bar(df3,
    x={'Invoice Amount':0.5},
    y='Marketplace',
    text_auto=True,
    template='simple_white',
    orientation='h',
    title='<b>Revenue by Source<b>')
    markertplace_contrubution.update_layout(title={'x' : 0.5},
                            plot_bgcolor = "rgba(0,0,0,0)",
                            xaxis =(dict(showgrid = False)),
                            yaxis =(dict(showgrid = False)),
                            showlegend=False)
    st.plotly_chart(markertplace_contrubution,use_container_width=True)



df4 = df1.groupby(by=['Month']).sum()[['Qty']].reset_index()

month_Qty = px.line(df4,
    x='Month',
    y='Qty',
    text='Qty',
    markers=True,
    template='simple_white',
    title='<b>Orders by Month<b>')
month_Qty.update_traces(textposition="top right")
month_Qty.update_layout(title={'x' : 0.5},
                            plot_bgcolor = "rgba(0,0,0,0)",
                            xaxis =(dict(showgrid = False)),
                            yaxis =(dict(showgrid = False)),
                            )
st.plotly_chart(month_Qty,use_container_width=True)


chart4, chart5 = st.columns(2)




with chart4:
    Avg_Order = go.Figure(go.Indicator(
    domain = {'x': [0, 1], 'y': [0, 1]},
    value = Avg_Value,
    mode = "gauge+number",
    title = {'text': "Average Order Value"}))

    st.plotly_chart(Avg_Order,use_container_width=True)

with chart5:
    Marketplace_cont = px.pie(df1,
                              names='Marketplace', 
                              values='Invoice Amount',
                              template='simple_white'              
                            )
    Marketplace_cont.update_traces(textposition='inside', textinfo='percent+label',showlegend=False)
    st.plotly_chart(Marketplace_cont,use_container_width=True)

    # ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
