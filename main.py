import streamlit as st

if 'loggedIn' not in st.session_state:
    st.session_state.loggedIn = False
if 'password_input' not in st.session_state:
    st.session_state.password_input = ""
if 'password' not in st.session_state:
    st.session_state.password = "252462"

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
        if st.session_state.password_input == st.session_state.password:
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

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("Log Out"):
            st.session_state.loggedIn = False
            st.rerun()

    with col2:
        if st.button("Change Password"):
            new_pass = st.sidebar.text_input("Enter new password", type="password")
        
        # Place the 'Confirm' button below the password field in the sidebar
            if st.sidebar.button("Confirm"):
                st.session_state.password = new_pass
                st.sidebar.success("Password changed successfully!")
st.sidebar.markdown('---')
st.sidebar.text("Made by Mudassir Junejo")
