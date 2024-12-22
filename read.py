import pandas as pd
import streamlit as st 
import sqlite3


if 'op' not in st.session_state:
    st.session_state.op = None


c1,c2,c3 = st.columns(3)
with c1:
    if st.button("View all customers"):
        st.session_state.op = 'customer'
        st.rerun()
with c2:
    if st.button("View all product"):
        st.session_state.op = 'product'
        st.rerun()
with c3:
    if st.button("View all orders"):
        st.session_state.op = 'order'
        st.rerun()

conn = sqlite3.connect('grocery_store.db')
cursor = conn.cursor()

if st.session_state.op == 'customer':
    query = """SELECT * FROM customers"""
    df = pd.read_sql_query(query, conn)
    st.subheader("Customers")
    st.dataframe(df,width=1000)

elif st.session_state.op == 'product':
    query = """SELECT * FROM products"""
    df = pd.read_sql_query(query, conn)
    st.subheader("Products")
    st.dataframe(df,width=1000)

elif st.session_state.op == 'order':
    query = """ SELECT orders.order_id, customers.name AS customer_name, orders.order_date, 
           orders.total_amount, orders.status
    FROM orders
    INNER JOIN customers ON orders.customer_id = customers.customer_id"""
    df = pd.read_sql_query(query, conn)
    st.subheader("Orders")
    st.dataframe(df,width=1000)