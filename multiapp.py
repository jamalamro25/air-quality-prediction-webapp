import streamlit as st

class MultiApp:
    """Framework for combining multiple Streamlit applications."""

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Add a new application.

        Args:
            title (str): Title shown in the sidebar.
            func (callable): Function that renders the page (must be app()).
        """
        self.apps.append({"title": title, "function": func})

    def run(self):
        titles = [a["title"] for a in self.apps]

        st.sidebar.title("<< Navigator >>")
        choice = st.sidebar.radio("Go to", titles)

        for app in self.apps:
            if app["title"] == choice:
                app["function"]()
                break
