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
    name = st.text_input("Name",placeholder="Enter customer's name")
    phone = st.text_input("Phone number",placeholder="Enter customer's phone number")
    city = st.text_input("City",placeholder="Enter customer's city")
    if st.button("Add"):
        if name and phone and city:
            cursor.execute("""INSERT INTO customers (name, phone, address) VALUES ("{}","{}","{}");""".format(name,phone,city))
            conn.commit()
            st.success("Customer added successfully")
            st.session_state.op = None
            st.rerun()
elif st.session_state.op == 'product':
    name = st.text_input("Name",placeholder="Enter product's name")
    cat = st.text_input("Category",placeholder="Enter product's category")
    price = st.text_input("Price",placeholder="Enter product's price")
    quantity = st.text_input("Quantity",placeholder="Enter product's quantity")
    if st.button("Add"):
        if name and cat and price and quantity:
            cursor.execute("""INSERT INTO products (name, category, price, stock_quantity) VALUES ('{}', '{}', {}, {});""".format(name,cat,float(price),int(quantity)))
            conn.commit()
            st.success("Product added successfully")
            st.session_state.op = None
            st.rerun()
elif st.session_state.op == 'order':
    customer_name = st.text_input("Customer Name", placeholder="Enter customer's name")
    dt = st.text_input("Order Date", placeholder="Enter order date")
    t_amount = st.text_input("Total Amount", placeholder="Enter total amount")
    status = st.text_input("Order Status", placeholder="Enter order status")

    # Fetch products for the order
    cursor.execute("SELECT product_id, name, price FROM products")
    products = cursor.fetchall()

    # Map product names to product IDs (product_options will be a dictionary)
    product_options = {product[1]: product[0] for product in products}
    
    # Display products as multiselect (product names as options)
    selected_products = st.multiselect("Select Products", options=list(product_options.keys()))

    # Dictionary to hold product quantities
    product_quantities = {}
    for product in selected_products:
        qty = st.number_input(f"Quantity for {product}", min_value=1, step=1)
        if qty > 0:
            product_quantities[product] = qty  # Store product and quantity in the dictionary

    if st.button("Add Order"):
        if customer_name and dt and t_amount and status and selected_products:
            # Get customer_id from customer name
            cursor.execute("SELECT customer_id FROM customers WHERE name = ?", (customer_name,))
            result = cursor.fetchone()

            if result:
                customer_id = result[0]

                # Insert into orders table
                cursor.execute("""
                INSERT INTO orders (customer_id, order_date, total_amount, status)
                VALUES (?, ?, ?, ?)
                """, (customer_id, dt, float(t_amount), status))
                order_id = cursor.lastrowid  # Get the last inserted order ID

                # Insert order items into the order_items table
                for product_name, quantity in product_quantities.items():
                    # Get product_id from the product name
                    product_id = product_options[product_name]
                    
                    # Get the product price (retrieved from previously fetched products list)
                    product_price = next(p[2] for p in products if p[0] == product_id)  # Fetch price by matching product_id

                    # Insert into order_items table
                    cursor.execute("""
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                    """, (order_id, product_id, quantity, product_price))

                conn.commit()
                st.success("Order and items added successfully!")
            else:
                st.error("Customer not found!")

            st.session_state.op = None
            st.rerun()

conn.close()