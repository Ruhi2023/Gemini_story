import streamlit as st 
nav = st.navigation([
    st.Page("pages/app4.py",title = "Home",icon="🏠"),
    st.Page("pages/Stories_page.py", title ="View Story",icon="📖"),
]) 
nav.run()