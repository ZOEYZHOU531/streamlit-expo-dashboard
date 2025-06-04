import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

# Page config and custom theme
st.set_page_config(page_title="Expo Dashboard", layout="wide")
st.markdown("""
<style>
html, body, .block-container, [class*="css"] {
    font-size: 17px;
    background-color: #f5f7ff;
    color: #333;
}
section.main > div {
    padding: 2rem;
    background-color: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    margin: 2rem auto;
}
.stSidebar {
    background-color: #f0f2f8 !important;
}
@keyframes fadeInUp {
  0% {opacity: 0; transform: translateY(20px);}
  100% {opacity: 1; transform: translateY(0);}
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
    <h1 style='text-align: center; color: #2a2a2a;'>🎪 Welcome to the Expo Intelligence Dashboard</h1>
    <p style='text-align: center;'>Crafted by ZHOU Yiting | CUHK MSc Marketing | Machine Learning in Marketing (MKTG6037MA)</p>
    """, unsafe_allow_html=True)

    st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3NrZjRkdGpid2cwMzlxNWt2djh1OWxmMm94bzR2b3VqZGpvNmVodiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/2S5rxKZ6c3eQbe7Etf/giphy.gif", use_column_width=True)

    

    name_input = st.text_input("🙋‍♂️ Say hi to me here:", "")
    if name_input:
        st.success(f"""Hi {name_input}, welcome to the dashboard! 🎉

I'm Zoey Zhou, and this is my final individual coursework for the course Machine Learning in Marketing (MKTG6037MA).

With an undergraduate background in Events Management, I've always been curious about how data and machine learning can elevate experience design and operational precision in large-scale exhibitions. This dashboard is built to simulate that world:

• 🏢 Visualize company participation trends
• 💸 Analyze budgeting vs real revenue
• 🎫 Explore audience structures: gender, age, city
• 📅 Examine historical turnout data

I hope this interactive experience brings insights and maybe a bit of delight ✨""")

    st.markdown("### 📈 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Companies", len(company_df))
    col2.metric("Audience Size", len(audience_df))
    col3.metric("Total Revenue", f"${budget_df['ActualRevenue'].sum():,.0f}")

    st.markdown("### 📊 Revenue vs Budget")
    fig = px.bar(budget_df, x="EventName", y=["PlannedBudget", "ActualRevenue"], barmode='group')
    fig.update_layout(title="Budget vs Revenue", legend_title_text='Metric', yaxis_title="USD")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Companies":
    st.title("🏢 Company Participation")
    industry_filter = st.multiselect("Select Industry:", options=sorted(company_df["Industry"].unique().tolist()), default=company_df["Industry"].unique().tolist())
    size_filter = st.multiselect("Select Company Size:", options=sorted(company_df["Size"].unique().tolist()), default=company_df["Size"].unique().tolist())
    filtered_df = company_df[(company_df["Industry"].isin(industry_filter)) & (company_df["Size"].isin(size_filter))]
    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("### 🔍 Companies by Industry")
    industry_counts = filtered_df["Industry"].value_counts().reset_index()
    industry_counts.columns = ["Industry", "Company Count"]
    fig_industry = px.bar(industry_counts, x="Industry", y="Company Count", color="Industry")
    st.plotly_chart(fig_industry, use_container_width=True)

elif page == "Finance":
    st.title("💰 Financial Breakdown")
    selected_event = st.selectbox("Choose an Event:", options=budget_df["EventName"].tolist())
    event_data = budget_df[budget_df["EventName"] == selected_event].iloc[0]
    values = [event_data["PromotionCost"], event_data["VenueCost"], event_data["ActualRevenue"]]
    labels = ["Promotion Cost", "Venue Cost", "Actual Revenue"]
    fig_pie = px.pie(values=values, names=labels, title=f"{selected_event} Financial Breakdown")
    st.plotly_chart(fig_pie, use_container_width=True)

    st.subheader("🔧 Simulate Budget Allocation")
    venue_ratio = st.slider("Venue Cost %", 10, 80, 25)
    promo_ratio = 100 - venue_ratio
    venue_cost = int(event_data["PlannedBudget"] * venue_ratio / 100)
    promo_cost = int(event_data["PlannedBudget"] * promo_ratio / 100)
    simulated_values = [promo_cost, venue_cost, event_data["ActualRevenue"]]
    fig_sim = px.pie(values=simulated_values, names=["Promotion Cost", "Venue Cost", "Actual Revenue"], title="Simulated Budget Split")
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

    st.markdown("### 🎂 Age Distribution")
    age_hist = px.histogram(audience_df, x="Age", nbins=10, color_discrete_sequence=['#636EFA'])
    st.plotly_chart(age_hist, use_container_width=True)

    st.markdown("### 🌍 Audience by City")
    city_counts = audience_df["City"].value_counts().reset_index()
    city_counts.columns = ["City", "Audience Count"]
    fig_city = px.bar(city_counts, x="City", y="Audience Count", color="City")
    st.plotly_chart(fig_city, use_container_width=True)

elif page == "History":
    st.title("📅 Historical Events")
    year_range = st.slider("Select Year Range:", 2019, 2024, (2019, 2024))
    history_df["Year"] = pd.to_datetime(history_df["Date"]).dt.year
    filtered_history = history_df[history_df["Year"].between(year_range[0], year_range[1])]
    st.dataframe(filtered_history, use_container_width=True)

    st.markdown("### 📈 Audience Count Over Time")
    fig_line = px.line(filtered_history, x="Date", y="AudienceCount", title="Trend of Audience Count")
    st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown("---")
st.caption("Developed with ❤️ by ZHOU Yiting | UID: 1155197902 | CUHK 2025 | Streamlit + Plotly")
