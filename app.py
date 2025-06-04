import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Page config and global theme
st.set_page_config(page_title="Expo Dashboard", layout="wide")
st.markdown("""
<style>
html, body, [class*="css"]  {
    font-size: 18px;
}
section.main > div {
    padding: 2rem;
    background-color: #fff;
    border-radius: 12px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
}
.stSidebar {
    background-color: #f9f9fa !important;
}
.st-bd {
    background-color: #f4f6fa !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
## 🎯 Navigation
---
""")
page = st.sidebar.radio("Go to:", ["Home", "Companies", "Finance", "Audience Insights", "History"])

# Load data
company_df = pd.read_csv("company_info.csv")
audience_df = pd.read_csv("audience_info.csv")
budget_df = pd.read_csv("event_budget.csv")
history_df = pd.read_csv("history_event.csv")

# Home Page
if page == "Home":
    st.markdown("""
        <h1 style='text-align: center; color: #333;'>🎪 Welcome to the Expo Intelligence Dashboard</h1>
        <p style='text-align: center;'>Crafted by ZHOU Yiting | CUHK MSc Marketing</p>
    """, unsafe_allow_html=True)

    components.html("""
    <div style='text-align:center;'>
        <lottie-player src="https://assets2.lottiefiles.com/packages/lf20_hdy0htc5.json"  background="transparent"  speed="1"  style="width: 300px; height: 300px; margin:auto"  loop  autoplay></lottie-player>
        <script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
    </div>
    """, height=320)

    with st.container():
        st.markdown("""
        👋 **Hello Professor WANG Jingbo,**

        I'm Zoey Zhou, and this is my final individual coursework for CUHK's Marketing class — a Streamlit project themed on **Expo Management**.

        Having studied **Events Management** during my undergraduate years, I’m passionate about how data can drive smarter planning in large-scale exhibitions. This dashboard aims to provide an intuitive overview of:

        - 🏢 Company participation and trends
        - 💸 Financial allocation vs actual revenue
        - 🎫 Audience profiles (gender, age, city)
        - 📅 Attendance evolution over time

        Feel free to explore using the sidebar. I hope you enjoy this data journey. ✨
        """)

    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Companies", len(company_df))
    col2.metric("Audience Size", len(audience_df))
    col3.metric("Total Revenue", f"${budget_df['ActualRevenue'].sum():,.0f}")

    st.markdown("### 📊 Revenue vs Budget")
    fig = px.bar(budget_df, x="EventName", y=["PlannedBudget", "ActualRevenue"], barmode='group',
                 title="Planned Budget vs. Actual Revenue")
    fig.update_layout(legend_title_text='Metric', yaxis_title="Amount")
    st.plotly_chart(fig, use_container_width=True)

# (other pages remain unchanged)

st.markdown("---")
st.caption("Developed with ❤️ by ZHOU Yiting | UID: 1155197902 | CUHK 2025 | Streamlit + Plotly")
