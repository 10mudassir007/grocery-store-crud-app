import streamlit as st

if 'loggedIn' not in st.session_state:
    st.session_state.loggedIn = False
if 'password_input' not in st.session_state:
    st.session_state.password_input = ""

st.title("Grocery Store App")

if not st.session_state.loggedIn:
    st.header("Login as Admin")
    st.text_input(
        "Password", 
        placeholder="Enter Password", 
        type="password", 
        key="password_input"
    )
    login_button = st.button("Login")

    if login_button:
        if st.session_state.password_input == "252462":
            st.session_state.loggedIn = True
            st.rerun()
        else:
            st.error("Incorrect Password")

if st.session_state.loggedIn:
    st.header("Logged in as Admin")
    st.markdown("##### Select operation from sidebar")
    create = st.Page(
        page='create.py',
        title="Add new Data",
        icon=":material/account_circle:"
    )
    read = st.Page(
        page='read.py',
        title="View Data",
        icon=":material/account_circle:"
    )
    update = st.Page(
        page='update.py',
        title="Update Data",
        icon=":material/account_circle:"
    )
    delete = st.Page(
        page='delete.py',
        title="Delete Data",
        icon=":material/account_circle:"
    )
    pg = st.navigation({"Operations":[create, read, update, delete]})
    pg.run()
st.sidebar.text("Made by Mudassir Junejo")