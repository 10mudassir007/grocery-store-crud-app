import streamlit as st 
import sqlite3
import time

if 'op' not in st.session_state:
    st.session_state.op = None


c1,c2,c3 = st.columns(3)
with c1:
    if st.button("Delete customers"):
        st.session_state.op = 'customer'
        st.rerun()
with c2:
    if st.button("Delete product"):
        st.session_state.op = 'product'
        st.rerun()
with c3:
    if st.button("Delete orders"):
        st.session_state.op = 'order'
        st.rerun()

conn = sqlite3.connect('grocery_store1.db')
cursor = conn.cursor()

if st.session_state.op == 'customer':
    cust_name = st.text_input("Enter Customer Name", placeholder="Enter customer name to delete")

    if st.button("Delete Customer"):
        if cust_name:
            cursor.execute("SELECT customer_id FROM customers WHERE name = ?", (cust_name,))
            customer = cursor.fetchone()

            if customer:
                customer_id = customer[0]

                # Delete the orders associated with the customer
                cursor.execute("DELETE FROM orders WHERE customer_id = ?", (customer_id,))
                conn.commit()

                # Delete the order items associated with those orders
                cursor.execute("DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE customer_id = ?)", (customer_id,))
                conn.commit()

                # Delete the customer
                cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))
                conn.commit()

                st.success(f"Customer '{cust_name}' and their related orders and order items deleted successfully!")
            else:
                st.error(f"Customer '{cust_name}' not found!")
        else:
            st.warning("Please enter a customer name.")


elif st.session_state.op == 'order':   
    cust_name = st.text_input("Enter Customer Name", placeholder="Enter existing customer name")
    order_date = st.text_input("Enter Order Date", placeholder="Enter order date (YYYY-MM-DD)")

    if st.button("Delete Order"):
        if cust_name and order_date:
            cursor.execute("SELECT customer_id FROM customers WHERE name = ?", (cust_name,))
            customer = cursor.fetchone()

            if customer:
                customer_id = customer[0]
                cursor.execute("SELECT order_id FROM orders WHERE customer_id = ? AND order_date = ?", (customer_id, order_date))
                order = cursor.fetchone()

                if order:
                    order_id = order[0]
                    cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
                    conn.commit()
                    cursor.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
                    conn.commit()
                    st.success(f"Order on '{order_date}' for customer '{cust_name}' deleted successfully!")
                else:
                    st.error(f"Order on '{order_date}' not found for customer '{cust_name}'.")
            else:
                st.error(f"Customer '{cust_name}' not found!")
        else:
            st.warning("Please enter both customer name and order date.")

conn.close()