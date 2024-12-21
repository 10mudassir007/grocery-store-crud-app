import streamlit as st

if 'loggedIn' not in st.session_state:
    st.session_state.loggedIn = False
if 'password_input' not in st.session_state:
    st.session_state.password_input = ""

def login():
    if st.session_state.password_input == "252462":
        st.session_state.loggedIn = True
    else:
        st.session_state.loggedIn = False
        st.error("Incorrect Password")

def logout():
    st.session_state.loggedIn = False

st.title("Grocery Store App")

if not st.session_state.loggedIn:
    st.header("Login as Admin")
    st.text_input(
        "Password", 
        placeholder="Enter Password", 
        type="password", 
        key="password_input"
    )
    st.button("Login", on_click=login)

if st.session_state.loggedIn:
    st.header("Logged in as Admin")
    with st.sidebar:
        st.button("Logout", on_click=logout)
        st.subheader("CRUD Operations")
        if st.button("Create"):
            st.write("Create operation coming soon...")
        if st.button("Read"):
            st.write("Read operation coming soon...")
        if st.button("Update"):
            st.write("Update operation coming soon...")
        if st.button("Delete"):
            st.write("Delete operation coming soon...")
