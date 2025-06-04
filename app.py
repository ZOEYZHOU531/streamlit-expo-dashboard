
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Page config and styling
st.set_page_config(page_title="Expo Dashboard", layout="wide")
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #f8f9fa, #ffffff);
}
.block-container {
    padding: 2rem;
    max-width: 1200px;
    margin: auto;
}
.stSidebar {
    background-color: #f1f3f6 !important;
}
section.main > div {
    padding: 1rem 2rem 2rem 2rem;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.stMarkdown, .stTitle, .stHeader {
    font-size: 1.1rem;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 📂 Expo Management Dashboard")
page = st.sidebar.radio("Select a page:", ["Home", "Companies", "Finance", "Audience Insights", "History"])

# Load data
company_df = pd.read_csv("company_info.csv")
audience_df = pd.read_csv("audience_info.csv")
budget_df = pd.read_csv("event_budget.csv")
history_df = pd.read_csv("history_event.csv")

if page == "Home":
    st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d", use_container_width=True)
    st.title("📊 Expo Data Visualization Platform")

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

    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Companies", len(company_df))
    col2.metric("Total Audience", len(audience_df))
    col3.metric("Total Revenue", f"${budget_df['ActualRevenue'].sum():,.0f}")

    st.subheader("📊 Budget vs Revenue")
    fig = px.bar(budget_df, x="EventName", y=["PlannedBudget", "ActualRevenue"], barmode='group',
                 title="Planned Budget vs. Actual Revenue")
    fig.update_layout(legend_title_text='Metric', yaxis_title="Amount")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Companies":
    st.title("🏢 Company Participation")
    industry_filter = st.multiselect("Select Industry:", options=sorted(company_df["Industry"].unique().tolist()), default=company_df["Industry"].unique().tolist())
    size_filter = st.multiselect("Select Company Size:", options=sorted(company_df["Size"].unique().tolist()), default=company_df["Size"].unique().tolist())
    filtered_df = company_df[(company_df["Industry"].isin(industry_filter)) & (company_df["Size"].isin(size_filter))]
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📊 Companies by Industry")
    industry_counts = filtered_df["Industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Company Count"]
    fig_industry = px.bar(industry_counts, x="Industry", y="Company Count", title="Number of Companies per Industry")
    st.plotly_chart(fig_industry, use_container_width=True)

elif page == "Finance":
    st.title("💰 Financial Breakdown")
    selected_event = st.selectbox("Choose an Event:", options=budget_df["EventName"].tolist())
    event_data = budget_df[budget_df["EventName"] == selected_event].iloc[0]
    values = [event_data["PromotionCost"], event_data["VenueCost"], event_data["ActualRevenue"]]
    labels = ["Promotion Cost", "Venue Cost", "Actual Revenue"]
    fig_pie = px.pie(values=values, names=labels, title=f"{selected_event} Financial Breakdown")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("🛠️ Simulate Budget Changes")
    venue_ratio = st.slider("Venue Cost %", 10, 80, 25)
    promo_ratio = 100 - venue_ratio
    venue_cost = int(event_data["PlannedBudget"] * venue_ratio / 100)
    promo_cost = int(event_data["PlannedBudget"] * promo_ratio / 100)
    simulated_values = [promo_cost, venue_cost, event_data["ActualRevenue"]]
    fig_sim = px.pie(values=simulated_values, names=["Promotion Cost", "Venue Cost", "Actual Revenue"],
                     title="Simulated Budget Breakdown")
    st.plotly_chart(fig_sim, use_container_width=True)

elif page == "Audience Insights":
    st.title("👥 Audience Demographics")
    col1, col2 = st.columns(2)
    with col1:
        gender_chart = px.pie(audience_df, names="Gender", title="Gender Distribution", color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(gender_chart, use_container_width=True)
    with col2:
        ticket_chart = px.pie(audience_df, names="TicketType", title="Ticket Type", color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(ticket_chart, use_container_width=True)

    age_hist = px.histogram(audience_df, x="Age", nbins=10, title="Age Distribution", color_discrete_sequence=['#636EFA'])
    st.plotly_chart(age_hist, use_container_width=True)

    st.subheader("🌍 Audience by City")
    city_counts = audience_df["City"].value_counts().reset_index()
    city_counts.columns = ["City", "Audience Count"]
    fig_city = px.bar(city_counts, x="City", y="Audience Count", color="City", title="Audience Distribution by City")
    st.plotly_chart(fig_city, use_container_width=True)

elif page == "History":
    st.title("📅 Historical Events")
    year_range = st.slider("Select Year Range:", 2019, 2024, (2019, 2024))
    history_df["Year"] = pd.to_datetime(history_df["Date"]).dt.year
    filtered_history = history_df[history_df["Year"].between(year_range[0], year_range[1])]
    st.dataframe(filtered_history, use_container_width=True)
    fig_line = px.line(filtered_history, x="Date", y="AudienceCount", title="Audience Count Over Time")
    st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")
st.caption("Developed with ❤️ by ZHOU Yiting | UID: 1155197902 | CUHK 2025 | Streamlit + Plotly")
