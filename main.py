import streamlit as st

# Define page navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Mood Analysis", "High Vibrational Food", "Texture Classification"])

# Load the selected page
if page == "Mood Analysis":
    import mood  # Ensure mood.py exists in the same directory
    mood.main()
elif page == "High Vibrational Food":
    import Hlv  # Ensure Hlv.py exists in the same directory
    Hlv.main()
elif page == "Texture Classification":
    import Texture  # Ensure Texture.py exists in the same directory
    Texture.main()

st.sidebar.info("Select a feature from the sidebar to begin.")
