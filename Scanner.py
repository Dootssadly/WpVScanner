import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_wp_version(url):
    try:
        if not url.startswith("http"):
            url = "http://" + url

        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Try meta tag first
        generator = soup.find("meta", attrs={"name": "generator"})
        if generator and "WordPress" in generator.get("content", ""):
            return generator["content"]

        # Try RSS feed as a backup
        feed_url = url.rstrip("/") + "/feed/"
        response = requests.get(feed_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'xml')
        generator = soup.find("generator")
        if generator and "WordPress" in generator.text:
            return generator.text.strip()

        return "Version not found (hidden or not a WP site)"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit App
st.set_page_config(page_title="WP Version Checker", page_icon="🧠", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: white;
    }
    .stApp {
        background-color: #0e1117;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔍 WordPress Version Checker")

url = st.text_input("Enter website URL", placeholder="e.g. https://example.com")

if st.button("Check Version"):
    if url.strip():
        with st.spinner("Checking..."):
            version_info = get_wp_version(url.strip())
        st.success(f"✅ {version_info}")
    else:
        st.warning("Please enter a valid URL.")
