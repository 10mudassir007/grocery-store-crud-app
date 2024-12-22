import streamlit as st 
import sqlite3
import time

if 'op' not in st.session_state:
    st.session_state.op = None


c1,c2,c3 = st.columns(3)
with c1:
    if st.button("Update customers"):
        st.session_state.op = 'customer'
        st.rerun()
with c2:
    if st.button("Update product"):
        st.session_state.op = 'product'
        st.rerun()
with c3:
    if st.button("Update orders"):
        st.session_state.op = 'order'
        st.rerun()

conn = sqlite3.connect('grocery_store.db')
cursor = conn.cursor()

if st.session_state.op == 'customer':
    st.subheader("Update Customer Information")
    
    cust_name = st.text_input("Customer Name", placeholder="Enter existing customer name to update")
    
    if cust_name:
        cursor.execute("SELECT * FROM customers WHERE name = ?", (cust_name,))
        customer = cursor.fetchone()
        
        if customer:
            st.success(f"Customer '{cust_name}' found!")
            
            update_choice = st.selectbox("What do you want to update?", ["Phone Number", "City"])
            
            if update_choice == "Phone Number":
                new_phone = st.text_input("New Phone Number", placeholder="Enter new phone number")
                if st.button("Update Phone"):
                    if new_phone:
                        cursor.execute("UPDATE customers SET phone = ? WHERE name = ?", (new_phone, cust_name))
                        conn.commit()
                        st.session_state.op = None
                        st.success(f"Phone number for '{cust_name}' updated successfully!")
                        st.rerun() 
                    else:
                        st.warning("Please enter a new phone number.")
            
            elif update_choice == "City":
                new_city = st.text_input("New City", placeholder="Enter new city")
                if st.button("Update City"):
                    if new_city:
                        cursor.execute("UPDATE customers SET address = ? WHERE name = ?", (new_city, cust_name))
                        conn.commit()
                        st.session_state.op = None
                        st.success(f"City for '{cust_name}' updated successfully!")
                        time.sleep(3)
                        st.rerun()  
                    else:
                        st.warning("Please enter a new city.")
        else:
            st.error(f"Customer '{cust_name}' not found!")

    
elif st.session_state.op == 'product':
    st.subheader("Update Product Information")
    
    prod_name = st.text_input("Product Name", placeholder="Enter product name to update")
    
    if prod_name:
        cursor.execute("SELECT * FROM products WHERE name = ?", (prod_name,))
        product = cursor.fetchone()
        
        if product:
            st.success(f"Product '{prod_name}' found!")
            
            update_choice = st.selectbox("What do you want to update?", ["Category", "Price", "Stock Quantity"])
            
            if update_choice == "Category":
                new_category = st.text_input("New Category", placeholder="Enter new category")
                if st.button("Update Category"):
                    if new_category:
                        cursor.execute("UPDATE products SET category = ? WHERE name = ?", (new_category, prod_name))
                        conn.commit()
                        st.session_state.op = None
                        st.success(f"Category for '{prod_name}' updated successfully!")
                        time.sleep(3)
                        st.rerun()  
                    else:
                        st.warning("Please enter a new category.")
            
            elif update_choice == "Price":
                new_price = st.text_input("New Price", placeholder="Enter new price")
                if st.button("Update Price"):
                    if new_price:
                        try:
                            cursor.execute("UPDATE products SET price = ? WHERE name = ?", (float(new_price), prod_name))
                            conn.commit()
                            st.session_state.op = None
                            st.success(f"Price for '{prod_name}' updated successfully!")
                            time.sleep(3)
                            st.rerun()  
                        except ValueError:
                            st.warning("Please enter a valid price.")
                    else:
                        st.warning("Please enter a new price.")
            
            elif update_choice == "Stock Quantity":
                new_stock = st.text_input("New Stock Quantity", placeholder="Enter new stock quantity")
                if st.button("Update Stock Quantity"):
                    if new_stock:
                        try:
                            cursor.execute("UPDATE products SET stock_quantity = ? WHERE name = ?", (int(new_stock), prod_name))
                            conn.commit()
                            st.session_state.op = None
                            st.success(f"Stock quantity for '{prod_name}' updated successfully!")
                            time.sleep(3)
                            st.rerun() 
                        except ValueError:
                            st.warning("Please enter a valid quantity.")
                    else:
                        st.warning("Please enter a new stock quantity.")
        else:
            st.error(f"Product '{prod_name}' not found!")

elif st.session_state.op == 'order':
    cust_name = st.text_input("Customer Name", placeholder="Enter customer name")
    order_date = st.text_input("Order Date", placeholder="Enter order date (YYYY-MM-DD)")
     
    if cust_name and order_date:
        cursor.execute("""
            SELECT orders.order_id, orders.order_date, orders.total_amount, orders.status
            FROM orders
            INNER JOIN customers ON orders.customer_id = customers.customer_id
            WHERE customers.name = ? AND orders.order_date = ?
        """, (cust_name, order_date))
        matching_orders = cursor.fetchall()

        if not matching_orders:
            st.error("No orders found for the given customer and date!")
        else:
            st.subheader("Matching Orders")
            for order in matching_orders:
                st.write(f"Order ID: {order[0]}, Date: {order[1]}, Total: {order[2]}, Status: {order[3]}")

            order_id = st.selectbox(
                "Select the Order ID to update", [order[0] for order in matching_orders]
            )

            new_status = st.selectbox("Order Status", ["Pending", "Completed"])
            new_total = st.text_input("New Total Amount", placeholder="Enter new total amount")

            if st.button("Update Order"):
                if order_id and new_total:
                    cursor.execute("""
                        UPDATE orders
                        SET status = ?, total_amount = ?
                        WHERE order_id = ?
                    """, (new_status, float(new_total), order_id))
                    conn.commit()
                    st.success("Order updated successfully!")
                    time.sleep(3)
                else:
                    st.error("Please select an order and provide the new total amount!")
    else:
        st.info("Please enter both customer name and order date to fetch orders.")
 
