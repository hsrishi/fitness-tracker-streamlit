# Imports
import streamlit as st


if __name__ == "__main__":
    st.set_page_config(
        page_title="Fitness Tracker",
        page_icon="👋",
    )
    # title/sidebar
    text = st.sidebar.title("Contents")
    title = st.title("Fitness Tracker")
    
    st.sidebar.success("Select a section from above.")

