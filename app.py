
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Load data
company_df = pd.read_csv("company_info.csv")
audience_df = pd.read_csv("audience_info.csv")
budget_df = pd.read_csv("event_budget.csv")
history_df = pd.read_csv("history_event.csv")

# Sidebar navigation
st.set_page_config(page_title="Expo Dashboard", layout="wide")
st.sidebar.image("https://static.streamlit.io/examples/dash-icon.png", width=50)
st.sidebar.title("Expo Management Dashboard")
page = st.sidebar.radio("Select a page:", ["Home", "Companies", "Finance", "Audience Insights", "History"])

if page == "Home":
    st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d", use_column_width=True)
    st.title("📊 Expo Data Visualization Platform")

    # Fireworks animation for welcome
    components.html("""
    <script src='https://cdn.jsdelivr.net/npm/fireworks-js@2.1.0/dist/index.umd.js'></script>
    <canvas id='fireworks' style='position:fixed; top:0; left:0; width:100vw; height:100vh; z-index:-1;'></canvas>
    <script>
      const container = document.getElementById('fireworks');
      const fireworks = new Fireworks.default(container, {
        autoresize: true,
        opacity: 0.4,
        acceleration: 1.05,
        friction: 0.97,
        gravity: 1.5,
        particles: 80,
        trace: 3,
        explosion: 5,
        intensity: 20,
        flickering: 50,
        lineStyle: 'round',
        hue: { min: 0, max: 360 },
        delay: { min: 15, max: 30 },
        rocketsPoint: { min: 50, max: 50 }
      });
      fireworks.start();
    </script>
    """, height=0)

    st.markdown("""
    👋 **Hello, Professor WANG Jingbo!**

    My name is Zoey Zhou, and this is my personal submission for the CUHK Marketing data application coursework.

    The theme of this project is **Expo Management** — an area that resonates with me as I majored in **Events Management during my undergraduate studies**. My academic background and past exposure to real-world exhibitions inspired me to simulate a mini expo dashboard to visualize how companies, audiences, and financials interconnect in this field.

    This dashboard includes:
    - 🏢 Company participation across industries and sizes
    - 💰 Financial planning and budget simulations
    - 👥 Audience demographics by gender, age, and city
    - 📅 Historical attendance trends

    Please use the sidebar to explore the sections. I hope this project not only showcases my skills in Streamlit and data visualization, but also demonstrates my passion and domain knowledge in the event industry. 😊
    """)

st.markdown("---")
st.caption("Developed with ❤️ by ZHOU Yiting | UID: 1155197902 | CUHK 2025 | Streamlit + Plotly")
