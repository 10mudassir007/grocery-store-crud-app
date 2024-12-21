import streamlit as st 
import sqlite3

if 'op' not in st.session_state:
    st.session_state.op = None


c1,c2,c3 = st.columns(3)
with c1:
    if st.button("Add new customer"):
        st.session_state.op = 'customer'
        st.rerun()
with c2:
    if st.button("Add new product"):
        st.session_state.op = 'product'
        st.rerun()
with c3:
    if st.button("Add new order"):
        st.session_state.op = 'order'
        st.rerun()

conn = sqlite3.connect('grocery_store1.db')
cursor = conn.cursor()

if st.session_state.op == 'customer':
elif st.session_state.op == 'product':
elif st.session_state.op == 'order':
