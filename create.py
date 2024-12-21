import streamlit as st 
import sqlite3

if 'op' not in st.session_state:
    st.session_state.op = None
if 'success' not in st.session_state:
    st.session_state.success = None

c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Add new customer"):
        st.session_state.op = 'customer'
        st.session_state.success = None
        st.rerun()
with c2:
    if st.button("Add new product"):
        st.session_state.op = 'product'
        st.session_state.success = None
        st.rerun()
with c3:
    if st.button("Add new order"):
        st.session_state.op = 'order'
        st.session_state.success = None
        st.rerun()

conn = sqlite3.connect('grocery_store1.db')
cursor = conn.cursor()

if st.session_state.op == 'customer':
    name = st.text_input("Name", placeholder="Enter customer's name")
    phone = st.text_input("Phone number", placeholder="Enter customer's phone number")
    city = st.text_input("City", placeholder="Enter customer's city")
    if st.button("Add"):
        if name and phone and city:
            cursor.execute("""INSERT INTO customers (name, phone, address) VALUES ("{}","{}","{}");""".format(name, phone, city))
            conn.commit()
            st.session_state.success = "Customer added successfully!"
            st.session_state.op = None

elif st.session_state.op == 'product':
    name = st.text_input("Name", placeholder="Enter product's name")
    cat = st.text_input("Category", placeholder="Enter product's category")
    price = st.text_input("Price", placeholder="Enter product's price")
    quantity = st.text_input("Quantity", placeholder="Enter product's quantity")
    if st.button("Add"):
        if name and cat and price and quantity:
            cursor.execute("""INSERT INTO products (name, category, price, stock_quantity) VALUES ('{}', '{}', {}, {});""".format(name, cat, float(price), int(quantity)))
            conn.commit()
            st.session_state.success = "Product added successfully!"
            st.session_state.op = None

elif st.session_state.op == 'order':
    customer_name = st.text_input("Customer Name", placeholder="Enter customer's name")
    dt = st.text_input("Order Date(YYYY-MM-DD)", placeholder="Enter order date")
    status = st.selectbox("Order Status", options=["Pending", "Completed"])
    
    cursor.execute("SELECT product_id, name, price FROM products")
    products = cursor.fetchall()

    product_options = {product[1]: product[0] for product in products}
    selected_products = st.multiselect("Select Products", options=list(product_options.keys()))

    product_quantities = {}
    total_amount = 0.0 
    for product in selected_products:
        qty = st.number_input(f"Quantity for {product}", min_value=1, step=1)
        if qty > 0:
            product_quantities[product] = qty 
            product_price = next(p[2] for p in products if p[1] == product)
            total_amount += product_price * qty  

    if st.button("Add Order"):
        if customer_name and dt and status and selected_products:
            cursor.execute("SELECT customer_id FROM customers WHERE name = ?", (customer_name,))
            result = cursor.fetchone()

            if result:
                customer_id = result[0]

                cursor.execute("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (?, ?, ?, ?)
                """, (customer_id, dt, total_amount, status))
                order_id = cursor.lastrowid

                for product_name, quantity in product_quantities.items():
                    product_id = product_options[product_name]
                    product_price = next(p[2] for p in products if p[1] == product_name)

                    cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                    """, (order_id, product_id, quantity, product_price))

                conn.commit()
                st.session_state.success = "Order and items added successfully!"
                st.session_state.op = None
            else:
                st.error("Customer not found!")

if st.session_state.success:
    st.success(st.session_state.success)

conn.close()
